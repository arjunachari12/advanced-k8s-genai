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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// AIAppSpec defines the desired state of AIApp.
type AIAppSpec struct {
	// Image is the container image used for the managed AI API workload.
	Image string `json:"image,omitempty"`

	// Replicas is the desired pod count for the managed Deployment.
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=5
	// +kubebuilder:default=1
	Replicas *int32 `json:"replicas,omitempty"`

	// Port is the application container and Service port.
	// +kubebuilder:default=8000
	Port int32 `json:"port,omitempty"`

	// ServiceType controls how the Service is exposed inside the cluster.
	// +kubebuilder:validation:Enum=ClusterIP;NodePort;LoadBalancer
	// +kubebuilder:default=ClusterIP
	ServiceType string `json:"serviceType,omitempty"`

	// ModelName is passed to the API container as MODEL_NAME.
	// +kubebuilder:default=tinyllama
	ModelName string `json:"modelName,omitempty"`

	// LLMURL points the managed API pods to the LLM endpoint they should call.
	LLMURL string `json:"llmUrl,omitempty"`

	// LogLevel controls the verbosity of the API workload.
	// +kubebuilder:validation:Enum=DEBUG;INFO;WARNING;ERROR
	// +kubebuilder:default=INFO
	LogLevel string `json:"logLevel,omitempty"`
}

// AIAppStatus defines the observed state of AIApp.
type AIAppStatus struct {
	// Phase is a compact summary of the current reconciliation result.
	Phase string `json:"phase,omitempty"`

	// ReadyReplicas is the number of ready pods currently reported by the Deployment.
	ReadyReplicas int32 `json:"readyReplicas,omitempty"`

	// DeploymentName is the managed Deployment name.
	DeploymentName string `json:"deploymentName,omitempty"`

	// ServiceName is the managed Service name.
	ServiceName string `json:"serviceName,omitempty"`

	// Conditions stores the latest reconciliation conditions.
	Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// AIApp is the Schema for the aiapps API.
type AIApp struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   AIAppSpec   `json:"spec,omitempty"`
	Status AIAppStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// AIAppList contains a list of AIApp.
type AIAppList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []AIApp `json:"items"`
}

func init() {
	SchemeBuilder.Register(&AIApp{}, &AIAppList{})
}
