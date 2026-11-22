# Complete Short production

The `viralcut_pipeline.py` pipeline takes gameplay footage you own or are licensed to use and:
1. Ranks candidate moments using FFmpeg scene changes and audio energy (heuristic, not semantic AI).
2. Exports the top candidate as a vertical 1080×1920 clip.
3. Generates English narration with Edge TTS.
4. Creates speech-aligned captions with faster-whisper and burns them into the video.
5. Writes suggested YouTube metadata and a build manifest.

## Run locally
```bash
pip install -r requirements.txt -r requirements-voice.txt
python viralcut_pipeline.py --input gameplay.mp4 --narration "Your narration here" --hook "A truthful opening hook"
```

## Run from iPhone with GitHub Actions
Open **Actions → Build a complete ViralCut Short → Run workflow**:
https://github.com/jumbo7789-commits/Viral-ai/actions/workflows/build-short.yml

Provide a direct HTTPS download URL for a video you own or have permission to use, confirm those rights, and enter the narration and truthful hook. The workflow accepts videos up to 1 GB and runs for up to 45 minutes. It produces an artifact named `viralcut-complete-short`; download it from the completed workflow run.

Only direct downloadable HTTPS video URLs are supported (not ordinary YouTube watch-page URLs). The workflow does not fetch other creators' videos. Keep the source URL private if it contains a token. GitHub Actions usage limits apply. Review the video, captions, title and description before publishing; nothing is uploaded to YouTube automatically. Highlight ranking is heuristic and cannot predict views or monetisation.
