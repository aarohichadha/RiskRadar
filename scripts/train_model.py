"""Train and export a reproducible financial sentiment model. No raw tweets redistributed."""
import argparse,csv,json,hashlib,re,urllib.request,gzip
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,f1_score
ROOT=Path(__file__).resolve().parents[1]
REVISION='ccbe24de388e287beb92dd393a335c376b350ac3'
BASE=f'https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment/resolve/{REVISION}/'
LABELS={'0':'negative','1':'positive','2':'neutral'}
def tokenize(text):
 text=re.sub(r'https?://\S+',' ',text.lower())
 return re.findall(r'[a-z]+',text)
def canonical(text):return ' '.join(tokenize(text))
def download(cache):
 cache.mkdir(parents=True,exist_ok=True)
 for name in ['sent_train.csv','sent_valid.csv','README.md']:
  p=cache/name
  if not p.exists():p.write_bytes(urllib.request.urlopen(BASE+name,timeout=30).read())
def read(path):return [{'text':r['text'],'label':LABELS[r['label']]} for r in csv.DictReader(path.open(encoding='utf-8'))]
def clean(rows):
 by=defaultdict(list)
 for r in rows:by[canonical(r['text'])].append(r)
 conflicts=sum(len({r['label'] for r in rs})>1 for rs in by.values())
 out=[rs[0] for k,rs in by.items() if k and len({r['label'] for r in rs})==1]
 return out,conflicts
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--cache',type=Path,default=ROOT/'.data-cache');args=parser.parse_args();download(args.cache)
 raw_train=read(args.cache/'sent_train.csv');raw_test=read(args.cache/'sent_valid.csv')
 train,train_conflicts=clean(raw_train);test,test_conflicts=clean(raw_test)
 trainkeys={canonical(r['text']) for r in train};overlap=sum(canonical(r['text']) in trainkeys for r in test);test=[r for r in test if canonical(r['text']) not in trainkeys]
 # Fixed settings. The publisher's validation split is evaluation-only, never fitted or tuned here.
 vectorizer=TfidfVectorizer(tokenizer=tokenize,token_pattern=None,lowercase=False,ngram_range=(1,2),min_df=2,max_features=16000,sublinear_tf=True)
 X=vectorizer.fit_transform([r['text'] for r in train]);y=[r['label'] for r in train]
 model=LogisticRegression(C=4,class_weight='balanced',max_iter=1000,random_state=42);model.fit(X,y)
 Xt=vectorizer.transform([r['text'] for r in test]);yt=[r['label'] for r in test];pred=model.predict(Xt)
 labels=list(model.classes_)
 report={'dataset':'zeroshot/twitter-financial-news-sentiment','revision':REVISION,'license':'MIT (publisher dataset card)','source':BASE,'raw_train_count':len(raw_train),'raw_validation_count':len(raw_test),'train_count':len(train),'evaluation_count':len(test),'conflicting_train_groups_removed':train_conflicts,'conflicting_evaluation_groups_removed':test_conflicts,'evaluation_overlap_removed':overlap,'train_labels':dict(Counter(y)),'evaluation_labels':dict(Counter(yt)),'accuracy':float(accuracy_score(yt,pred)),'macro_f1':float(f1_score(yt,pred,average='macro')),'classification_report':classification_report(yt,pred,output_dict=True,zero_division=0),'confusion_matrix':confusion_matrix(yt,pred,labels=labels).tolist(),'confusion_matrix_labels':labels,'method':'TF-IDF unigrams/bigrams + balanced multinomial logistic regression','hyperparameters':{'C':4,'min_df':2,'max_features':16000,'ngram_range':[1,2]},'evaluation_design':'Publisher validation split, canonical exact-text deduplication, conflicts removed and train/evaluation overlap removed. No tuning on evaluation split. Not a temporal or entity-disjoint evaluation.','source_sha256':{n:hashlib.sha256((args.cache/n).read_bytes()).hexdigest() for n in ['sent_train.csv','sent_valid.csv']}}
 artifact={'version':2,'model':'TF-IDF + logistic regression','classes':labels,'vocabulary':{k:int(v) for k,v in vectorizer.vocabulary_.items()},'idf':vectorizer.idf_.round(7).tolist(),'coefficients':model.coef_.round(7).tolist(),'intercepts':model.intercept_.round(7).tolist(),'metadata':report}
 for folder in ['data','dist']:(ROOT/folder/'model.json.gz').write_bytes(gzip.compress(json.dumps(artifact,separators=(',',':')).encode(),mtime=0))
 (ROOT/'data/evaluation.json').write_text(json.dumps(report,indent=2));(ROOT/'dist/evaluation.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({k:report[k] for k in ['train_count','evaluation_count','accuracy','macro_f1','evaluation_overlap_removed']},indent=2))
