# Automatic highlights

Run:

`python main.py highlights --input assets/gameplay.mp4 --duration 30 --count 5`

ViralCut scans for FFmpeg scene changes, measures average audio energy in candidate windows, ranks candidates and exports up to five vertical MP4 clips into `output/highlights/`. It uses deterministic heuristics, not semantic AI. It may miss quiet but important moments or rank loud but uninteresting moments. Preview all clips and check rights to footage/audio before publishing. The editor currently exports video without source audio; audio-aware ranking is separate from the exported clip's soundtrack and this will be improved in a later milestone.
