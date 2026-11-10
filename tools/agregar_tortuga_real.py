#!/usr/bin/env python3
"""Add an authentic underwater turtle video to the EXPLORANDUM preview.
Uses the original clip under CC BY-SA 4.0; no still-photo animation.
"""
import json, pathlib, subprocess, urllib.parse, urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
out=root/"media"/"real"
out.mkdir(parents=True,exist_ok=True)
filename="Swimming with the sea turtle up close in Moalboal Cebu.webm"
api="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":"File:"+filename,"prop":"imageinfo","iiprop":"url|size","format":"json"})
agent={"User-Agent":"ExplorandumMedia/1.0 (github.com/prepdiplo-web/Explorandum)"}
with urllib.request.urlopen(urllib.request.Request(api,headers=agent),timeout=40) as r:
    obj=json.load(r)
page=next(iter(obj["query"]["pages"].values()))
source=page["imageinfo"][0]["url"]
raw=out/"tortuga-marina.input.webm"
with urllib.request.urlopen(urllib.request.Request(source,headers=agent),timeout=60) as response,open(raw,"wb") as f:
    while True:
        chunk=response.read(1024*1024)
        if not chunk: break
        f.write(chunk)
if not (100000<raw.stat().st_size<20*1024*1024):
    raise RuntimeError("unexpected source size")
dst=out/"tortuga-marina.mp4"
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(raw),
               "-t","6.5","-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
               "-an","-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p",
               "-movflags","+faststart",str(dst)],check=True,timeout=180)
raw.unlink()
subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=codec_name,width,height","-of","default=nw=1",str(dst)],check=True)
print("TORTUGA_READY",dst.stat().st_size)
