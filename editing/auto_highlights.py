"""Heuristic highlight finder for footage the user owns or is licensed to use.

Uses FFmpeg scene-change timestamps and short-window audio RMS. This is a
ranking aid, not semantic AI and not a guarantee that a moment will perform well.
"""
import math
import re
import shutil
import subprocess
import wave
from array import array
from pathlib import Path

SCENE_RE = re.compile(r"pts_time:([0-9]+(?:\.[0-9]+)?)")

def _run(command):
    return subprocess.run(command, check=True, capture_output=True, text=True)

def probe_duration(source):
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe is required (install FFmpeg).")
    result = _run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                   "-of", "default=noprint_wrappers=1:nokey=1", str(source)])
    return float(result.stdout.strip())

def find_scene_changes(source, threshold=0.30):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("FFmpeg is required (install FFmpeg).")
    command = [ffmpeg, "-hide_banner", "-i", str(source), "-vf",
               f"select='gt(scene,{float(threshold)})',showinfo", "-an", "-f", "null", "-"]
    result = subprocess.run(command, capture_output=True, text=True)
    # FFmpeg may return non-zero for the null output on some builds; timestamps
    # are still useful if showinfo emitted them.
    return sorted({float(x) for x in SCENE_RE.findall(result.stderr)})

def _audio_rms_by_second(source, duration):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("FFmpeg is required (install FFmpeg).")
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        _run([ffmpeg, "-y", "-v", "error", "-i", str(source), "-vn", "-ac", "1",
              "-ar", "8000", "-c:a", "pcm_s16le", tmp.name])
        with wave.open(tmp.name, "rb") as wav:
            rate, width = wav.getframerate(), wav.getsampwidth()
            frames_per_second = rate
            seconds = []
            for _ in range(math.ceil(duration)):
                raw = wav.readframes(frames_per_second)
                if not raw:
                    break
                if width == 2:
                    samples = array("h")
                    samples.frombytes(raw)
                    if __import__("sys").byteorder != "little":
                        samples.byteswap()
                    rms = math.sqrt(sum(x*x for x in samples) / max(1, len(samples)))
                else:
                    rms = 0.0
                seconds.append(rms)
            return seconds

def rank_highlights(source, clip_duration=30, count=5, scene_threshold=0.30):
    """Return ranked {start,duration,score,reason} candidates."""
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)
    total = probe_duration(source)
    clip_duration = min(max(5.0, float(clip_duration)), 60.0, total)
    if total < 5:
        raise ValueError("Source video must be at least 5 seconds long.")
    scenes = find_scene_changes(source, scene_threshold)
    rms = _audio_rms_by_second(source, total)
    # Generate candidate starts around scene changes and at regular intervals.
    starts = {0.0, max(0.0, total-clip_duration)}
    starts.update(max(0.0, min(total-clip_duration, t-clip_duration/2)) for t in scenes)
    step = max(5.0, clip_duration/2)
    t = 0.0
    while t <= total-clip_duration:
        starts.add(round(t, 2)); t += step
    candidates = []
    for start in starts:
        lo, hi = int(start), min(len(rms), int(math.ceil(start+clip_duration)))
        energy = sum(rms[lo:hi]) / max(1, hi-lo)
        scene_hits = sum(1 for x in scenes if start <= x <= start+clip_duration)
        score = energy + scene_hits * 120.0
        candidates.append({"start": round(start,2), "duration": round(clip_duration,2),
                           "score": round(score,2), "audio_rms": round(energy,2),
                           "scene_changes": scene_hits,
                           "reason": "Audio energy and scene-change heuristic"})
    candidates.sort(key=lambda x: x["score"], reverse=True)
    chosen=[]
    for item in candidates:
        if all(abs(item["start"]-other["start"]) >= clip_duration*0.65 for other in chosen):
            chosen.append(item)
        if len(chosen) >= max(1, int(count)):
            break
    return chosen

def create_highlights(source, output_dir="output/highlights", clip_duration=30, count=5):
    from editing.short_editor import create_short
    output=Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    picks=rank_highlights(source, clip_duration, count)
    results=[]
    for i,pick in enumerate(picks,1):
        target=output/f"highlight_{i:02d}.mp4"
        create_short(source,target,pick["start"],pick["duration"])
        results.append({**pick,"file":str(target)})
    return results
