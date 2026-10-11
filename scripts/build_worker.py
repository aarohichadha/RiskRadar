"""Bundle an ESM Worker and essential assets into a single deployment module."""
import json,base64
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
assets={}
for name in ['index.html','app.js','engine.js','model.json.gz','portfolio.json','replay.json','evaluation.json']:
 p=ROOT/'dist'/name;binary=name.endswith('.gz');mime='application/octet-stream' if binary else 'text/html; charset=utf-8' if name.endswith('.html') else 'text/javascript; charset=utf-8' if name.endswith('.js') else 'application/json'
 assets['/'+name]={'body':base64.b64encode(p.read_bytes()).decode() if binary else p.read_text(),'encoding':'base64' if binary else 'text','type':mime}
engine=(ROOT/'dist/engine.js').read_text().replace('export const ','const ').replace('export function ','function ')
code='const STATIC_ASSETS='+json.dumps(assets,separators=(',',':'))+';\n'+engine+'\n'+(ROOT/'worker/api.js').read_text()
p=ROOT/'dist/server/index.js';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
manifest_path=ROOT/'.openai/hosting.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
manifest.pop('static',None)
(ROOT/'dist/.openai').mkdir(exist_ok=True);(ROOT/'dist/.openai/hosting.json').write_text(json.dumps(manifest,indent=2))
print('Bundled Worker:',len(code),'bytes')
