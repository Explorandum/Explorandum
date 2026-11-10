#!/usr/bin/env python3
"""Authentic kelp forest video by Taryn Elliott, Pexels 5548030, Pexels Content License.
https://www.pexels.com/video/colorful-fish-swimming-among-seaweed-5548030/
"""
import urllib.request,subprocess,pathlib,imageio_ffmpeg
DEST=pathlib.Path(__file__).resolve().parents[1]/"media"/"real";DEST.mkdir(parents=True,exist_ok=True)
base="https://videos.pexels.com/video-files/5548030/"
files=["5548030-hd_1920_1080_25fps.mp4","5548030-hd_1280_720_25fps.mp4","5548030-uhd_3840_2160_25fps.mp4"]
source=None
for file in files:
    try:
        with urllib.request.urlopen(urllib.request.Request(base+file,headers={"User-Agent":"Mozilla/5.0"},method="HEAD"),timeout=25) as r:
            size=int(r.headers.get("Content-Length","0") or "0")
            if r.status==200 and (not size or size<420000000):
                source=base+file;print("SELECTED",file,size,flush=True);break
    except Exception as e:print("SKIP",file,str(e)[:100],flush=True)
if not source:raise RuntimeError("Kelp original unavailable")
out=DEST/"bosque-algas.mp4"
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","warning","-y","-i",source,"-t","12",
"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
"-an","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True,timeout=350)
if out.stat().st_size<200000:raise RuntimeError("Kelp clip invalid")
print("KELP_READY",out.stat().st_size)
