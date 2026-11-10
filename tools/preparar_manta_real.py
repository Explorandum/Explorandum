#!/usr/bin/env python3
"""Use genuine manta footage, Zlatin Georgiev, Pexels 7555072, Pexels Content License.
Source https://www.pexels.com/video/a-manta-ray-at-the-ocean-7555072/
"""
import urllib.request,subprocess,pathlib,imageio_ffmpeg
dest=pathlib.Path(__file__).resolve().parents[1]/"media"/"real";dest.mkdir(parents=True,exist_ok=True)
base="https://videos.pexels.com/video-files/7555072/7555072-"
opts=["hd_1920_1080_25fps.mp4","hd_1280_720_25fps.mp4","uhd_3840_2160_25fps.mp4"]
src=None
for opt in opts:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+opt,headers={"User-Agent":"Mozilla/5.0"},method="HEAD"),timeout=20) as r:
   size=int(r.headers.get("Content-Length","0") or "0")
   if r.status==200 and (not size or size<150000000):src=base+opt;print("SOURCE",opt,size,flush=True);break
 except Exception as e:print("SKIP",opt,str(e)[:80],flush=True)
if not src:raise RuntimeError("No manta source")
out=dest/"manta-oceanica-real.mp4"
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-loglevel","error","-y","-i",src,"-t","9.5","-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1","-an","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True,timeout=200)
if out.stat().st_size<200000:raise RuntimeError("Short clip")
print("MANTA_READY",out.stat().st_size,flush=True)
