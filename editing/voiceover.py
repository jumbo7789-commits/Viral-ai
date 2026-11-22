"""Optional narration, speech-aligned subtitles and voiceover mixing.

Requires: pip install -r requirements-voice.txt and FFmpeg.
Edge TTS requires an internet connection. Whisper caption alignment runs locally.
"""
import asyncio
import shutil
import subprocess
from pathlib import Path

DEFAULT_VOICE = "en-GB-RyanNeural"

def _ffmpeg():
    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError("FFmpeg is required for video/audio rendering.")
    return path

def generate_voiceover(text, output="output/voiceover.mp3", voice=DEFAULT_VOICE, rate="+8%", pitch="+0Hz"):
    text = text.strip()
    if not text:
        raise ValueError("Narration text cannot be empty.")
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError("Install optional voice tools: pip install -r requirements-voice.txt") from exc
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    async def _generate():
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(target))
    asyncio.run(_generate())
    return str(target)

def create_srt(audio, output="output/captions.srt", model_size="tiny"):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install local caption tools: pip install -r requirements-voice.txt") from exc
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(audio), beam_size=5, vad_filter=True)
    def stamp(seconds):
        ms = round(seconds * 1000)
        hours, ms = divmod(ms, 3600000)
        minutes, ms = divmod(ms, 60000)
        secs, ms = divmod(ms, 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, segment in enumerate(segments, 1):
        words = segment.text.strip()
        if words:
            rows.extend([str(index), f"{stamp(segment.start)} --> {stamp(segment.end)}", words, ""])
    target.write_text("\n".join(rows), encoding="utf-8")
    if not rows:
        raise RuntimeError("Speech recognition returned no caption segments.")
    return str(target)

def render_voiceover(video, narration, output="output/short_with_voiceover.mp4",
                     captions=None, burn_captions=False, original_volume=0.18):
    ffmpeg = _ffmpeg()
    video, narration, target = Path(video), Path(narration), Path(output)
    if not video.is_file() or not narration.is_file():
        raise FileNotFoundError("Video and narration audio files must both exist.")
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [ffmpeg, "-y", "-i", str(video), "-i", str(narration)]
    probe = shutil.which("ffprobe")
    has_audio = False
    if probe:
        check = subprocess.run([probe, "-v", "error", "-select_streams", "a:0",
                                "-show_entries", "stream=index", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True)
        has_audio = bool(check.stdout.strip())
    if has_audio:
        filters = "[0:a]volume=" + str(max(0.0, min(1.0, float(original_volume)))) + "[bg];[1:a]volume=1.0[vo];[bg][vo]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    else:
        filters = "[1:a]anull[aout]"
    if burn_captions:
        if not captions or not Path(captions).is_file():
            raise ValueError("A valid SRT file is required to burn captions.")
        subtitle_path = str(Path(captions).resolve()).replace("\\", "/").replace(":", "\\:")
        filters += f";[0:v]subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=150'[vout]"
        command += ["-filter_complex", filters, "-map", "[vout]", "-map", "[aout]"]
    else:
        command += ["-filter_complex", filters, "-map", "0:v:0", "-map", "[aout]"]
    command += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(target)]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return str(target)
