#!/usr/bin/env python3
"""Native FFmpeg fallback for silent stock previews.

Consumes the reviewed scenes.stock-preview.json. Uses short dip cuts
instead of crossfades, preserving effective caption timing. No API calls.
"""
import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT/'channels/gestern-gabs-das/videos/001-nachnamen-berufe'


def font(name,size,bold=False):
    face=ImageFont.truetype(str(ROOT/'.cache/fonts'/name),size)
    if bold and hasattr(face,'set_variation_by_axes') and 'Bitter' in name:
        face.set_variation_by_axes([800])
    return face


def overlay(scene,path):
    image=Image.new('RGBA',(1920,1080))
    draw=ImageDraw.Draw(image)
    regular=font('Lato-Regular.ttf',47)
    small=font('Lato-Regular.ttf',21)
    # Soft shadows help readability without turning craft footage into cards.
    draw.rectangle((0,0,1920,105),fill=(0,0,0,35))
    draw.text((1855,46),'GESTERN GAB’S DAS · SYMBOLBILDER',font=small,anchor='rt',fill='white',stroke_width=1,stroke_fill='#22303c')
    text=scene.get('caption','')
    rows=text.split('\n')
    heights=[draw.textbbox((0,0),r,font=regular)[3]-draw.textbbox((0,0),r,font=regular)[1] for r in rows]
    line_height=61
    block_height=len(rows)*line_height+22
    widths=[draw.textlength(r,font=regular) for r in rows]
    max_width=max(widths,default=0)
    if max_width>1630 or len(rows)>2:
        raise ValueError('Caption exceeds safe area: '+scene['id'])
    top=1080-62-block_height
    draw.rounded_rectangle(((1920-max_width)/2-28,top,(1920+max_width)/2+28,1018),radius=5,fill=(12,19,24,225))
    for i,row in enumerate(rows):
        draw.text((960,top+10+i*line_height),row,font=regular,anchor='mt',fill='white')
    if scene.get('label'):
        titlefont=font('Bitter[wght].ttf',49,True)
        subtitlefont=font('Lato-Regular.ttf',25)
        title=scene['label']['title'];sub=scene['label'].get('subtitle','')
        width=int(draw.textlength(title,font=titlefont))+52
        draw.rectangle((70,50,70+width,125),fill='#22303c')
        draw.text((96,61),title,font=titlefont,fill='#f3ebdd')
        if sub:
            sw=int(draw.textlength(sub,font=subtitlefont))+52
            draw.rectangle((70,125,70+sw,169),fill='#2f6f73')
            draw.text((96,132),sub,font=subtitlefont,fill='white')
    if scene.get('headline'):
        headlinefont=font('Bitter[wght].ttf',105,True)
        draw.multiline_text((115,335),scene['headline'],font=headlinefont,fill='#f3ebdd',spacing=12,stroke_width=2,stroke_fill='#22303c')
    if scene.get('cta'):
        ctafont=font('Lato-Bold.ttf',37)
        text='+ '+scene['cta'];w=int(draw.textlength(text,font=ctafont))+56
        draw.rounded_rectangle((105,680,105+w,755),radius=6,fill='#b24a33')
        draw.text((133,696),text,font=ctafont,fill='white')
    if scene.get('inset'):
        inset=scene['inset']
        art=Image.open(VIDEO/inset['src']).convert('RGB')
        art.thumbnail((332,355))
        card=Image.new('RGBA',(360,440),'#f3ebdd')
        card.alpha_composite(art.convert('RGBA'),((360-art.width)//2,14))
        note=ImageDraw.Draw(card)
        note.text((16,382),'Ständebuch, 1568',font=font('Lato-Regular.ttf',23),fill='#22303c')
        note.text((16,410),'Gemeinfrei',font=font('Lato-Regular.ttf',18),fill='#22303c')
        image.alpha_composite(card,(1480,230))
    image.save(path)


def render(args):
    data=json.loads((VIDEO/'scenes.stock-preview.json').read_text(encoding='utf-8-sig'))
    scenes=data['scenes'][:args.limit] if args.limit else data['scenes']
    fps=data['fps'];overlap=data.get('transition_frames',6)
    outdir=VIDEO/'render/native';outdir.mkdir(parents=True,exist_ok=True)
    binary=args.ffmpeg or os.environ.get('FFMPEG_BINARY') or shutil.which('ffmpeg')
    if not binary:
        npm=ROOT/'pipeline/render/node_modules/ffmpeg-static/ffmpeg.exe'
        if npm.exists():binary=str(npm)
    if not binary:raise SystemExit('FFmpeg not found; set FFMPEG_BINARY or --ffmpeg.')
    jobs=[]
    for i,scene in enumerate(scenes):
        if scene['type']!='clip':raise ValueError('Native backend accepts reviewed clip scenes only.')
        frames=round(scene['duration_s']*fps)-(overlap if i<len(data['scenes'])-1 else 0)
        imagepath=outdir/(scene['id']+'.png')
        overlay(scene,imagepath)
        jobs.append((i,scene,frames,imagepath))
    def one(job):
        i,scene,frames,imagepath=job
        duration=frames/fps;part=outdir/(scene['id']+'.mp4')
        grade='eq=saturation=0.86:contrast=1.05:brightness=-0.018:gamma_r=1.025:gamma_b=0.985'
        graph=f'[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps={fps},{grade},format=yuv420p[base];[base][1:v]overlay=shortest=1,fade=t=in:st=0:d=0.10,fade=t=out:st={duration-0.10:.6f}:d=0.10,format=yuv420p[out]'
        cmd=[binary,'-hide_banner','-loglevel','error','-y','-threads','1','-ss',str(scene.get('trim_start_s',0)),'-i',str(VIDEO/scene['src']),'-loop','1','-i',str(imagepath),'-filter_complex_threads','1','-filter_complex',graph,'-map','[out]','-an','-frames:v',str(frames),'-r',str(fps),'-c:v','libx264','-preset','veryfast','-crf','26','-threads','2','-pix_fmt','yuv420p',str(part)]
        result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        if result.returncode:raise RuntimeError(scene['id']+': '+result.stderr[-2000:])
        return i,part
    parts={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(one,job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            i,path=future.result();parts[i]=path
            if len(parts)%10==0 or len(parts)==len(jobs):print(f'Rendered {len(parts)}/{len(jobs)} moving shots',flush=True)
    concat=outdir/'concat.txt'
    concat.write_text('\n'.join("file '"+parts[i].name+"'" for i in range(len(parts))),encoding='utf-8')
    output=Path(args.out).resolve() if args.out else VIDEO/'render/preview-stock-1080p.mp4'
    output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([binary,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(output)],check=True)
    subprocess.run([binary,'-hide_banner','-loglevel','error','-i',str(output),'-f','null','-'],check=True)
    log={'renderer':'native FFmpeg fallback','reason':'Remotion bundled Windows compositor access violation3221225477; Html5Video test succeeded but frame seeking too slow for full preview','resolution':'1920x1080','fps':fps,'audio_streams':0,'codec':'h264','crf':26,'transition':'0.10s dip on each side of cuts (not Remotion crossfade)','duration_s':sum(job[2] for job in jobs)/fps,'shots':len(jobs),'bytes':output.stat().st_size,'file':output.name,'checks':['full FFmpeg decode completed','caption safe width checked at actual font size','no audio stream mapped'],'limitations':['Static labels and engraving PiP over moving footage; no label spring animation in this backend.','Caption timing estimated from word counts; final voiceover alignment pending.']}
    (VIDEO/'render/render-report.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(log),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg');parser.add_argument('--out');parser.add_argument('--workers',type=int,default=3);parser.add_argument('--limit',type=int)
    render(parser.parse_args())
