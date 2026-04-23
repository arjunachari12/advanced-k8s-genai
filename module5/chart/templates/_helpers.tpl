{{- define "genai-platform.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "genai-platform.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := include "genai-platform.name" . -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "genai-platform.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "genai-platform.labels" -}}
helm.sh/chart: {{ include "genai-platform.chart" . }}
app.kubernetes.io/name: {{ include "genai-platform.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "genai-platform.selectorLabels" -}}
app.kubernetes.io/name: {{ include "genai-platform.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "genai-platform.componentName" -}}
{{- printf "%s-%s" (include "genai-platform.fullname" .root) .component | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "genai-platform.componentLabels" -}}
{{ include "genai-platform.selectorLabels" .root }}
app.kubernetes.io/component: {{ .component }}
{{- end -}}

{{- define "genai-platform.namespace" -}}
{{- .Release.Namespace -}}
{{- end -}}

{{- define "genai-platform.llmServiceUrl" -}}
http://{{ include "genai-platform.componentName" (dict "root" . "component" "llm") }}.{{ include "genai-platform.namespace" . }}.svc.cluster.local:{{ .Values.llm.service.port }}
{{- end -}}

{{- define "genai-platform.apiServiceUrl" -}}
http://{{ include "genai-platform.componentName" (dict "root" . "component" "api") }}.{{ include "genai-platform.namespace" . }}.svc.cluster.local:{{ .Values.api.service.port }}
{{- end -}}
