#!/usr/bin/env python3
"""Trim the NOAA logo title from the beginning of the real deep-sea jellyfish footage.
Uses the local already licensed MP4, does not alter the original.
"""
import pathlib,subprocess
import imageio_ffmpeg
root=pathlib.Path(__file__).resolve().parents[1]
original=root/'media/real/medusa-oceano-profundo.mp4'
out=root/'media/real/medusa-sin-cartela.mp4'
assert original.is_file() and original.stat().st_size>100_000
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y',
 '-ss','5.5','-i',str(original),'-t','10.5','-an','-c:v','libx264','-crf','21',
 '-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True,timeout=180)
assert out.stat().st_size>100000
print('NOAA_JELLYFISH_TRIMMED',out.stat().st_size,flush=True)
