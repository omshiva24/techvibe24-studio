'''Nostalgic, real-looking scene prompts for the Children's Day Short (Indian setting).'''
STY = (', cinematic film still, shot on ARRI Alexa, shallow depth of field, soft natural light, warm nostalgic color grade, '
       'film grain, ultra detailed, photorealistic, 8k')
NEG = (' ### text, letters, words, watermark, logo, signature, cartoon, anime, illustration, painting, drawing, cgi, 3d render, '
       'deformed, disfigured, extra limbs, extra fingers, bad hands, bad anatomy, ugly face, blurry, lowres, oversaturated, nsfw')
P = {
 'college': 'a tired Indian college student sitting at a desk in a hostel room at night, laptop screen glowing, piles of notes and a coffee mug, side view, cold blue screen light',
 'photo': 'close-up of hands holding an old faded printed childhood school class photo, warm window light, dust in the air, nostalgic, shallow depth of field',
 'boat': 'two little Indian children floating paper boats in a rain puddle on a village street during monsoon rain, seen from behind, joyful, splashing water, warm light',
 'tiffin': 'happy Indian school children in school uniform sitting together on a wooden bench sharing steel tiffin lunch boxes, laughing, warm afternoon sunlight through classroom window',
 'cricket': 'Indian kids playing street cricket in a narrow lane at golden hour, a boy batting with a wooden bat, tennis ball in the air, dust glowing in sunlight, joyful, wide shot',
 'kite': 'a small Indian boy flying a colorful kite on a rooftop terrace at sunset, seen from behind, golden sky, dreamy, nostalgic',
 'friends': 'a group of happy Indian college friends laughing together on a college campus lawn at golden hour, carefree, candid moment, warm light',
 'final': 'colorful balloons and paper confetti floating in warm golden light, soft bokeh, celebration, dreamy, no people',
}
def full(sid): return P[sid] + STY + NEG
