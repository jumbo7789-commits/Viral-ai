import argparse, json
from content import make_metadata, save_metadata
from editing.short_editor import create_short
from editing.auto_highlights import create_highlights
from editing.voiceover import generate_voiceover, create_srt, render_voiceover

def main():
    p=argparse.ArgumentParser(description="ViralCut AI Shorts toolkit")
    sub=p.add_subparsers(dest="command",required=True)
    e=sub.add_parser("edit",help="Cut one vertical Short")
    e.add_argument("--input",required=True); e.add_argument("--output",default="output/short.mp4"); e.add_argument("--start",type=float,default=0); e.add_argument("--duration",type=float,default=35)
    h=sub.add_parser("highlights",help="Find and export highlight candidates")
    h.add_argument("--input",required=True); h.add_argument("--output-dir",default="output/highlights"); h.add_argument("--duration",type=float,default=30); h.add_argument("--count",type=int,default=5)
    v=sub.add_parser("voiceover",help="Generate narration, aligned captions and optionally combine with a Short")
    v.add_argument("--text",required=True,help="Narration text"); v.add_argument("--audio-output",default="output/voiceover.mp3")
    v.add_argument("--voice",default="en-GB-RyanNeural"); v.add_argument("--rate",default="+8%")
    v.add_argument("--video",help="Optional existing Short to add narration to")
    v.add_argument("--output",default="output/short_with_voiceover.mp4")
    v.add_argument("--captions",default="output/captions.srt")
    v.add_argument("--burn-captions",action="store_true")
    v.add_argument("--model",default="tiny",choices=["tiny","base","small"])
    m=sub.add_parser("metadata",help="Create suggested title and description")
    m.add_argument("--topic",required=True); m.add_argument("--hook",required=True); m.add_argument("--notes",default="")
    a=p.parse_args()
    if a.command=="edit":
        print(create_short(a.input,a.output,a.start,a.duration))
    elif a.command=="highlights":
        results=create_highlights(a.input,a.output_dir,a.duration,a.count)
        print(json.dumps(results,indent=2))
        print("Review every clip before publishing. Scores are heuristic, not predictions of views.")
    elif a.command=="voiceover":
        audio=generate_voiceover(a.text,a.audio_output,a.voice,a.rate)
        captions=create_srt(audio,a.captions,a.model)
        print(json.dumps({"voiceover":audio,"captions":captions},indent=2))
        if a.video:
            print(render_voiceover(a.video,audio,a.output,captions,a.burn_captions))
    else:
        d=make_metadata(a.topic,a.hook,a.notes); save_metadata(d); print(json.dumps(d,indent=2))
if __name__=="__main__": main()
