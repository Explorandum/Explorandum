#!/usr/bin/env python3
"""Create authentic short clips from legally reusable NOAA and CC0 research video.
NOAA deep-sea octopuses (public domain) and Alopias pelagicus (CC0).
Do not interpolate still images. Output is independently reviewed before use.
"""
import pathlib,urllib.request,urllib.parse,json,subprocess
import imageio_ffmpeg
ROOT=pathlib.Path(__file__).resolve().parents[1];DEST=ROOT/"media"/"real";DEST.mkdir(parents=True,exist_ok=True)
CLIPS=[
{"filename":"Pelagic thresher shark (Alopias pelagicus).webm","out":"tiburon-zorro-real.mp4","start":4,"length":14},
{"filename":"Wk215-deep-sea-octopuses.webm","out":"pulpos-profundidad-noaa.mp4","start":8,"length":19},
]
UA={"User-Agent":"ExplorandumVideoResearch/1.0 (github.com/prepdiplo-web/Explorandum)"}
for item in CLIPS:
  api="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":"File:"+item["filename"],"prop":"imageinfo","iiprop":"url|size","format":"json"})
  with urllib.request.urlopen(urllib.request.Request(api,headers=UA),timeout=35) as resp:data=json.load(resp)
  imageinfo=next(iter(data["query"]["pages"].values()))["imageinfo"][0]
  if imageinfo["size"]>25000000:raise Exception("Source unexpectedly large")
  tmp=DEST/(item["out"]+".source.webm")
  with urllib.request.urlopen(urllib.request.Request(imageinfo["url"],headers=UA),timeout=90) as resp,open(tmp,"wb") as out:
    while True:
      chunk=resp.read(1024*1024)
      if not chunk:break
      out.write(chunk)
  out=DEST/item["out"]
  cmd=[imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","error","-y","-ss",str(item["start"]),"-i",str(tmp),"-t",str(item["length"]),"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1","-an","-c:v","libx264","-preset","fast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
  subprocess.run(cmd,check=True,timeout=160)
  tmp.unlink()
  if out.stat().st_size<150000:raise Exception("Video invalid")
  print("REAL_CLIP_READY",out.name,out.stat().st_size,flush=True)
