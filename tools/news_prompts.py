'''Photoreal backdrop prompts for the TechVibe24 news Short (no people, no logos).'''
STY = (', cinematic film still, shot on ARRI Alexa, anamorphic lens, shallow depth of field, moody dramatic lighting, '
       'deep teal and electric blue tones, ultra detailed, photorealistic, 8k')
NEG = (' ### text, letters, words, numbers, typography, watermark, logo, brand, signature, cartoon, anime, illustration, painting, '
       'drawing, cgi, plastic, deformed, blurry, lowres, oversaturated, person, people, human, face, hands, nsfw')
P = {
 'hook': 'dark futuristic broadcast news studio with a curved wall of giant glowing screens showing world maps and abstract data graphs, red alert lighting, empty anchor desk, volumetric haze',
 'nv1': 'extreme macro close-up of a powerful AI graphics processor chip on a black circuit board, glowing green light traces, metallic heat spreader, tiny reflections, dark background',
 'nv2': 'empty black leather executive chair at the head of a long glass boardroom table, night city skyline through floor-to-ceiling windows, cold green and blue light, dramatic long shadows',
 'ipo': 'huge wall of stock market screens with glowing green rising candlestick charts on a dark trading floor, bokeh city lights, sense of a record-breaking market',
 'spx': 'aerial view of a gigantic futuristic AI data center campus in the Arizona desert at dusk, rows of huge server halls, cooling towers, power lines, a rocket launch trail in the distant purple sky',
 'law': 'wooden judge gavel resting on a sound block on a courtroom desk, a glowing blue holographic AI brain made of circuit lines floating above it, dark wood courtroom, dramatic rim light',
 'gls': 'sleek modern black smart glasses on a glossy black reflective surface, faint holographic display glowing in one lens, premium product photography, soft studio light, blue accent light',
 'cta': 'abstract tunnel of glowing blue and violet circuit lines and light streaks rushing toward the camera, deep dark space, speed and motion',
}
def full(sid): return P[sid] + STY + NEG
