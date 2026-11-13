#!/usr/bin/env bash
# Build the news Short from downloaded assets.  bash tools/news_build.sh ASSETS_DIR VOICE [PARTS]
set -euo pipefail
A=$1; VOICE=$2; PARTS=${3:-2}
python3 tools/news_timeline.py "$A" "$VOICE" build
python3 tools/news_audio.py build
T=$(python3 -c "import json;print(json.load(open('build/news_tl.json'))['T'])")
mkdir -p build/parts; rm -f build/parts/*.mp4
for p in $(seq 0 $((PARTS-1))); do
  read S E < <(python3 -c "T=$T;L=T/$PARTS;p=$p;print('%.4f %.4f'%(p*L,(p+1)*L if p<$PARTS-1 else T))")
  node tools/news_render.mjs $S $E build/parts/p$p.mp4 > build/parts/p$p.log 2>&1 &
done
wait
cat build/parts/*.log | grep -E "done|segments" || true
ls build/parts/p*.mp4 | sed "s/.*/file '&'/;s#build/parts/#parts/#" > build/parts.txt
# loudness: two-pass to -14 LUFS / -1.5 dBTP (YouTube reference)
J=$(ffmpeg -hide_banner -i build/news_mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
mkdir -p out
ffmpeg -y -v error -f concat -safe 0 -i build/parts.txt -i build/news_mix.wav -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=9:$MI:linear=true,aresample=48000" -c:a aac -b:a 256k -t $T -movflags +faststart out/TechVibe24_TechNews_13Nov2026.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact out/TechVibe24_TechNews_13Nov2026.mp4
