"""Portable inference from exported TF-IDF and logistic regression weights."""
import re,math,json,gzip
from collections import Counter
from pathlib import Path
MODEL_PATH=Path(__file__).parent/'data/model.json.gz'
def tokens(text):return re.findall(r'[a-z]+',re.sub(r'https?://\S+',' ',text.lower()))
class SentimentModel:
 def __init__(self):self.artifact=json.loads(gzip.decompress(MODEL_PATH.read_bytes()));self.vocabulary=self.artifact['vocabulary']
 def predict(self,text):
  ts=tokens(text);features=Counter(ts+[a+' '+b for a,b in zip(ts,ts[1:])]);weighted={self.vocabulary[k]:(1+math.log(v))*self.artifact['idf'][self.vocabulary[k]] for k,v in features.items() if k in self.vocabulary}
  norm=math.sqrt(sum(v*v for v in weighted.values())) or 1
  scores=[bias+sum(coef[i]*v/norm for i,v in weighted.items()) for bias,coef in zip(self.artifact['intercepts'],self.artifact['coefficients'])]
  m=max(scores);exp=[math.exp(v-m) for v in scores];total=sum(exp)
  return {label:v/total for label,v in zip(self.artifact['classes'],exp)},len(weighted)
