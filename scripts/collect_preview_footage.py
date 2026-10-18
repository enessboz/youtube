import sys, os, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pipeline'/'footage'))
import footage
env_candidates=[Path(os.environ['PEXELS_ENV_FILE'])] if os.environ.get('PEXELS_ENV_FILE') else [ROOT/'.env', ROOT.parents[1]/'.env']
if not os.environ.get('PEXELS_API_KEY'):
 for ENV in env_candidates:
  if not ENV.exists():continue
  for line in ENV.read_text(encoding='utf-8-sig').splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1)
        if k.strip()=='PEXELS_API_KEY': os.environ[k.strip()]=v.strip().strip('\"').strip("'")
  if os.environ.get('PEXELS_API_KEY'):break
os.environ.pop('PIXABAY_API_KEY',None)
D=ROOT/'channels/gestern-gabs-das/videos/001-nachnamen-berufe'
queries={'mueller':['flour mill','water wheel','grain harvest'], 'schmidt':['blacksmith forging','hammer anvil'], 'schneider':['tailor cutting fabric','sewing machine'], 'fischer':['fisherman net','fishing boat'], 'hook':['old village street']}
# Cache API search results to avoid spending quota on repeated collection runs.
cache=D/'footage-search-results.json'
if cache.exists():
    results=json.loads(cache.read_text(encoding='utf-8'))
else:
    results={}
    for sec,qs in queries.items():
        results[sec]=[]
        for q in qs:
            rr=footage.search(q,n=6,min_duration=6)
            results[sec].append({'query':q,'results':rr})
            print(sec,q,len(rr),'candidates',flush=True)
    cache.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
# DOWNLOAD_SELECTED
if __name__=='__main__':
 import subprocess
 from concurrent.futures import ThreadPoolExecutor
 dest=D/'assets/footage'; dest.mkdir(parents=True,exist_ok=True)
 chosen={'mueller':[35794910,19675231,19675240,855416,19740011,13125056], 'schmidt':[31638148,5846397,5846389,4186969,38104095], 'schneider':[4621701,6765465,6459918,6459913,6460113], 'fischer':[4440938,4440945,2652362,10496570,4788511], 'hook':[27987395,34038695], 'barrels':[5537827]}
 ff=os.environ.get('FFMPEG_BINARY') or shutil.which('ffmpeg') or str(ROOT/'pipeline/render/node_modules/ffmpeg-static/ffmpeg.exe')
 def collect(pair):
  sec,vid=pair; path=dest/f'pexels-{vid}.mp4'
  saved_meta=dest/'stock-preview-metadata'/path.with_suffix('.json').name
  if path.exists(): meta=json.loads((saved_meta if saved_meta.exists() else path.with_suffix('.json')).read_text(encoding='utf-8'))
  else: _,meta=footage.download(f'pexels:{vid}',str(dest))
  saved_meta.parent.mkdir(parents=True,exist_ok=True)
  saved_meta.write_text(json.dumps(meta,ensure_ascii=False,indent=1),encoding='utf-8')
  out=dest/f'pexels-{vid}-contact.jpg'
  # Four real frames spaced across the source, grouped into a contact sheet.
  fps=4/max(1,meta['duration']-1)
  subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(path),'-vf',f'fps={fps},scale=480:-1,tile=2x2','-frames:v','1','-y',str(out)],check=True)
  print('downloaded',sec,vid,flush=True)
  return {'section':sec,**meta,'filename':path.name,'contact_sheet':out.name}
 with ThreadPoolExecutor(max_workers=4) as pool:
  selected=list(pool.map(collect,[(s,v) for s,vs in chosen.items() for v in vs]))
 (D/'assets/footage/candidates.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
