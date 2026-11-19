'''Cinematic scene prompts for the International Men's Day Short (faces hidden: silhouettes / from behind).'''
STY = (', cinematic film still, shot on ARRI Alexa, anamorphic lens, shallow depth of field, dramatic lighting, '
       'moody teal and orange color grade, film grain, ultra detailed, photorealistic, 8k')
NEG = (' ### text, letters, words, watermark, logo, signature, cartoon, anime, illustration, painting, drawing, cgi, '
       'deformed, disfigured, extra limbs, extra fingers, bad hands, bad anatomy, blurry, lowres, oversaturated, nsfw, visible face')
P = {
 'dawn': 'a man in simple work clothes with a bag on his shoulder walking out of a small house at dawn, seen from behind, quiet empty street, soft blue morning light, mist',
 'work': 'a hardworking man carrying a heavy sack on his shoulder at a construction site at golden sunset, seen from behind, dust in the golden light, sweat, determination',
 'bench': 'a tired man sitting alone on a bench under a single streetlight at night in light rain, seen from behind, head down, city lights bokeh, loneliness',
 'father': 'a father holding his little son\'s hand, walking on a quiet road at golden hour, seen from behind, warm sunlight, long shadows, love',
 'friends': 'two young men sitting side by side on a hill watching the sunset, seen from behind, one arm around the other\'s shoulder, brotherhood, warm light',
 'cliff': 'a strong man standing firm on a rocky cliff edge facing a stormy sea, seen from behind, wind, dramatic dark clouds, rays of light breaking through',
 'peak': 'silhouette of a man standing on a mountain summit with arms wide open at sunrise, sea of clouds below, golden sun rays, epic wide shot, victory',
 'walk': 'an old father and his grown-up son walking together toward a golden sunset on a village road, seen from behind, the son\'s hand on the father\'s shoulder, warm golden light',
}
def full(sid): return P[sid] + STY + NEG
