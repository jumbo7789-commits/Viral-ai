import argparse, json
from content import make_metadata, save_metadata
from editing.short_editor import create_short

def main():
    p=argparse.ArgumentParser(description="ViralCut AI Shorts toolkit")
    sub=p.add_subparsers(dest="command",required=True)
    e=sub.add_parser("edit"); e.add_argument("--input",required=True); e.add_argument("--output",default="output/short.mp4"); e.add_argument("--start",type=float,default=0); e.add_argument("--duration",type=float,default=35)
    m=sub.add_parser("metadata"); m.add_argument("--topic",required=True); m.add_argument("--hook",required=True); m.add_argument("--notes",default="")
    a=p.parse_args()
    if a.command=="edit": print(create_short(a.input,a.output,a.start,a.duration))
    else:
        d=make_metadata(a.topic,a.hook,a.notes); save_metadata(d); print(json.dumps(d,indent=2))
if __name__=="__main__": main()
