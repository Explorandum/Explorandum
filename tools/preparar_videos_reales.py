#!/usr/bin/env python3
"""Build short, authentic wildlife videos for a separate documentary preview.
No stills, Ken Burns effects, invented fauna or AI-generated video.
All clips retain Commons author, source and license in cabina-video-real.html.
"""
import json, pathlib, subprocess, urllib.parse, urllib.request, time, re, sys
from urllib.error import URLError
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT/"media"/"real"
DEST.mkdir(parents=True,exist_ok=True)
AGENT={"User-Agent":"ExplorandumMedia/1.0 (educational documentary, repo github.com/prepdiplo-web/Explorandum)","Accept":"application/json"}
SOURCES=[
 {"name":"tiburon-ballena","file":"Swimming with a whale shark (Rhincodon typus) (no audio).webm","seconds":24,"start":20,"max_source_mb":95},
 {"name":"lobo-marino","file":"Sea lions at Pier 39 video.webm","seconds":17,"start":0,"max_source_mb":20},
 {"name":"ballena-jorobada","file":"WhalesKGS.webm","seconds":7,"start":0,"max_source_mb":5},
 {"name":"arrecife-real","file":"Unterwasserwelt, Korallenriff im Roten Meer DSCF1654.webm","seconds":24,"start":16,"max_source_mb":95},
]
def media_info(file):
    title="File:"+file
    api="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":title,"prop":"imageinfo","iiprop":"url|size","iiurlwidth":1280,"format":"json"})
    req=urllib.request.Request(api,headers=AGENT)
    with urllib.request.urlopen(req,timeout=45) as response:
        value=json.load(response)
    page=next(iter(value["query"]["pages"].values()))
    if "missing" in page or not page.get("imageinfo"):raise RuntimeError("Missing Commons video "+file)
    info=page["imageinfo"][0]
    # A 720p or 1080p Wikimedia Commons transcode is essential for gigantic source files.
    name=file.replace(" ","_")
    md5=__import__('hashlib').md5(name.encode("utf8")).hexdigest()
    path="/".join((md5[0],md5[:2],urllib.parse.quote(name,safe="(),-._")))
    candidates=[
        "https://upload.wikimedia.org/wikipedia/commons/transcoded/"+path+"/720p.vp9.webm",
        "https://upload.wikimedia.org/wikipedia/commons/transcoded/"+path+"/1080p.vp9.webm"
    ]
    if info["size"]<=95*1024*1024:
        return info["url"],info["size"],candidates
    return None,info["size"],candidates

def download(url,destination,max_mb):
    req=urllib.request.Request(url,headers={"User-Agent":AGENT["User-Agent"]})
    with urllib.request.urlopen(req,timeout=80) as response,open(destination,"wb") as file:
        seen=0
        while True:
            data=response.read(1024*1024)
            if not data:break
            seen+=len(data)
            if seen>max_mb*1024*1024:raise ValueError("download larger than limit")
            file.write(data)
    if destination.stat().st_size<10000:raise ValueError("video too small")
    return seen

for item in SOURCES:
    print("PREPARING",item["name"],item["file"],flush=True)
    original,size,transcoded=media_info(item["file"])
    choices=([original] if original else [])+transcoded
    raw=DEST/(item["name"]+".input.webm")
    errors=[]
    for url in choices:
        try:
            print("FETCH",url,flush=True)
            download(url,raw,item["max_source_mb"])
            break
        except Exception as ex:
            errors.append(str(ex));time.sleep(2)
            raw.unlink(missing_ok=True)
    else:
        # If the file is too large and Wikimedia transcodes fail, report clearly.
        raise RuntimeError("No accessible source for "+item["name"]+": "+" | ".join(errors))
    output=DEST/(item["name"]+".mp4")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(item["start"]),"-i",str(raw),
      "-t",str(item["seconds"]),"-vf","scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1",
      "-an","-c:v","libx264","-preset","fast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(output)]
    subprocess.run(cmd,check=True,timeout=240)
    raw.unlink(missing_ok=True)
    if output.stat().st_size<20000:raise RuntimeError("Video empty")
    info=subprocess.check_output(["ffprobe","-v","quiet","-show_entries","format=duration,size","-of","json",str(output)],text=True)
    print("COMPLETE",item["name"],info,flush=True)
print("ALL_REAL_VIDEOS_READY",len(SOURCES),flush=True)
