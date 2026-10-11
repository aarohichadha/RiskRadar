"""Distinct live publishers. Metadata only, with source URLs and timestamps."""
import urllib.request,xml.etree.ElementTree as ET,re,html,time,threading
SOURCES={'bbc':'https://feeds.bbci.co.uk/news/business/rss.xml','guardian':'https://www.theguardian.com/business/rss','sec':'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&count=20&output=atom'}
_cache={};_lock=threading.Lock()
def strip_markup(text):return html.unescape(re.sub(r'<[^>]+>',' ',text or '')).strip()
def ingest(source,contact=''):
 if source not in SOURCES:raise ValueError('source must be bbc, guardian or sec')
 if source=='sec' and '@' not in contact:raise ValueError('SEC requires SEC_CONTACT_EMAIL with a real contact email')
 with _lock:
  cached=_cache.get(source)
  if cached and time.monotonic()-cached[0]<60:return cached[1]
 req=urllib.request.Request(SOURCES[source],headers={'User-Agent':f'RiskRadar educational prototype {contact or "RSS reader"}'})
 with urllib.request.urlopen(req,timeout=15) as response:data=response.read(2000000)
 root=ET.fromstring(data);ns={'a':'http://www.w3.org/2005/Atom'};rows=[]
 if source!='sec':
  for item in root.findall('./channel/item')[:20]:rows.append({'text':strip_markup(item.findtext('title','')+' '+item.findtext('description',''))[:20000],'source':source+'-business-rss','url':item.findtext('link',''),'published_at':item.findtext('pubDate',''),'synthetic':False})
 else:
  for item in root.findall('a:entry',ns)[:20]:
   link=item.find('a:link',ns);rows.append({'text':strip_markup(item.findtext('a:title','',ns)+' '+item.findtext('a:summary','',ns))[:20000],'source':'sec-edgar-atom','url':link.get('href','') if link is not None else '', 'published_at':item.findtext('a:updated','',ns),'synthetic':False})
 with _lock:_cache[source]=(time.monotonic(),rows)
 return rows
