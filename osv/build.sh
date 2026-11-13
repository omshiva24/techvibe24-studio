#!/usr/bin/env bash
# Full build of the OS one-shot video.  bash osv/build.sh VOICE_DIR OUT_DIR
set -euo pipefail
cd "$(dirname "$0")"; VD=$1; OUT=$2; mkdir -p "$OUT" build/parts
python3 timeline.py "$VD" > build/timeline.log; cat build/timeline.log
python3 mix.py
NP=$(python3 -c "import json;print(len(json.load(open('build/tl.json'))['pages']))")
MID=$(python3 -c "
import json;tl=json.load(open('build/tl.json'));T=tl['T']
print(min(range(1,len(tl['pages'])),key=lambda i:abs(tl['pages'][i]['t0']-T/2)))")
rm -f build/parts/*.mp4
python3 render.py 0 $MID build/parts/a.mp4 > build/parts/a.log 2>&1 &
python3 render.py $MID $NP build/parts/b.mp4 > build/parts/b.log 2>&1 &
wait
tail -qn 1 build/parts/a.log build/parts/b.log
printf "file 'parts/a.mp4'\nfile 'parts/b.mp4'\n" > build/parts.txt
T=$(python3 -c "import json;print(json.load(open('build/tl.json'))['T'])")
J=$(ffmpeg -hide_banner -i build/mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -y -v error -f concat -safe 0 -i build/parts.txt -i build/mix.wav -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true,aresample=48000" -c:a aac -b:a 192k -t $T -movflags +faststart "$OUT/Operating_System_One_Shot_TechVibe24.mp4"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height -of compact "$OUT/Operating_System_One_Shot_TechVibe24.mp4"
python3 render.py --pages build/pages > /dev/null
python3 make_extras.py build/pages "$OUT"
python3 gen_meta.py "$OUT"
echo BUILD OK
