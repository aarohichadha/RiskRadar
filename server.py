"""Dependency-free local server with SQLite persistence and JSON API."""
import json,sqlite3,os, argparse, threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from engine import RiskEngine,stress,rebalance,ROOT
from connectors import ingest
engine=RiskEngine();DB=ROOT/'runtime.sqlite3'; lock=threading.Lock()
def save(rows):
 with lock,sqlite3.connect(DB) as db:
  db.execute('CREATE TABLE IF NOT EXISTS signals(id TEXT PRIMARY KEY,payload TEXT)')
  for s in rows:db.execute('INSERT OR REPLACE INTO signals VALUES (?,?)',(s['signal_id'],json.dumps(s)))
def history():
 with lock,sqlite3.connect(DB) as db:return [json.loads(r[0]) for r in db.execute('SELECT payload FROM signals ORDER BY rowid DESC LIMIT 500')]
save([])
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'dist'),**kw)
 def reply(self,body,status=200):
  data=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/api/health':return self.reply({'status':'ok'})
  if self.path=='/api/signals':return self.reply(history())
  return super().do_GET()
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length',0))
   if n>2000000:return self.reply({'error':'payload too large'},413)
   body=json.loads(self.rfile.read(n))
   if self.path=='/api/analyze':
    rows=body.get('rows',[body]);signals=[engine.analyze(r) for r in rows];save(signals);return self.reply(signals)
   if self.path=='/api/ingest':
    rows=ingest(body['source'],os.getenv('SEC_CONTACT_EMAIL',''));signals=[engine.analyze(r) for r in rows];save(signals);return self.reply(signals)
   if self.path=='/api/stress':return self.reply(stress(body['signal'],body.get('portfolio',json.loads((ROOT/'data/portfolio.json').read_text())),body.get('threshold',7),body.get('multiplier',1)))
   if self.path=='/api/rebalance':return self.reply(rebalance(body.get('signals',history()[::-1])))
   return self.reply({'error':'unknown endpoint'},404)
  except (ValueError,KeyError,TypeError) as e:self.reply({'error':str(e)},400)
  except Exception as e:self.reply({'error':'Operation failed. Check source availability and server logs.'},502)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);args=parser.parse_args();print(f'RiskRadar http://localhost:{args.port}',flush=True);ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
