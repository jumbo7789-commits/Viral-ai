# Setup guide
Use Python 3.11+ and install requirements with `pip install -r requirements.txt`. Install FFmpeg separately. Run `python main.py --help`.
To edit authorised footage: `python main.py edit --input assets/gameplay.mp4 --start 12 --duration 35 --output output/short.mp4`.
For YouTube upload, configure a Google Cloud project, enable YouTube Data API v3, create OAuth Desktop credentials and keep the JSON file local as `client_secret.json`. Never commit credentials. Review content before publishing; privacy defaults to private.
