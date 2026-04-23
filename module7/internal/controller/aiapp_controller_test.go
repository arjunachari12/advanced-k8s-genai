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

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"

	aiv1alpha1 "github.com/arjun/genai-k8s/module7/ai-workload-operator/api/v1alpha1"
)

var _ = Describe("AIApp Controller", func() {
	const (
		resourceName = "test-aiapp"
		namespace    = "default"
	)

	ctx := context.Background()
	typeNamespacedName := types.NamespacedName{Name: resourceName, Namespace: namespace}

	BeforeEach(func() {
		resource := &aiv1alpha1.AIApp{
			ObjectMeta: metav1.ObjectMeta{
				Name:      resourceName,
				Namespace: namespace,
			},
			Spec: aiv1alpha1.AIAppSpec{
				Image: "example.com/genai-api:test",
			},
		}

		err := k8sClient.Get(ctx, typeNamespacedName, &aiv1alpha1.AIApp{})
		if apierrors.IsNotFound(err) {
			Expect(k8sClient.Create(ctx, resource)).To(Succeed())
			return
		}

		Expect(err).NotTo(HaveOccurred())
	})

	AfterEach(func() {
		resource := &aiv1alpha1.AIApp{}
		err := k8sClient.Get(ctx, typeNamespacedName, resource)
		if apierrors.IsNotFound(err) {
			return
		}
		Expect(err).NotTo(HaveOccurred())
		Expect(k8sClient.Delete(ctx, resource)).To(Succeed())

		deployment := &appsv1.Deployment{}
		err = k8sClient.Get(ctx, typeNamespacedName, deployment)
		if err == nil {
			Expect(k8sClient.Delete(ctx, deployment)).To(Succeed())
		} else {
			Expect(apierrors.IsNotFound(err)).To(BeTrue())
		}

		service := &corev1.Service{}
		err = k8sClient.Get(ctx, typeNamespacedName, service)
		if err == nil {
			Expect(k8sClient.Delete(ctx, service)).To(Succeed())
		} else {
			Expect(apierrors.IsNotFound(err)).To(BeTrue())
		}
	})

	It("creates managed resources and reports pending status before pods are ready", func() {
		controllerReconciler := &AIAppReconciler{
			Client: k8sClient,
			Scheme: k8sClient.Scheme(),
		}

		_, err := controllerReconciler.Reconcile(ctx, reconcile.Request{NamespacedName: typeNamespacedName})
		Expect(err).NotTo(HaveOccurred())

		deployment := &appsv1.Deployment{}
		Expect(k8sClient.Get(ctx, typeNamespacedName, deployment)).To(Succeed())
		Expect(*deployment.Spec.Replicas).To(Equal(int32(1)))
		Expect(deployment.Spec.Template.Spec.Containers).To(HaveLen(1))

		container := deployment.Spec.Template.Spec.Containers[0]
		Expect(container.Image).To(Equal("example.com/genai-api:test"))
		Expect(container.Ports).To(HaveLen(1))
		Expect(container.Ports[0].ContainerPort).To(Equal(int32(defaultPort)))
		Expect(container.Env).To(ContainElements(
			corev1.EnvVar{Name: "APP_NAME", Value: resourceName},
			corev1.EnvVar{Name: "LOG_LEVEL", Value: defaultLogLevel},
			corev1.EnvVar{Name: "LLM_URL", Value: defaultLLMURL},
			corev1.EnvVar{Name: "MODEL_NAME", Value: defaultModelName},
		))

		service := &corev1.Service{}
		Expect(k8sClient.Get(ctx, typeNamespacedName, service)).To(Succeed())
		Expect(service.Spec.Type).To(Equal(defaultServiceType))
		Expect(service.Spec.Ports).To(HaveLen(1))
		Expect(service.Spec.Ports[0].Port).To(Equal(int32(defaultPort)))

		updatedAIApp := &aiv1alpha1.AIApp{}
		Expect(k8sClient.Get(ctx, typeNamespacedName, updatedAIApp)).To(Succeed())
		Expect(updatedAIApp.Status.Phase).To(Equal("Pending"))
		Expect(updatedAIApp.Status.ReadyReplicas).To(BeZero())
		Expect(updatedAIApp.Status.DeploymentName).To(Equal(resourceName))
		Expect(updatedAIApp.Status.ServiceName).To(Equal(resourceName))
		Expect(metaConditionStatus(updatedAIApp.Status.Conditions, conditionTypeAvailable)).To(Equal(metav1.ConditionFalse))
		Expect(metaConditionReason(updatedAIApp.Status.Conditions, conditionTypeAvailable)).To(Equal("DeploymentProgressing"))
		Expect(metaConditionStatus(updatedAIApp.Status.Conditions, conditionTypeReconciling)).To(Equal(metav1.ConditionTrue))
		Expect(metaConditionReason(updatedAIApp.Status.Conditions, conditionTypeReconciling)).To(Equal("ReconcilingResources"))
	})
})

func metaConditionStatus(conditions []metav1.Condition, conditionType string) metav1.ConditionStatus {
	for _, condition := range conditions {
		if condition.Type == conditionType {
			return condition.Status
		}
	}
	return metav1.ConditionUnknown
}

func metaConditionReason(conditions []metav1.Condition, conditionType string) string {
	for _, condition := range conditions {
		if condition.Type == conditionType {
			return condition.Reason
		}
	}
	return ""
}
