import json
from pathlib import Path
def make_metadata(topic,hook,notes=""):
    topic,hook=topic.strip(),hook.strip()
    if not topic or not hook: raise ValueError("Topic and truthful hook are required")
    return {"title":hook[:95],"description":f"{notes.strip()}\n\nTopic: {topic}\n\n#GTA6 #Gaming #Shorts".strip(),"tags":["GTA 6","Grand Theft Auto VI","gaming","YouTube Shorts"],"category_id":"20","privacy_status":"private"}
def save_metadata(data,path="output/metadata.json"):
    Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
