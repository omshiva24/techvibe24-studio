'''Cinematic scene prompts for the "insults create leaders" Short (faces hidden: silhouettes / from behind).'''
STY = (', cinematic film still, shot on ARRI Alexa, anamorphic lens, shallow depth of field, dramatic lighting, '
       'moody teal and orange color grade, film grain, ultra detailed, photorealistic, 8k')
NEG = (' ### text, letters, words, watermark, logo, signature, cartoon, anime, illustration, painting, drawing, cgi, '
       'deformed, disfigured, extra limbs, extra fingers, bad hands, bad anatomy, blurry, lowres, oversaturated, nsfw')
P = {
 'rain': 'a lonely young man in a dark hoodie standing alone under a single streetlight in heavy rain at night, seen from behind, head down, wet street reflections, cold blue light',
 'crowd': 'dark silhouettes of a group of people laughing and pointing at a lone young man in a hoodie, strong backlight, smoky room, faces in shadow, mocking crowd',
 'fist': 'extreme close-up of a strong clenched fist with water drops on the knuckles, dramatic side light, dark background, determination',
 'study': 'a young man in a hoodie studying alone late at night at a wooden desk, single warm desk lamp, stacks of books, seen from behind, dark room, focus',
 'stairs': 'a young man in a hoodie running up long concrete city stairs at dawn, seen from behind, mist, golden sunrise light, motion, determination',
 'peak': 'silhouette of a young man standing on a rocky mountain summit at sunrise, sea of clouds below, golden sun rays, epic wide shot, victory',
 'stage': 'a leader in a dark suit standing on a huge stage seen from behind, facing a massive cheering crowd, spotlight beams from above, golden confetti, epic wide shot',
 'walk': 'silhouette of a confident man in a suit walking toward a bright golden light at the end of a dark corridor, god rays, haze, hope',
}
def full(sid): return P[sid] + STY + NEG
