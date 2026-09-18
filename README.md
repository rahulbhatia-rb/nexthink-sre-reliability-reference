# Nexthink SRE Reliability Reference

Application reference for Nexthink's Senior SRE role. It describes a production control loop for multi-tenant AWS/Kubernetes services: define SLOs, measure error-budget burn, block unsafe delivery, and make incident recovery auditable.

## What this project demonstrates

This repository is intentionally small enough to review in a few minutes, but it models a real release-safety boundary. A deployment controller should not promote a canary merely because CI is green; it must also decide whether the live service is healthy enough to accept more risk.

The implementation accepts four signals:

| Signal | Why it matters | Gate behaviour |
| --- | --- | --- |
| Availability | Protects the user-facing service objective | Below 99.9% holds promotion |
| p95 latency | Detects performance regressions hidden by a simple health check | Above 500 ms holds promotion |
| Remaining error budget | Preserves reliability capacity for customers | Below 20% holds promotion |
| Canary error rate | Detects a release-specific regression early | Above 1% rolls the canary back |

The outcome is deliberately explicit:

- `promote`: all signals are inside policy.
- `hold`: service health or error budget requires investigation before increasing exposure.
- `rollback`: the canary itself is unhealthy, so the safe action is to stop and revert it.

## Operating contract

```text
Telemetry → SLI/SLO evaluation → error-budget policy → canary/rollback decision → incident record
```

The key engineering rule is that delivery speed is conditional on reliability: a release can progress only while latency, availability, and error-budget signals remain inside policy. When they do not, the platform freezes promotion, captures the relevant telemetry, and routes recovery through a tested runbook.

This maps to the role's AWS, Terraform, Kubernetes, CI/CD, Datadog, incident-command and multi-tenant SaaS requirements without claiming access to Nexthink infrastructure.

## Working component

`src/reliability_gate.py` implements the decision point: healthy signals **promote** a canary, an SLO or error-budget concern **holds** promotion, and an elevated canary error rate **rolls back**. `tests/test_reliability_gate.py` validates all three paths.

```bash
python3 -m unittest discover -s tests -v
```

## How this would run in production

1. A deployment pipeline creates or updates a small canary in Kubernetes.
2. An adapter collects availability, p95 latency, and error signals from Datadog or Prometheus, and reads the remaining error budget from the service SLO definition.
3. The adapter passes those values into `release_decision` and writes the decision, build identifier, and metrics snapshot to the change record.
4. `promote` advances the rollout; `hold` freezes it and creates an operator task; `rollback` reverts the immutable release and links the event to incident response.
5. Terraform and GitOps define the infrastructure and deployment policy, while this component keeps the decision logic independently testable.

## Boundaries and assumptions

The thresholds in this sample are illustrative and must be calibrated to each service's contractual SLOs. The project does not call Nexthink systems or claim access to any customer or production infrastructure. Its purpose is to show a practical approach to the role's AWS, Kubernetes, Terraform, CI/CD, observability, incident-command, and SaaS reliability requirements.

## Candidate links

- https://www.linkedin.com/in/rahul-h-bhatia/
- https://rahulhbhatia.vercel.app
- https://www.credly.com/users/rahul-h-bhatia/badges
