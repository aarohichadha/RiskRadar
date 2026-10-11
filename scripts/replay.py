"""Write deterministic machine-readable demonstration outputs."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from engine import RiskEngine,stress,rebalance
engine=RiskEngine();rows=json.loads((ROOT/'data/replay.json').read_text());signals=[engine.analyze(row) for row in rows];portfolio=json.loads((ROOT/'data/portfolio.json').read_text());result={'signals':signals,'stress':stress(signals[2],portfolio),'weights':rebalance(signals)}
(ROOT/'data/demo-results.json').write_text(json.dumps(result,indent=2));print('Wrote data/demo-results.json')
