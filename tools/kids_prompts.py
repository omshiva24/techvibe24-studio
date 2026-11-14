'''3D animated-movie style prompts for the Children's Day "message to kids" Short.'''
STY = (', high quality 3D animated movie still, cute stylized character with big expressive eyes, soft global illumination, '
       'subsurface scattering, vibrant colors, cinematic lighting, depth of field, octane render, 8k, masterpiece')
NEG = (' ### text, letters, words, watermark, logo, signature, deformed, disfigured, extra limbs, extra fingers, bad hands, '
       'bad anatomy, ugly, creepy, scary, horror, photo, realistic photo, blurry, lowres, nsfw')
P = {
 'stars': 'a cute little Indian boy sitting on a grassy hill at night looking up at a sky full of glowing stars and a big crescent moon, fireflies around, magical blue night',
 'dream': 'a cute little Indian girl holding up a glowing paper rocket toward the starry night sky, wonder in her eyes, golden sparkles floating, magical',
 'bike': 'a cute little Indian boy standing up next to his small red bicycle in a park, a band-aid on his knee, smiling bravely, golden evening light',
 'paint': 'a cute little Indian girl happily painting a big colorful rainbow on a canvas, paint splashes, bright cozy room with sunlight, joyful',
 'kind': 'a cute little Indian boy sharing his yellow umbrella with a small wet puppy in the rain, warm glowing street lights, heartwarming',
 'special': 'a cute little Indian girl smiling with arms wide open in a flower field at sunrise, butterflies around her, warm golden light, happiness',
 'final': 'happy cute Indian kids running together holding colorful balloons on a green hill at sunrise, joyful celebration, confetti in the air',
}
def full(sid): return P[sid] + STY + NEG
