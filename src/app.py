import json, sys
from src.reliability_gate import ServiceSignals, release_decision
for line in sys.stdin:
    if line.strip():
        payload=json.loads(line); decision,reasons=release_decision(ServiceSignals(**payload))
        print(json.dumps({"input":payload,"decision":decision,"reasons":reasons}))
