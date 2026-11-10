#!/usr/bin/env python3
"""Produce genuine H.264 MP4 camera-motion clips from freely licensed photographs.
These are animated photographs, not original underwater animal video.
Source: RECORDS in oceano-inmersivo-3d.html.
"""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / "oceano-inmersivo-3d.html").read_text()
m = re.search(r"const RECORDS=(\[[\s\S]*?\]);\nconst ", html)
if not m: raise RuntimeError("RECORDS missing")
records = json.loads(m.group(1))
names = {
    0:"angel-cortes",1:"pastos-marinos",2:"mobulas",3:"lobo-marino",
    4:"morena-panamica",5:"coral-cabo-pulmo",6:"pez-mariposa",7:"cousteau-historico"
}
out_dir = root / "media" / "documental"
out_dir.mkdir(parents=True, exist_ok=True)

def grab(url, dest):
    req=urllib.request.Request(url,headers={
       "User-Agent":"ExplorandumEducationalMedia/1.0 (project media asset attribution; contact via GitHub prepdiplo-web/Explorandum)",
       "Accept":"image/avif,image/webp,image/jpeg,*/*"})
    with urllib.request.urlopen(req, timeout=80) as response:
        data=response.read()
    if len(data)<4000 or data[:4] == b"<htm": raise ValueError(f"bad image response {len(data)} bytes")
    dest.write_bytes(data)

for idx,name in names.items():
    rec=records[idx]
    img=out_dir / (name+".jpg")
    video=out_dir / (name+".mp4")
    url=rec["photo"]
    if idx==7:
        # Higher-resolution NASA portrait of Jacques Cousteau, public archival image.
        url="https://commons.wikimedia.org/wiki/Special:Redirect/file/Jacques%20Cousteau%20(16654493311).jpg?width=1280"
    print("DOWNLOAD",idx,name,url,flush=True)
    ok=False
    for attempt in range(3):
        try:
            grab(url,img)
            ok=True
            break
        except Exception as e:
            print("Attempt",attempt+1,"failed",str(e),flush=True)
            time.sleep(4*(attempt+1))
    if not ok: raise RuntimeError("Could not download "+name)
    print("RENDER", name,flush=True)
    # 7.5 s of subtle cinematic forward camera movement, actual MP4, no faux wildlife movement.
    filter_graph="scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(zoom+0.00050,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=960x540:fps=24,format=yuv420p"
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(img),"-vf",filter_graph,
         "-frames:v","180","-c:v","libx264","-preset","veryfast","-crf","22",
         "-movflags","+faststart","-an",str(video)]
    subprocess.run(cmd,check=True,timeout=240)
    if video.stat().st_size < 15000: raise RuntimeError("Broken output: "+str(video))
    print("READY",name,video.stat().st_size,flush=True)
    img.unlink()
print("ALL CLIPS READY",len(names),flush=True)
