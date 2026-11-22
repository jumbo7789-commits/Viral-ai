import os,requests
API="https://www.googleapis.com/youtube/v3/search"
def search_videos(query="GTA 6",max_results=10,api_key=None):
    key=api_key or os.getenv("YOUTUBE_API_KEY")
    if not key: raise RuntimeError("Set YOUTUBE_API_KEY to use public trend research")
    p={"part":"snippet","q":query,"type":"video","order":"viewCount","maxResults":min(max(1,int(max_results)),50),"key":key}
    r=requests.get(API,params=p,timeout=30); r.raise_for_status()
    out=[]
    for x in r.json().get("items",[]):
        s=x.get("snippet",{}); vid=x.get("id",{}).get("videoId")
        out.append({"title":s.get("title",""),"channel":s.get("channelTitle",""),"published_at":s.get("publishedAt",""),"url":f"https://www.youtube.com/watch?v={vid}" if vid else ""})
    return out
