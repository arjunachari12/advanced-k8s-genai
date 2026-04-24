# Production Agentic System Architecture
## Use Case: Kubernetes SRE Agent using LangGraph + MCP + Kubernetes

---

## 1. Production Use Case

### Scenario

A user asks:

> Why is `payment-api` failing in production?

The agentic system investigates Kubernetes, logs, metrics, traces, GitOps history, and cloud infrastructure. It then produces a root cause analysis and optionally performs a safe remediation after human approval.

---

## 2. Big Picture Architecture

```mermaid
flowchart TD
    U[User / Slack / Web UI] --> API[Agent API - FastAPI]
    API --> LG[LangGraph Orchestrator]

    LG --> PA[Planner Agent]
    LG --> KA[Kubernetes Investigator Agent]
    LG --> OA[Observability Agent]
    LG --> GA[GitOps / ArgoCD Agent]
    LG --> RA[Root Cause Analyzer]
    LG --> RV[Reviewer Agent]
    LG --> RM[Remediation Agent]

    LG --> MCP[MCP Tool Layer]

    MCP --> K8S[k8s-mcp-server]
    MCP --> PROM[prometheus-mcp-server]
    MCP --> LOKI[loki-mcp-server]
    MCP --> ARGO[argocd-mcp-server]
    MCP --> GH[github-mcp-server]

    K8S --> KC[Kubernetes Cluster]
    PROM --> PM[Prometheus]
    LOKI --> LK[Loki / Grafana]
    ARGO --> AC[Argo CD]
    GH --> GIT[GitHub]
```

### Explanation

| Layer | Responsibility |
|---|---|
| User Interface | Slack, Teams, Web UI, CLI |
| Agent API | Receives user request |
| LangGraph | Controls workflow and agent routing |
| Agents | Planner, investigator, reviewer, remediation |
| MCP Servers | Provide standard tool access |
| External Systems | Kubernetes, Prometheus, Loki, ArgoCD, GitHub |

---

## 3. Simple Explanation for Students

```text
LangGraph = Brain / Workflow engine
MCP       = Tool connection standard
Kubernetes = Runtime platform
```

### Example

```text
User asks: Why is payment-api failing?

LangGraph decides the steps.
MCP tools collect real data.
Kubernetes runs the agentic system.
```

---

## 4. LangGraph Agent Workflow

```mermaid
flowchart TD
    START([START]) --> INPUT[Receive Incident Question]
    INPUT --> PLANNER[Planner Agent]

    PLANNER --> K8S[Kubernetes Investigator]
    K8S --> OBS[Observability Investigator]
    OBS --> GITOPS[GitOps / ArgoCD Investigator]
    GITOPS --> RCA[Root Cause Analyzer]
    RCA --> REVIEW[Reviewer Agent]

    REVIEW --> DECISION{Need Remediation?}

    DECISION -->|No| REPORT[Generate Diagnosis Report]
    DECISION -->|Yes| APPROVAL{Human Approved?}

    APPROVAL -->|No| REPORT
    APPROVAL -->|Yes| FIX[Remediation Agent]

    FIX --> VERIFY[Verify Recovery]
    VERIFY --> FINAL[Final Incident Summary]
    REPORT --> FINAL
    FINAL --> END([END])
```

---

## 5. Agent Responsibilities

```mermaid
flowchart LR
    P[Planner Agent] -->|Creates investigation plan| K[Kubernetes Agent]
    K -->|Pod status, events, deployment| O[Observability Agent]
    O -->|Logs, metrics, traces| G[GitOps Agent]
    G -->|Deployment history, commits| R[Root Cause Agent]
    R -->|Finds likely cause| V[Reviewer Agent]
    V -->|Approves safe response| M[Remediation Agent]
```

### Agents

| Agent | Purpose |
|---|---|
| Planner Agent | Breaks problem into steps |
| Kubernetes Agent | Checks pods, events, deployments, nodes |
| Observability Agent | Checks logs, metrics, traces |
| GitOps Agent | Checks ArgoCD sync and Git commits |
| Root Cause Agent | Combines evidence and identifies issue |
| Reviewer Agent | Validates recommendation |
| Remediation Agent | Executes approved action |

---

## 6. MCP Tool Architecture

```mermaid
flowchart TD
    LG[LangGraph Orchestrator] --> CLIENT[MCP Client]

    CLIENT --> K8S_MCP[k8s-mcp-server]
    CLIENT --> PROM_MCP[prometheus-mcp-server]
    CLIENT --> LOKI_MCP[loki-mcp-server]
    CLIENT --> ARGO_MCP[argocd-mcp-server]
    CLIENT --> GITHUB_MCP[github-mcp-server]

    K8S_MCP --> T1[get_pods]
    K8S_MCP --> T2[describe_pod]
    K8S_MCP --> T3[get_events]
    K8S_MCP --> T4[restart_deployment]

    PROM_MCP --> T5[query_prometheus]
    PROM_MCP --> T6[get_error_rate]

    LOKI_MCP --> T7[query_logs]
    LOKI_MCP --> T8[get_recent_errors]

    ARGO_MCP --> T9[get_sync_history]
    ARGO_MCP --> T10[rollback_app]

    GITHUB_MCP --> T11[get_recent_commits]
    GITHUB_MCP --> T12[compare_versions]
```

---

## 7. Example Investigation Flow

```mermaid
sequenceDiagram
    participant User
    participant API as Agent API
    participant LG as LangGraph
    participant K8S as k8s MCP
    participant Loki as Loki MCP
    participant Prom as Prometheus MCP
    participant Argo as ArgoCD MCP
    participant Human as Human Approver

    User->>API: Why is payment-api failing?
    API->>LG: Start incident investigation
    LG->>K8S: get failing pods
    K8S-->>LG: CrashLoopBackOff pods found
    LG->>Loki: query recent logs
    Loki-->>LG: DB timeout errors
    LG->>Prom: check 5xx and latency
    Prom-->>LG: 5xx increased after 10:32 AM
    LG->>Argo: check deployment history
    Argo-->>LG: version changed v1.4.7 to v1.4.8
    LG->>LG: Analyze root cause
    LG-->>User: Likely cause found. Rollback recommended.
    User->>Human: Approve rollback?
    Human-->>LG: Approved
    LG->>Argo: rollback app
    Argo-->>LG: Rollback successful
    LG->>Prom: verify error rate
    Prom-->>LG: Errors reduced
    LG-->>User: Incident resolved summary
```

---

## 8. Kubernetes Deployment Architecture

```mermaid
flowchart TD
    subgraph NS[Namespace: agentic-sre-prod]
        ING[Ingress / API Gateway]
        API[agent-api Deployment]
        WORKER[langgraph-worker Deployment]
        REDIS[Redis - queue/cache]
        PG[Postgres - checkpoint/state]

        K8S[k8s-mcp-server Deployment]
        PROM[prometheus-mcp-server Deployment]
        LOKI[loki-mcp-server Deployment]
        ARGO[argocd-mcp-server Deployment]
        GITHUB[github-mcp-server Deployment]
    end

    USER[User / Slack / UI] --> ING
    ING --> API
    API --> WORKER
    WORKER --> REDIS
    WORKER --> PG

    WORKER --> K8S
    WORKER --> PROM
    WORKER --> LOKI
    WORKER --> ARGO
    WORKER --> GITHUB

    K8S --> CLUSTER[Target Kubernetes Cluster]
    PROM --> PROMEXT[Prometheus]
    LOKI --> LOKIEXT[Loki / Grafana]
    ARGO --> ARGOEXT[Argo CD]
    GITHUB --> GHEXT[GitHub]
```

---

## 9. Production Pod Design

### Recommended production model

```mermaid
flowchart LR
    A[agent-api pod] --> B[langgraph-worker pod]
    B --> C[k8s-mcp-server pod]
    B --> D[prometheus-mcp-server pod]
    B --> E[loki-mcp-server pod]
    B --> F[argocd-mcp-server pod]
    B --> G[github-mcp-server pod]
```

### Important point

Do **not** create one pod per logical agent initially.

Better design:

```text
Planner Agent
Kubernetes Agent
Observability Agent
Reviewer Agent
Remediation Agent
```

These are usually **logical nodes inside LangGraph**, not separate Kubernetes pods.

Separate pods are mainly for:

- MCP tool servers
- API service
- background workers
- databases
- queues

---

## 10. When to Separate Agents into Different Pods

```mermaid
flowchart TD
    Q{Should this agent be a separate pod?}

    Q -->|Needs independent scaling| YES[Yes]
    Q -->|Needs GPU| YES
    Q -->|Needs different runtime| YES
    Q -->|Needs strict isolation| YES
    Q -->|Long-running heavy jobs| YES

    Q -->|Simple reasoning node| NO[No]
    Q -->|Same codebase| NO
    Q -->|Same scaling pattern| NO

    YES --> SEP[Deploy as separate service]
    NO --> LOGICAL[Keep as LangGraph node]
```

---

## 11. Example Kubernetes Components

```text
Namespace:
  agentic-sre-prod

Deployments:
  agent-api
  langgraph-worker
  k8s-mcp-server
  prometheus-mcp-server
  loki-mcp-server
  argocd-mcp-server
  github-mcp-server

State:
  postgres
  redis

Security:
  service-account-agent
  service-account-k8s-mcp
  network-policies
  secrets
  configmaps
```

---

## 12. Example Kubernetes YAML Skeleton

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langgraph-worker
  namespace: agentic-sre-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: langgraph-worker
  template:
    metadata:
      labels:
        app: langgraph-worker
    spec:
      containers:
        - name: worker
          image: company/agentic-sre-worker:1.0.0
          env:
            - name: REDIS_URL
              value: redis://redis:6379
            - name: POSTGRES_URL
              valueFrom:
                secretKeyRef:
                  name: agent-secrets
                  key: postgres-url
            - name: K8S_MCP_URL
              value: http://k8s-mcp-server:8080
            - name: PROMETHEUS_MCP_URL
              value: http://prometheus-mcp-server:8080
```

---

## 13. MCP Server Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-mcp-server
  namespace: agentic-sre-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: k8s-mcp-server
  template:
    metadata:
      labels:
        app: k8s-mcp-server
    spec:
      serviceAccountName: k8s-mcp-reader
      containers:
        - name: k8s-mcp-server
          image: company/k8s-mcp-server:1.0.0
          ports:
            - containerPort: 8080
```

---

## 14. Service Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: k8s-mcp-server
  namespace: agentic-sre-prod
spec:
  selector:
    app: k8s-mcp-server
  ports:
    - port: 8080
      targetPort: 8080
```

---

## 15. Security Architecture

```mermaid
flowchart TD
    USER[User] --> AUTH[SSO / OIDC Auth]
    AUTH --> API[Agent API]
    API --> POLICY[Policy Engine]
    POLICY --> LG[LangGraph]

    LG --> READ[Read-only Tools]
    LG --> WRITE{Write Tool?}

    WRITE -->|No| READ
    WRITE -->|Yes| APPROVAL[Human Approval]
    APPROVAL --> AUDIT[Audit Log]
    AUDIT --> EXEC[Execute Action]

    READ --> AUDIT
```

### Security rules

```text
1. Read-only tools by default
2. Separate service account per MCP server
3. Human approval for write actions
4. NetworkPolicy between services
5. OIDC/JWT authentication
6. Audit every tool call
7. No direct public access to MCP servers
8. Separate prod and non-prod credentials
```

---

## 16. Safe vs Dangerous Actions

| Action | Auto Allowed? | Approval Needed? |
|---|---:|---:|
| Get pods | Yes | No |
| Get logs | Yes | No |
| Query metrics | Yes | No |
| Check ArgoCD history | Yes | No |
| Restart dev deployment | Maybe | Maybe |
| Restart prod deployment | No | Yes |
| Rollback prod app | No | Yes |
| Delete pod | No | Yes |
| Delete namespace | Never | Yes + strong policy |
| Modify secrets | Never | Yes + strong policy |

---

## 17. Production Observability for the Agent Itself

```mermaid
flowchart LR
    API[Agent API] --> OTEL[OpenTelemetry]
    WORKER[LangGraph Worker] --> OTEL
    MCP[MCP Servers] --> OTEL

    OTEL --> PROM[Prometheus Metrics]
    OTEL --> LOKI[Logs]
    OTEL --> TEMPO[Traces]
    PROM --> GRAFANA[Grafana Dashboard]
    LOKI --> GRAFANA
    TEMPO --> GRAFANA
```

Track:

```text
agent_request_count
agent_request_latency
tool_call_count
failed_tool_call_count
approval_pending_count
remediation_success_count
llm_token_usage
llm_cost_per_request
```

---

## 18. Final Teaching Summary

```text
A production agentic system should not be just one chatbot.

It should have:

1. LangGraph for workflow and agent orchestration
2. MCP servers for tool access
3. Kubernetes for deployment and scaling
4. Redis/Postgres for state and checkpointing
5. Human approval for risky actions
6. Observability for the agent itself
7. Strong RBAC and network security
```

---

## 19. One-Line Architecture

```text
User asks a production question → LangGraph plans and coordinates agents → MCP tools collect real system data → Reviewer validates → Human approves → Remediation executes safely on Kubernetes.
```

---

## 20. Best Practices for Students

```text
Start simple:
  One FastAPI app + one LangGraph workflow + one MCP server

Then grow:
  Add more MCP servers
  Add Redis/Postgres checkpointing
  Add approval workflow
  Add observability
  Deploy to Kubernetes
  Add security policies
```

