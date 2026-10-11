import unittest,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import RiskEngine,stress,rebalance,ROOT
class EngineTests(unittest.TestCase):
 def setUp(self):self.e=RiskEngine();self.p=json.loads((ROOT/'data/portfolio.json').read_text())
 def test_sentiment_direction(self):
  self.assertGreater(self.e.analyze({'text':'strong profit growth record revenue'})['sentiment_score'],0)
  self.assertLess(self.e.analyze({'text':'default bankruptcy losses'})['sentiment_score'],0)
 def test_unknown_text(self):self.assertEqual(self.e.analyze({'text':'zzzz qqqq'})['impact_score'],1)
 def test_bounds(self):
  for r in json.loads((ROOT/'data/replay.json').read_text()):
   s=self.e.analyze(r);self.assertTrue(-1<=s['sentiment_score']<=1);self.assertTrue(1<=s['impact_score']<=10)
 def test_stress_arithmetic(self):
  s={'impact_score':10,'event_classification':'Geopolitical'};r=stress(s,self.p)
  self.assertEqual(r['before'],10000000);self.assertAlmostEqual(r['loss'],1020000);self.assertAlmostEqual(r['after'],8980000)
 def test_strict_threshold(self):self.assertFalse(stress({'impact_score':7,'event_classification':'Geopolitical'},self.p)['triggered'])
 def test_no_compounding(self):
  s={'impact_score':10,'event_classification':'Geopolitical'};self.assertEqual(stress(s,self.p),stress(s,self.p));self.assertEqual(self.p[0]['value'],4000000)
 def test_weights(self):
  w=rebalance([{'company':'AAPL','sentiment_score':1}]);self.assertAlmostEqual(sum(x['weight'] for x in w),1);self.assertGreater(w[0]['weight'],.1)
 def test_latest_signal(self):self.assertLess(rebalance([{'company':'AAPL','sentiment_score':1},{'company':'AAPL','sentiment_score':-1}])[0]['weight'],.1)
 def test_invalid(self):
  with self.assertRaises(ValueError):self.e.analyze({'text':''})
  with self.assertRaises(ValueError):stress({'impact_score':8,'event_classification':'Other'},self.p,multiplier=4)
if __name__=='__main__':unittest.main()
