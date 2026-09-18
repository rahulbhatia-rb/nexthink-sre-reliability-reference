"""SLO-aware deployment gate for a multi-tenant SaaS service."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ServiceSignals:
    availability: float
    p95_latency_ms: int
    error_budget_remaining: float
    canary_error_rate: float

def release_decision(signals: ServiceSignals) -> tuple[str, tuple[str, ...]]:
    """Choose promotion, hold, or rollback from explicit reliability signals."""
    reasons=[]
    if signals.availability < .999: reasons.append("availability-slo-breached")
    if signals.p95_latency_ms > 500: reasons.append("latency-slo-breached")
    if signals.error_budget_remaining < .20: reasons.append("error-budget-low")
    if signals.canary_error_rate > .01: reasons.append("canary-error-rate-high")
    if "canary-error-rate-high" in reasons: return "rollback",tuple(reasons)
    return ("hold" if reasons else "promote"),tuple(reasons)
