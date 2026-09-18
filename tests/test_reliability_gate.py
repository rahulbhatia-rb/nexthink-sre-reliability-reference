import unittest
from src.reliability_gate import ServiceSignals, release_decision

class GateTests(unittest.TestCase):
 def s(self,**k):
  d=dict(availability=.9999,p95_latency_ms=120,error_budget_remaining=.8,canary_error_rate=.001);d.update(k);return ServiceSignals(**d)
 def test_promotes_healthy_canary(self): self.assertEqual(release_decision(self.s()),("promote",()))
 def test_holds_when_budget_low(self): self.assertEqual(release_decision(self.s(error_budget_remaining=.1))[0],"hold")
 def test_rolls_back_bad_canary(self): self.assertEqual(release_decision(self.s(canary_error_rate=.02))[0],"rollback")
