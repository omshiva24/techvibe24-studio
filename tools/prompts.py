'''Scene prompts for the Hanuman Chalisa video (SDXL models on AI Horde).'''
HAN = ('Hanuman, the monkey god from Ramayana, (vanara with the face of a monkey:1.5), reddish-orange fur, '
       'ornate golden crown, gold ornaments, red silk dhoti, golden gada mace')
MONKEY = '(monkey-faced Hanuman:1.3)'
RAM = 'Lord Rama, blue-skinned Hindu god prince with golden crown, yellow silk, bow'
SITA = 'Goddess Sita in red and gold saree'
STY = (', epic Indian mythology movie scene, cinematic film still, dramatic volumetric god rays, '
       'rich saffron and gold colors, highly detailed, photorealistic, 8k')
NEG = (' ### text, letters, watermark, logo, signature, cartoon, anime, childish, toy, deformed, disfigured, '
       'extra limbs, extra arms, extra fingers, bad anatomy, ugly face, blurry, lowres, nsfw, human face, human nose, trident')
P = {
 'intro': f'{HAN}, small distant figure kneeling in prayer on a Himalayan peak against a huge rising sun, sea of clouds, birds',
 'd1': 'old Indian saint poet Tulsidas with white beard and saffron robe writing on palm leaves by an oil lamp on the Ganga ghats at dawn, temples in mist',
 'd2': f'{HAN}, descending from the sky with a raised blessing palm, swirling clouds and wind, divine light',
 'c1': f'{HAN}, standing majestically on a mountain summit above the clouds, mace on shoulder, vast golden aura, sunrise',
 'c2': 'divine mother Anjani holding (baby monkey god Hanuman with a monkey face:1.4) in a forest hermitage at sunrise, swirling wind and light from the sky',
 'c3': f'{HAN}, standing in a stormy sky surrounded by lightning bolts, powerful, dark clouds breaking with light',
 'c4': f'close portrait of {HAN}, golden glowing face, jewelled earrings, serene compassionate eyes, golden rim light',
 'c5': f'{HAN}, holding a glowing thunderbolt and a saffron flag waving in the wind on a rocky ridge at golden hour',
 'c6': 'Lord Shiva meditating on snowy Mount Kailash, a beam of golden blessing light descending to a green forest far below',
 'c7': f'{HAN}, sitting under a giant banyan tree reading ancient palm leaf scriptures, calm, morning light',
 'c8': f'{HAN}, kneeling with eyes closed in devotion, glowing image of Rama and Sita in his heart, temple light',
 'c9': f'{SITA}, sitting sorrowfully under an ashoka tree in a moonlit palace garden, a golden ring glowing in her hand',
 'c10': f'giant colossal {HAN}, fighting demon army on a burning battlefield of Lanka, fire, smoke, red sky',
 'c11': f'{HAN}, flying through a moonlit night sky carrying a whole mountain glowing with green herbs on his palm',
 'c12': f'{RAM}, tears of joy, looking up with love at the sky at dawn, war camp tents and saffron banners behind',
 'c13': f'{RAM} blessing kneeling {MONKEY}, divine golden light, glowing faces of gods in the clouds above',
 'c14': 'celestial heaven assembly of Hindu gods on clouds, Brahma on a lotus, sage Narada and goddess Saraswati playing veena, giant serpent Sheshnag, golden light',
 'c15': 'cosmic circle of Hindu gods in the clouds, Yama on a buffalo, Kubera with treasure, sages and poets bowing to a brilliant golden light',
 'c16': f'{HAN}, kneeling with folded hands on a rocky mountain at golden hour, joyful devotion, valley below',
 'c17': 'golden palace hall in Lanka, coronation of king Vibhishana, golden towers through arches, royal court',
 'c18': '(baby monkey god Hanuman with a monkey face:1.4) leaping high into the sky toward a giant blazing sun, arms outstretched, clouds and earth far below',
 'c19': f'{HAN}, leaping across a vast stormy ocean toward a distant island, huge waves and spray, dramatic sky',
 'c20': f'{HAN}, effortlessly lifting a huge boulder off a mountain path while grateful villagers watch',
 'c21': f'{HAN}, standing guard before the grand golden gates of an ancient Indian palace in Ayodhya, oil lamps on the steps',
 'c22': f'{HAN}, standing tall in a fierce storm with lightning, protective golden aura, small village huts glowing safely behind him',
 'c23': f'{HAN}, roaring on a mountain top, golden shockwave rings in the sky, clouds parting, mountains trembling',
 'c24': f'dark misty forest at night, shadowy ghosts fleeing from the blazing golden light of {HAN}',
 'c25': 'humble Indian home lit by oil lamps, golden healing light falling on a sick elderly man in bed, family praying with folded hands',
 'c26': f'devotee meditating in a stone temple courtyard, {HAN} standing behind protecting him, dark clouds dissolving into light',
 'c27': f'{RAM}, seated on a simple wooden throne in a forest hermitage, serene ascetic king, morning light rays',
 'c28': 'devotees offering marigold flowers and oil lamps at an ancient Hanuman temple at dusk, glowing lanterns rising into the sky',
 'c29': f'{HAN}, standing in a vast cosmic sky above the earth, four giant glowing rings of light around him, stars',
 'c30': f'{HAN}, raising his mace to protect praying sages in a forest ashram from shadowy demon warriors',
 'c31': f'{SITA} blessing kneeling {MONKEY} in a moonlit garden, glowing jewels and orbs floating around in lotus light',
 'c32': f'{HAN}, kneeling holding a glowing golden pot of divine nectar, soft light and incense smoke',
 'c33': 'devotee singing a bhajan with small cymbals in an old stone temple, oil lamps, golden light rays from above',
 'c34': 'glowing soul ascending a path of light through the clouds to a golden divine city of palaces in the sky',
 'c35': 'Indian family doing aarti with a brass lamp before a Hanuman idol at a home shrine, marigold garlands, warm evening light',
 'c36': f'{HAN}, smashing dark iron chains with his mace, freeing a kneeling devotee in a burst of light',
 'c37': f'{HAN}, blessing a kneeling disciple with raised palm on a river bank at sunrise',
 'c38': 'devotee praying with a rudraksha mala in a temple at dawn, broken chains on the floor, rays of divine light',
 'c39': 'Lord Shiva meditating on snowy Mount Kailash, crescent moon in his hair, serene glowing light, starry sky',
 'c40': 'old saint Tulsidas with white beard and saffron robe praying with folded hands by a river at dawn, glowing heart light',
 'd3': f'{HAN}, kneeling in deep devotion inside a glowing temple, a radiant golden vision of Lord Rama and Sita above him, divine light',
 'jai1': 'Lord Rama, blue-skinned Hindu god prince with golden crown and a bow, standing serenely in a golden temple, lotus flowers, divine light',
}
def full(sid): return P[sid] + STY + NEG
