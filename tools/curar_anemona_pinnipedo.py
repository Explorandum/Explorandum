#!/usr/bin/env python3
"""Curate two real underwater stock video clips. Originals credited to creators;
Pexels Content License. Subject identity verified through visual review before publishing.
"""
import urllib.request,subprocess,pathlib,imageio_ffmpeg
dest=pathlib.Path(__file__).resolve().parents[1]/"media"/"real";dest.mkdir(parents=True,exist_ok=True)
clips=[
("2556515","anemona-viva","1920_1080_25fps",5.6),
("5607745","pinnipedo-bajo-agua","3840_2160_2997fps",10.0),
]
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
for ident,name,preferred,seconds in clips:
    base="https://videos.pexels.com/video-files/"+ident+"/"+ident+"-"
    variants=[f"hd_{preferred}.mp4","hd_1920_1080_30fps.mp4","hd_1920_1080_2997fps.mp4","hd_1280_720_2997fps.mp4","hd_1280_720_25fps.mp4","uhd_3840_2160_2997fps.mp4"]
    source=None
    for variant in variants:
        url=base+variant
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"},method="HEAD"),timeout=20) as r:
                size=int(r.headers.get("Content-Length","0") or "0")
                if r.status==200 and (size==0 or size<150000000):source=url;print("FOUND",name,variant,size,flush=True);break
        except Exception as e:print("SKIP",variant,str(e)[:90],flush=True)
    if source is None:raise RuntimeError("No licensed source "+ident)
    output=dest/(name+".mp4")
    subprocess.run([ffmpeg,"-hide_banner","-loglevel","error","-y","-i",source,"-t",str(seconds),"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1","-an","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(output)],check=True,timeout=200)
    if output.stat().st_size<200000:raise RuntimeError("Broken video")
    print("READY",name,output.stat().st_size,flush=True)
