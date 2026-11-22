"""End-to-end Short builder for user-owned or licensed gameplay footage."""
import argparse
import json
from pathlib import Path

from content import make_metadata, save_metadata
from editing.auto_highlights import create_highlights
from editing.voiceover import generate_voiceover, create_srt, render_voiceover


def build(input_video, narration, topic, hook, output_dir="output/final",
          duration=30, voice="en-GB-RyanNeural", rate="+8%", burn_captions=True):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    picks = create_highlights(input_video, str(out / "candidates"), duration, 1)
    if not picks:
        raise RuntimeError("No highlight candidate could be created.")
    selected = picks[0]["file"]
    audio = generate_voiceover(narration, str(out / "voiceover.mp3"), voice, rate)
    captions = create_srt(audio, str(out / "captions.srt"), "tiny")
    video = render_voiceover(selected, audio, str(out / "viralcut_short.mp4"),
                             captions, burn_captions)
    metadata = make_metadata(topic, hook,
        "Original edited gameplay with narration and captions. Review the final video and metadata before publishing.")
    save_metadata(metadata, str(out / "youtube_metadata.json"))
    manifest = {"video": video, "voiceover": audio, "captions": captions,
                "metadata": str(out / "youtube_metadata.json"),
                "highlight_selection": picks[0],
                "note": "Highlight selection is heuristic. Review before publishing."}
    (out / "build_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main():
    p = argparse.ArgumentParser(description="Build a complete vertical Short from permitted gameplay footage.")
    p.add_argument("--input", required=True)
    p.add_argument("--narration", required=True)
    p.add_argument("--topic", default="GTA 6 gameplay")
    p.add_argument("--hook", required=True)
    p.add_argument("--output-dir", default="output/final")
    p.add_argument("--duration", type=float, default=30)
    p.add_argument("--voice", default="en-GB-RyanNeural")
    p.add_argument("--rate", default="+8%")
    p.add_argument("--no-burn-captions", action="store_true")
    a = p.parse_args()
    result = build(a.input, a.narration, a.topic, a.hook, a.output_dir,
                   a.duration, a.voice, a.rate, not a.no_burn_captions)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
