# Nexthink SRE Reliability Reference

Application reference for Nexthink's Senior SRE role. It describes a production control loop for multi-tenant AWS/Kubernetes services: define SLOs, measure error-budget burn, block unsafe delivery, and make incident recovery auditable.

## Operating contract

```text
Telemetry → SLI/SLO evaluation → error-budget policy → canary/rollback decision → incident record
```

The key engineering rule is that delivery speed is conditional on reliability: a release can progress only while latency, availability, and error-budget signals remain inside policy. When they do not, the platform freezes promotion, captures the relevant telemetry, and routes recovery through a tested runbook.

This maps to the role's AWS, Terraform, Kubernetes, CI/CD, Datadog, incident-command and multi-tenant SaaS requirements without claiming access to Nexthink infrastructure.

## Candidate links

- https://www.linkedin.com/in/rahul-h-bhatia/
- https://rahulhbhatia.vercel.app
- https://www.credly.com/users/rahul-h-bhatia/badges
