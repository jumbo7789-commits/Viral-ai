import argparse, json
from content import make_metadata, save_metadata
from editing.short_editor import create_short
from editing.auto_highlights import create_highlights, rank_highlights

def main():
    p=argparse.ArgumentParser(description="ViralCut AI Shorts toolkit")
    sub=p.add_subparsers(dest="command",required=True)
    e=sub.add_parser("edit",help="Cut one vertical Short")
    e.add_argument("--input",required=True); e.add_argument("--output",default="output/short.mp4"); e.add_argument("--start",type=float,default=0); e.add_argument("--duration",type=float,default=35)
    h=sub.add_parser("highlights",help="Find and export the strongest heuristic highlight candidates")
    h.add_argument("--input",required=True); h.add_argument("--output-dir",default="output/highlights"); h.add_argument("--duration",type=float,default=30); h.add_argument("--count",type=int,default=5)
    m=sub.add_parser("metadata",help="Create suggested title and description")
    m.add_argument("--topic",required=True); m.add_argument("--hook",required=True); m.add_argument("--notes",default="")
    a=p.parse_args()
    if a.command=="edit":
        print(create_short(a.input,a.output,a.start,a.duration))
    elif a.command=="highlights":
        results=create_highlights(a.input,a.output_dir,a.duration,a.count)
        print(json.dumps(results,indent=2))
        print("Review every clip before publishing. Scores are heuristic, not predictions of views.")
    else:
        d=make_metadata(a.topic,a.hook,a.notes); save_metadata(d); print(json.dumps(d,indent=2))
if __name__=="__main__": main()
