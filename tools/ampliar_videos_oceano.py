#!/usr/bin/env python3
"""EXPLORANDUM video real: clips from individually attributed Wikimedia sources.
All files are original live-action footage. No interpolation or photograph animations.
"""
import json,pathlib,subprocess,urllib.parse,urllib.request,time,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT/"media"/"real";DEST.mkdir(parents=True,exist_ok=True)
AGENT={"User-Agent":"ExplorandumMedia/1.0 (educational project, github.com/prepdiplo-web/Explorandum)"}
CLIPS=[
    dict(name="ballena-madre-cria",file="Humpback whale Tail Sailing behaviour.webm",start=0,seconds=16,maxmb=22),
    dict(name="raya-comun",file="Stingray fly.webm",start=0,seconds=14,maxmb=12),
    dict(name="morena-aleta-amarilla",file="Yellowmargin Moray Eel at Kealakekua .webm",start=6,seconds=19,maxmb=45),
    dict(name="ctenoforo-california",file="Hormiphora californiensis video.webm",start=0,seconds=13,maxmb=15),
    dict(name="medusa-oceano-profundo",file="Jellyfish- 2016 Deepwater Exploration of the Marianas.webm",start=4,seconds=17,maxmb=18),
]
def info(file):
    api="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","prop":"imageinfo","titles":"File:"+file,"iiprop":"url|size","format":"json"})
    with urllib.request.urlopen(urllib.request.Request(api,headers=AGENT),timeout=45) as r: obj=json.load(r)
    p=next(iter(obj["query"]["pages"].values()))
    if "imageinfo" not in p: raise RuntimeError("Unknown Commons file: "+file)
    return p["imageinfo"][0]
def download(url,target,limit):
    with urllib.request.urlopen(urllib.request.Request(url,headers=AGENT),timeout=110) as r,open(target,"wb") as f:
        size=0
        while True:
            part=r.read(1024*1024)
            if not part:break
            size+=len(part)
            if size>limit*1024*1024: raise ValueError("source larger than limit")
            f.write(part)
    if target.stat().st_size<5000:raise RuntimeError("empty media")
def convert(entry,raw):
    out=DEST/(entry["name"]+".mp4")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(entry["start"]),"-i",str(raw),
                   "-t",str(entry["seconds"]),"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
                   "-c:v","libx264","-preset","fast","-crf","22","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(out)],check=True,timeout=240)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration,size:stream=width,height,codec_name","-of","json",str(out)],text=True))
    if out.stat().st_size<30000 or float(probe["format"]["duration"])<4:raise RuntimeError("Broken video: "+str(out))
    print("DONE",entry["name"],probe["format"]["duration"],out.stat().st_size,flush=True)
for e in CLIPS:
    print("SOURCE",e["file"],flush=True)
    metadata=info(e["file"])
    raw=DEST/(e["name"]+".input.webm")
    download(metadata["url"],raw,e["maxmb"])
    convert(e,raw)
    raw.unlink()
print("READY_REAL_CLIPS",len(CLIPS))
