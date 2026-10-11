"""Transparent prototype NLP engine. Training examples are synthetic, not validation data."""
import re, math, json, hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).parent
CLASSES=['positive','negative','neutral']
RULES={'Geopolitical':['war','sanctions','conflict','geopolitical','invasion'], 'Macroeconomic':['inflation','interest rate','recession','central bank','unemployment'], 'Credit Event':['default','bankruptcy','liquidity','downgrade','debt'], 'Merger/Acquisition':['merger','acquisition','takeover'], 'Product Launch':['product','launch','recall']}
SHOCKS={'Geopolitical':{'equity':-.10,'rates':.02,'spread':.015},'Macroeconomic':{'equity':-.08,'rates':.02,'spread':.005},'Credit Event':{'equity':-.12,'rates':0,'spread':.025},'Merger/Acquisition':{'equity':-.04,'rates':0,'spread':.004},'Product Launch':{'equity':-.03,'rates':0,'spread':.002},'Other':{'equity':-.02,'rates':0,'spread':.001}}
def tokens(text):return re.findall(r'[a-z]+',text.lower())
class RiskEngine:
 def __init__(self):
  from sentiment import SentimentModel
  self.sentiment=SentimentModel()
 def analyze(self,row):
  if not isinstance(row,dict) or not isinstance(row.get('text'),str):raise ValueError('Each record must contain a text string')
  text=row['text'].strip()
  if not text or len(text)>20000:raise ValueError('text must contain 1 to 20000 characters')
  probs,coverage=self.sentiment.predict(text)
  low=text.lower();hits={k:[w for w in ws if re.search(r'\b'+re.escape(w)+r'\b',low)] for k,ws in RULES.items()};event=max(hits,key=lambda k:len(hits[k]));event=event if hits[event] else 'Other'
  severe=[w for w in ['war','default','bankruptcy','crisis','sanctions','recession','fraud'] if re.search(r'\b'+w+r'\b',low)]
  impact=min(10,1+2*len(severe)+len(hits.get(event,[])))
  company=row.get('company') or infer_company(text)
  return dict(row,company=company,signal_id=hashlib.sha256((str(row.get('source','manual'))+'|'+text).encode()).hexdigest()[:16],sentiment_score=round(probs['positive']-probs['negative'],4),sentiment_label=max(probs,key=probs.get),probabilities=probs,event_classification=event,impact_score=impact,evidence={'event_keywords':hits.get(event,[]),'severity_keywords':severe},model='TF-IDF + logistic regression',impact_method='keyword heuristic',confidence_calibrated=False,low_confidence=max(probs.values())<.55,matched_features=coverage)
ALIASES={'AAPL':['apple'],'MSFT':['microsoft'],'NVDA':['nvidia'],'AMZN':['amazon'],'GOOGL':['alphabet','google'],'META':['meta','facebook'],'TSLA':['tesla'],'JPM':['jpmorgan','j.p. morgan'],'V':['visa'],'WMT':['walmart']}
def infer_company(text):
 for ticker,aliases in ALIASES.items():
  if re.search(r'\$'+ticker+r'\b',text,re.I) or any(re.search(r'\b'+re.escape(a)+r'\b',text,re.I) for a in aliases):return ticker
 return 'GLOBAL'
def stress(signal,portfolio,threshold=7,multiplier=1):
 if not 0<=multiplier<=3:raise ValueError('multiplier must be between 0 and 3')
 if not 1<=threshold<=10:raise ValueError('threshold must be between 1 and 10')
 triggered=signal['impact_score']>threshold
 shock={k:v*multiplier for k,v in SHOCKS.get(signal['event_classification'],SHOCKS['Other']).items()} if triggered else dict(equity=0,rates=0,spread=0)
 rows=[]
 for a in portfolio:
  v=float(a['value'])
  if not math.isfinite(v) or v<0:raise ValueError('asset value must be finite and nonnegative')
  change=v*(a.get('equity_beta',0)*shock['equity']-a.get('duration',0)*shock['rates']-a.get('spread_duration',0)*shock['spread'])+a.get('rate_sensitivity',0)*shock['rates']
  rows.append(dict(a,before=v,after=v+change,change=change))
 before=sum(r['before'] for r in rows);after=sum(r['after'] for r in rows)
 return dict(triggered=triggered,threshold=threshold,shock=shock,assets=rows,before=before,after=after,loss=before-after,loss_pct=(before-after)/before*100 if before else 0,assumption='Illustrative adverse scenario, independent of sentiment direction. Derivative sensitivity is currency per unit rate change.')
def rebalance(signals):
 tickers=['AAPL','MSFT','NVDA','AMZN','GOOGL','META','TSLA','JPM','V','WMT'];latest={s.get('company'):s for s in signals};raw={t:1+.5*latest.get(t,{}).get('sentiment_score',0) for t in tickers};z=sum(raw.values())
 return [{'ticker':t,'base_weight':.1,'weight':raw[t]/z,'sentiment':latest.get(t,{}).get('sentiment_score',0)} for t in tickers]
