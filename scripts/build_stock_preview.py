#!/usr/bin/env python3
"""Build a silent captioned preview from reviewed local stock footage.

Only accepted, manually inspected clips may enter the timeline. API access is not
needed here. Timing estimates narration at 140 words/minute, not audio alignment.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / 'channels/gestern-gabs-das/videos/001-nachnamen-berufe'
FPS = 30
OVERLAP = 6
EXCLUDE = {'pexels-6459913.mp4', 'pexels-4440945.mp4'}


def caption_lines(words):
    text = ' '.join(words)
    if len(text) <= 52:
        return text
    options = []
    for i in range(1, len(words)):
        left, right = ' '.join(words[:i]), ' '.join(words[i:])
        if max(len(left), len(right)) <= 52:
            options.append((abs(len(left)-len(right)), left+'\n'+right))
    return min(options)[1] if options else None


def split_caption(text):
    words = text.split()
    chunks = []
    while words:
        size = min(11, len(words))
        while size > 1 and caption_lines(words[:size]) is None:
            size -= 1
        block = words[:size]
        caption = caption_lines(block)
        if caption is None:
            raise ValueError('Single token too wide: '+block[0])
        chunks.append((caption, len(block)))
        words = words[size:]
    return chunks


def section_key(section):
    lower = section.lower()
    if 'müller' in lower:
        return 'mueller'
    if 'schmidt' in lower:
        return 'schmidt'
    if 'schneider' in lower or 'schröder' in lower:
        return 'schneider'
    if 'fischer' in lower:
        return 'fischer'
    return 'hook'


def build():
    paragraphs = json.loads((VIDEO/'script-preview.json').read_text(encoding='utf-8-sig'))
    reviewed = json.loads((VIDEO/'footage-review.json').read_text(encoding='utf-8-sig'))['clips']
    pools = {}
    for clip in reviewed:
        if clip['accepted'] and clip['filename'] not in EXCLUDE:
            pools.setdefault(clip['section'], []).append(clip)
    # Intro is a purposeful montage of the four crafts, with an alley establishing shot.
    intro = [pools['schmidt'][0], pools['mueller'][0], pools['schneider'][0], pools['fischer'][0], *pools['hook']]
    counters, uses = Counter(), Counter()
    scenes, plan, cursor = [], [], 0
    labels = {'mueller':('MÜLLER','Vom Korn zum Mehl'), 'schmidt':('SCHMIDT','Das Handwerk am Feuer'), 'schneider':('SCHNEIDER / SCHRÖDER','Ein Name aus dem Handwerk'), 'fischer':('FISCHER','Am Meer und im Binnenland')}
    seen = set()
    for p in paragraphs:
        key = section_key(p['section'])
        section_choices = (pools['mueller'] if p['id'] == 'p001' else intro) if key == 'hook' else pools[key]
        for chunk_index, (caption, wordcount) in enumerate(split_caption(p['text'])):
            choices = pools['barrels'] if p['id'] == 'p011' and chunk_index in (0, 2) else section_choices
            effective_frames = max(90, round(wordcount * 60/140 * FPS))
            duration_frames = effective_frames + OVERLAP
            clip = choices[counters[key] % len(choices)]
            counters[key] += 1
            if scenes and scenes[-1]['src'].endswith(clip['filename']):
                clip = choices[counters[key] % len(choices)]
                counters[key] += 1
            windows = clip['usable_trim_windows_s']
            use_index = uses[clip['filename']]
            window = windows[use_index % len(windows)]
            start = float(window[0])
            if duration_frames/FPS > float(window[1])-start + 0.01:
                raise ValueError(f"Trim exceeds reviewed window: {clip['filename']}")
            if start + duration_frames/FPS > clip['duration']:
                raise ValueError('Trim exceeds media length')
            uses[clip['filename']] += 1
            scene = {'id':f'preview-{len(scenes)+1:03}', 'type':'clip', 'duration_s':round(duration_frames/FPS, 6), 'src':'assets/footage/'+clip['filename'], 'trim_start_s':start, 'playback_rate':1, 'grade':'warm', 'caption':caption, 'text_anchor':caption.replace('\n',' ')}
            if key != 'hook' and key not in seen:
                scene['label'] = {'title':labels[key][0], 'subtitle':labels[key][1]}
                seen.add(key)
            if len(scenes) == 0:
                scene['headline'] = 'Dein Name.\nEin altes Handwerk.'
            if 30 <= cursor/FPS < 62 and ('Abonnier' in caption or 'Erinnerungen' in caption):
                scene['cta'] = 'Abonnieren · ein neues Stück Gestern'
            # A tiny engraving inset is optional emphasis, never the video's backbone.
            if key in labels and counters[key] == 6:
                image = {'mueller':'mueller.jpg','schmidt':'schmied.jpg','schneider':'schneider.jpg','fischer':'fischer.jpg'}[key]
                scene['inset'] = {'src':'assets/'+image, 'caption':'Berufsbild im Ständebuch, 1568 · gemeinfrei'}
            scenes.append(scene)
            plan.append({**scene, 'paragraph_id':p['id'], 'section':p['section'], 'source_type':'stock_video', 'source':clip['source_url'], 'author':clip['author'], 'license':clip['license'], 'claim_sources':p['sourceIds'], 'start_s':round(cursor/FPS,3), 'motion':'Original footage at normal speed; 6-frame crossfade', 'illustrative_current_footage':True, 'needs_synthetic_disclosure':False})
            cursor += effective_frames
    # The last shot has no successor to crossfade into.
    scenes[-1]['duration_s'] = round(scenes[-1]['duration_s'] - OVERLAP/FPS,6)
    plan[-1]['duration_s'] = scenes[-1]['duration_s']
    duration = cursor/FPS
    if not 180 <= duration <= 300:
        raise ValueError(f'Preview must be 3–5 minutes, got {duration:.2f}s')
    data = {'fps':FPS,'transition_frames':OVERLAP,'silent_preview':True,'timing_basis':'140 words/minute; no audio alignment','duration_s':duration,'scenes':scenes}
    (VIDEO/'scenes.stock-preview.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (VIDEO/'scenes.stock-plan.json').write_text(json.dumps({'scope':'first-four-name silent stock preview','duration_s':duration,'scenes':plan},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary = {'duration_s':duration,'shots':len(scenes),'unique_clips':len(uses),'motion_footage_share':1,'silent':True,'clip_uses':dict(uses),'reused_windows':sum(max(0,n-len(next(c for c in reviewed if c['filename']==f)['usable_trim_windows_s'])) for f,n in uses.items()),'captions':'max 2 lines × 52 characters; 47px at1080p','limitations':['Estimated narration timing; no audio yet.','Some source windows recur; review rhythm before extending to25minutes.','Current stock illustrates craft; it is not historical German location evidence.']}
    (VIDEO/'preview-manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    build()
