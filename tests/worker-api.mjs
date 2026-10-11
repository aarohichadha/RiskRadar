import assert from 'node:assert/strict';import worker from '../dist/server/index.js';
const origin='https://aarohichadha.github.io';
let r=await worker.fetch(new Request('https://test/api/health'));assert.equal((await r.json()).status,'ok');
r=await worker.fetch(new Request('https://test/api/analyze',{method:'POST',headers:{Origin:origin},body:JSON.stringify({text:'Company reports strong profit growth and record revenue',company:'AAPL'})}));const s=(await r.json())[0];assert.ok(s.sentiment_score>0);assert.equal(r.headers.get('access-control-allow-origin'),origin);
r=await worker.fetch(new Request('https://test/model.json.gz'));assert.ok((await r.arrayBuffer()).byteLength>1000);
r=await worker.fetch(new Request('https://test/api/ingest',{method:'POST',body:JSON.stringify({source:'invalid'})}));assert.equal(r.status,400);
console.log('Worker health, learned sentiment, model asset, CORS and invalid source checks pass');
