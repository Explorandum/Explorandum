#!/usr/bin/env python3
"""Create a real HD documentary clip from an actual 4K Pexels humpback whale calf film.
Original: Adrien JACTA, Pexels video 15546563, published 2023, Pexels Content License.
https://www.pexels.com/video/a-humpback-whale-and-her-calf-swimming-in-the-blue-sea-15546563/
No AI or still images.
"""
import urllib.request,urllib.error,subprocess,pathlib,imageio_ffmpeg,time
DEST=pathlib.Path(__file__).resolve().parents[1]/"media"/"real";DEST.mkdir(parents=True,exist_ok=True)
BASE="https://videos.pexels.com/video-files/15546563/"
variants=["15546563-hd_1920_1080_25fps.mp4","15546563-hd_1280_720_25fps.mp4","15546563-uhd_3840_2160_25fps.mp4"]
head={"User-Agent":"Mozilla/5.0 (compatible; EXPLORANDUM nonprofit educational documentary)"}
source=None
for item in variants:
    u=BASE+item
    try:
        req=urllib.request.Request(u,headers=head,method="HEAD")
        with urllib.request.urlopen(req,timeout=25) as response:
            size=int(response.headers.get("Content-Length","0") or "0")
            if response.status==200 and (size==0 or size<420*1024*1024):
                source=u;print("SELECTED",u,"bytes",size,flush=True);break
    except Exception as exc:print("SOURCE UNAVAILABLE",item,str(exc)[:150],flush=True)
if source is None:raise RuntimeError("No valid original Pexels source found")
# Use ffmpeg HTTP range input when supported by provider to avoid unnecessary full downloads.
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
out=DEST/"ballena-jorobada-azul.mp4"
cmd=[ffmpeg,"-hide_banner","-loglevel","warning","-y","-ss","4","-i",source,"-t","16",
"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
"-an","-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
subprocess.run(cmd,check=True,timeout=350)
if out.stat().st_size<300000:raise RuntimeError("Output video unexpectedly short")
print("PUBLISHED_ASSET",out.name,"bytes",out.stat().st_size,flush=True)
