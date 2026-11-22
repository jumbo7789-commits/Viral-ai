# AI voiceovers and captions

Install the optional tools (not required for the base editor):

`pip install -r requirements-voice.txt`

Generate narration and speech-aligned SRT captions:

`python main.py voiceover --text "This is the moment everything changed..." `

Use a different English voice:

`python main.py voiceover --text "Your script here" --voice en-GB-SoniaNeural`

Add narration to an existing Short and burn captions into the picture:

`python main.py voiceover --text "Your narration" --video output/highlights/highlight_01.mp4 --burn-captions`

Outputs default to `output/voiceover.mp3`, `output/captions.srt`, and `output/short_with_voiceover.mp4`. The caption model runs locally on CPU; its first run downloads the selected Whisper model and can take time. Edge TTS needs an internet connection. Check the chosen voice and captions before publishing. The generated voice is synthetic; do not impersonate a real person or imply endorsement. Avoid copyrighted scripts, music and gameplay you do not have rights to use.
