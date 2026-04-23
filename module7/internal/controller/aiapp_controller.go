/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"fmt"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	apimeta "k8s.io/apimachinery/pkg/api/meta"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/intstr"
	"k8s.io/client-go/util/retry"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/log"

	aiv1alpha1 "github.com/arjun/genai-k8s/module7/ai-workload-operator/api/v1alpha1"
)

const (
	conditionTypeAvailable   = "Available"
	conditionTypeReconciling = "Reconciling"
	defaultImage             = "arjunachari12/genai-api:1.0.0"
	defaultPort              = 8000
	defaultServiceType       = corev1.ServiceTypeClusterIP
	defaultModelName         = "tinyllama"
	defaultLLMURL            = "http://genai-genai-platform-llm.genai-staging.svc.cluster.local:11434"
	defaultLogLevel          = "INFO"
)

// AIAppReconciler reconciles a AIApp object.
type AIAppReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=ai.workshop.io,resources=aiapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=ai.workshop.io,resources=aiapps/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=ai.workshop.io,resources=aiapps/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups="",resources=services,verbs=get;list;watch;create;update;patch;delete

// Reconcile makes the cluster match the desired AIApp state.
func (r *AIAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)

	var aiApp aiv1alpha1.AIApp
	if err := r.Get(ctx, req.NamespacedName, &aiApp); err != nil {
		if apierrors.IsNotFound(err) {
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	deployment, err := r.reconcileDeployment(ctx, &aiApp)
	if err != nil {
		return ctrl.Result{}, err
	}

	service, err := r.reconcileService(ctx, &aiApp)
	if err != nil {
		return ctrl.Result{}, err
	}

	var currentDeployment appsv1.Deployment
	if err := r.Get(ctx, types.NamespacedName{Name: deployment.Name, Namespace: deployment.Namespace}, &currentDeployment); err != nil {
		return ctrl.Result{}, err
	}

	phase := "Pending"
	availableStatus := metav1.ConditionFalse
	availableReason := "DeploymentProgressing"
	availableMessage := "Waiting for managed pods to become ready."
	reconcilingStatus := metav1.ConditionTrue
	reconcilingReason := "ReconcilingResources"
	reconcilingMessage := "Controller is converging the Deployment and Service."

	if currentDeployment.Status.ReadyReplicas == pointerValue(aiApp.Spec.Replicas, 1) {
		phase = "Ready"
		availableStatus = metav1.ConditionTrue
		availableReason = "DeploymentReady"
		availableMessage = "Deployment is available and serving traffic."
		reconcilingStatus = metav1.ConditionFalse
		reconcilingReason = "DesiredStateReached"
		reconcilingMessage = "Live state matches the AIApp spec."
	}

	updated := aiApp.DeepCopy()
	updated.Status.Phase = phase
	updated.Status.ReadyReplicas = currentDeployment.Status.ReadyReplicas
	updated.Status.DeploymentName = deployment.Name
	updated.Status.ServiceName = service.Name
	setCondition(&updated.Status.Conditions, metav1.Condition{
		Type:               conditionTypeAvailable,
		Status:             availableStatus,
		Reason:             availableReason,
		Message:            availableMessage,
		LastTransitionTime: metav1.Now(),
		ObservedGeneration: aiApp.Generation,
	})
	setCondition(&updated.Status.Conditions, metav1.Condition{
		Type:               conditionTypeReconciling,
		Status:             reconcilingStatus,
		Reason:             reconcilingReason,
		Message:            reconcilingMessage,
		LastTransitionTime: metav1.Now(),
		ObservedGeneration: aiApp.Generation,
	})

	if err := r.Status().Patch(ctx, updated, client.MergeFrom(&aiApp)); err != nil {
		logger.Error(err, "unable to update AIApp status")
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *AIAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&aiv1alpha1.AIApp{}).
		Owns(&appsv1.Deployment{}).
		Owns(&corev1.Service{}).
		Named("aiapp").
		Complete(r)
}

func desiredDeployment(aiApp *aiv1alpha1.AIApp) *appsv1.Deployment {
	spec := normalizedSpec(aiApp)
	labels := map[string]string{
		"app.kubernetes.io/name":       "aiapp",
		"app.kubernetes.io/instance":   aiApp.Name,
		"app.kubernetes.io/managed-by": "aiapp-operator",
	}

	replicas := pointerValue(spec.Replicas, 1)
	port := spec.Port

	return &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      aiApp.Name,
			Namespace: aiApp.Namespace,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: labels,
					Annotations: map[string]string{
						"prometheus.io/scrape": "true",
						"prometheus.io/port":   fmt.Sprintf("%d", port),
						"prometheus.io/path":   "/metrics",
					},
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:            "api",
							Image:           spec.Image,
							ImagePullPolicy: corev1.PullIfNotPresent,
							Ports: []corev1.ContainerPort{
								{
									Name:          "http",
									ContainerPort: port,
								},
							},
							Env: []corev1.EnvVar{
								{Name: "APP_NAME", Value: aiApp.Name},
								{Name: "LOG_LEVEL", Value: spec.LogLevel},
								{Name: "LLM_URL", Value: spec.LLMURL},
								{Name: "MODEL_NAME", Value: spec.ModelName},
								{Name: "OLLAMA_TIMEOUT_SECONDS", Value: "120"},
							},
							ReadinessProbe: &corev1.Probe{
								ProbeHandler: corev1.ProbeHandler{
									HTTPGet: &corev1.HTTPGetAction{
										Path: "/health",
										Port: intstrFromString("http"),
									},
								},
								InitialDelaySeconds: 10,
								PeriodSeconds:       10,
							},
							LivenessProbe: &corev1.Probe{
								ProbeHandler: corev1.ProbeHandler{
									HTTPGet: &corev1.HTTPGetAction{
										Path: "/health",
										Port: intstrFromString("http"),
									},
								},
								InitialDelaySeconds: 20,
								PeriodSeconds:       20,
							},
						},
					},
				},
			},
		},
	}
}

func desiredService(aiApp *aiv1alpha1.AIApp) *corev1.Service {
	spec := normalizedSpec(aiApp)
	labels := map[string]string{
		"app.kubernetes.io/name":       "aiapp",
		"app.kubernetes.io/instance":   aiApp.Name,
		"app.kubernetes.io/managed-by": "aiapp-operator",
	}

	port := spec.Port
	serviceType := corev1.ServiceType(spec.ServiceType)

	return &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:      aiApp.Name,
			Namespace: aiApp.Namespace,
		},
		Spec: corev1.ServiceSpec{
			Type:     serviceType,
			Selector: labels,
			Ports: []corev1.ServicePort{
				{
					Name:       "http",
					Port:       port,
					TargetPort: intstrFromString("http"),
					Protocol:   corev1.ProtocolTCP,
				},
			},
		},
	}
}

func setCondition(conditions *[]metav1.Condition, condition metav1.Condition) {
	apimeta.SetStatusCondition(conditions, condition)
}

func pointerValue(value *int32, fallback int32) int32 {
	if value == nil {
		return fallback
	}
	return *value
}

func intstrFromString(value string) intstr.IntOrString {
	return intstr.FromString(value)
}

func (r *AIAppReconciler) reconcileDeployment(ctx context.Context, aiApp *aiv1alpha1.AIApp) (*appsv1.Deployment, error) {
	deployment := desiredDeployment(aiApp)
	if err := retry.RetryOnConflict(retry.DefaultRetry, func() error {
		_, err := controllerutil.CreateOrUpdate(ctx, r.Client, deployment, func() error {
			deployment.Spec = desiredDeployment(aiApp).Spec
			return controllerutil.SetControllerReference(aiApp, deployment, r.Scheme)
		})
		return err
	}); err != nil {
		return nil, err
	}
	return deployment, nil
}

func (r *AIAppReconciler) reconcileService(ctx context.Context, aiApp *aiv1alpha1.AIApp) (*corev1.Service, error) {
	service := desiredService(aiApp)
	if err := retry.RetryOnConflict(retry.DefaultRetry, func() error {
		_, err := controllerutil.CreateOrUpdate(ctx, r.Client, service, func() error {
			service.Spec = desiredService(aiApp).Spec
			return controllerutil.SetControllerReference(aiApp, service, r.Scheme)
		})
		return err
	}); err != nil {
		return nil, err
	}
	return service, nil
}

func normalizedSpec(aiApp *aiv1alpha1.AIApp) aiv1alpha1.AIAppSpec {
	spec := aiApp.Spec.DeepCopy()
	if spec == nil {
		spec = &aiv1alpha1.AIAppSpec{}
	}
	if spec.Image == "" {
		spec.Image = defaultImage
	}
	if spec.Port == 0 {
		spec.Port = defaultPort
	}
	if spec.ServiceType == "" {
		spec.ServiceType = string(defaultServiceType)
	}
	if spec.ModelName == "" {
		spec.ModelName = defaultModelName
	}
	if spec.LLMURL == "" {
		spec.LLMURL = defaultLLMURL
	}
	if spec.LogLevel == "" {
		spec.LogLevel = defaultLogLevel
	}
	return *spec
}
