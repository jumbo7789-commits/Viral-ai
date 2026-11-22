import shutil,subprocess
from pathlib import Path
def create_short(source,output,start=0,duration=35):
    ff=shutil.which("ffmpeg")
    if not ff: raise RuntimeError("FFmpeg is required")
    src,out=Path(source),Path(output)
    if not src.is_file(): raise FileNotFoundError(src)
    out.parent.mkdir(parents=True,exist_ok=True)
    vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
    cmd=[ff,"-y","-ss",str(max(0,float(start))),"-i",str(src),"-t",str(min(max(1,float(duration)),180)),"-vf",vf,"-an","-c:v","libx264","-preset","veryfast","-crf","23","-movflags","+faststart",str(out)]
    subprocess.run(cmd,check=True,capture_output=True,text=True); return str(out)
