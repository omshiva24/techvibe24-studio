#!/usr/bin/env bash
# parts/p00.mp4..p15.mp4 + build/audio.m4a -> dist/ (full video, 3 Shorts, thumbnail, QA sheet)
set -e
T=$(python3 -c "import json;print(json.load(open('build/timeline.json'))['T'])")
FO=$(python3 -c "print($T-2.5)")
mkdir -p dist
ls parts/p*.mp4 | sort | sed "s/.*/file '&'/" > parts/list.txt
sed -i "s#file 'parts/#file '#" parts/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i parts/list.txt -i build/audio.m4a -map 0:v -map 1:a -c:v copy -af "afade=t=out:st=$FO:d=2.5" -c:a aac -b:a 192k -t $T -movflags +faststart dist/HanumanChalisa_Movie_TECHVIBE24.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 dist/HanumanChalisa_Movie_TECHVIBE24.mp4
clip() { n=$1; s=$2; e=$3; d=$(python3 -c "print(round($e-$s,3))"); fo=$(python3 -c "print(round($e-$s-1.2,3))"); vo=$(python3 -c "print(round($e-$s-0.6,3))")
  ffmpeg -y -loglevel error -ss $s -i dist/HanumanChalisa_Movie_TECHVIBE24.mp4 -t $d -vf "fade=t=in:st=0:d=0.4,fade=t=out:st=$vo:d=0.6" -af "afade=t=in:st=0:d=0.4,afade=t=out:st=$fo:d=1.2" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart dist/HanumanChalisa_Movie_Short_Part$n.mp4; }
clip 1 0 165.0
clip 2 165.0 315.4
clip 3 315.4 $T
mkdir -p qa; i=0
for t in 5 15 38 70 95 115 150 180 190 225 240 265 300 330 360 385 410 435 448 456; do i=$((i+1)); ffmpeg -y -loglevel error -ss $t -i dist/HanumanChalisa_Movie_TECHVIBE24.mp4 -frames:v 1 -q:v 3 qa/f$(printf %02d $i).jpg; done
ffmpeg -y -loglevel error -i qa/f%02d.jpg -vf scale=216:384,tile=5x4 -q:v 4 dist/qa_sheet.jpg
ffmpeg -y -loglevel error -ss 38 -i dist/HanumanChalisa_Movie_TECHVIBE24.mp4 -frames:v 1 -q:v 1 www/thumb/frame.jpg
node tools/thumb.mjs dist/HanumanChalisa_Movie_Thumbnail.jpg
cp www/thumb/frame.jpg dist/HanumanChalisa_Movie_Cover_Vertical.jpg
ls -la dist
