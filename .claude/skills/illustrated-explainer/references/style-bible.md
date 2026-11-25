# Style bible: flat "block-head" editorial cartoon

Measured from 169 storyboard frames of a reference video in this format (one frame every
~5 s, pixel stats with PIL). Use it as a description of a general look; give your channel its
own variation (palette tweak, a recurring host character) rather than cloning anyone.

## Look
- **Characters**: large rounded white square head (#FCF8E3, no skin tone, no nose), ~1/3 of body height;
  two solid black oval dot eyes; thick short black eyebrow dashes that carry all emotion; single-line or
  small open mouth; small C-shaped ears; solid black scribbly hair/topknot (grey/white for elders); thin
  uniform black stick limbs and neck; black mitten hands; small oval feet.
- **Emotion = eyebrows**: angled down to the centre = anger/determination; tilted up in the middle =
  worry/sadness; flat = neutral. Sweat drops / motion lines for comedy.
- **Clothing**: flat colour cut-out shapes with bold outline and 1-3 fold lines over the stick body.
  Identity comes from costume, headwear, facial hair and props only.
- **Lines**: bold even black ink on characters (~6-10 px at 1080p); thinner brown-black on backgrounds.
- **Shading**: characters flat; backgrounds soft two-tone cel shading, gentle gradients, light haze.
- **Backgrounds**: richer storybook scenery (cities, temples, forts, harbours, aerial towns with tiny
  figures); plain cream paper for gags/diagrams; dark charcoal with a light pool for drama.
- **Titles**: ~1 every 20-25 s, mostly at an era/name start, format `NAME — YEAR` (e.g. `DELHI SULTANATE — 1206`),
  top-centre in empty sky. Add them in assembly (shots.json `title`), not in the image.
- **No** lower-thirds, logos or watermark in the reference; muted earthy colours (~34% of pixels saturated).

## Palette
| role | hex |
|---|---|
| paper / head white | #FCF8E3 |
| ink | #0A0C09 |
| dark spotlight bg | #24241F, #2E3333 |
| sand / ochre | #D7C19F, #BEA885, #A9926A |
| earth browns | #897B5E, #695D46, #613E2F |
| terracotta / brick / saffron cloth | #BB704E |
| royal maroon | #723A30, #552B2C; title red #863135 |
| olive cloth / foliage | #8E9554, #6A7241 |
| sky | #9AD1EA, #85C0E0 |
| sea / river | #2F678A, #5891AD |
| stone grey | #8E908A, #606769 |
| map empire red | #C1694D |

## MASTER STYLE BLOCK (prepend to every image prompt, unchanged for the whole video)
```
Flat 2D editorial cartoon illustration, 16:9 widescreen, clean digital ink. CHARACTERS: minimalist "block-head" people - each head is a large rounded white square (off-white #FCF8E3, no skin tone, no nose), two solid black oval dot eyes, thick short black eyebrow strokes that carry the emotion, a single-line or small open mouth, tiny C-shaped ears, solid black scribbly curly hair or bun on top; bodies are thin uniform black stick lines for arms, legs and neck, small black mitten hands, small black oval feet; heads about one third of body height. Clothing drawn as simple flat colour shapes with bold black outline and only 1-3 fold lines, layered over the stick body (draped dhoti, saree, robe, sash, turban, crown as the period requires). Bold even black outlines on characters, thinner brown-black lines on backgrounds. BACKGROUNDS: detailed but flat storybook-cartoon scenery with soft two-tone cel shading, gentle gradients and light atmospheric haze; muted earthy palette of sand #D7C19F, ochre #A9926A, terracotta #BB704E, maroon #723A30, olive #8E9554, stone grey #8E908A, sky blue #9AD1EA, deep sea blue #2F678A, cream paper #FCF8E3. Characters stay flat and unshaded against the richer backgrounds. Clear readable staging, gentle humour, no photorealism, no 3D, no gradients on faces, no extra facial features, no realistic hands. Do not render any lettering, inscriptions or writing unless the prompt quotes exact text; leave clean empty space at the top for a title.
```
Models that ignore hex codes: keep the colour names, drop the hex values.

## Shot-type mix (reference, 169 frames)
| shot type | share | notes |
|---|---|---|
| two-shot / group dialogue (medium) | 31% | the workhorse; two characters reacting to each other |
| wide landscape / establishing | 27% | often the titled shot at an era start; aerial towns with tiny figures |
| close-up reaction | 11% | one face, eyebrows doing the work |
| single character medium | 10% | hero intro, ruler on a throne |
| object insert | 9% | seal, edict rock, manuscript, coins, map on a desk |
| map | 6% | relief or political, empire in flat red |
| dark spotlight | 4% | regret, death, turning points |
| text card / infographic | 2% | giant numeral, pie chart, plate diagram |

Rhythm: wide/establishing (+title) → dialogue two-shot → close-up or insert → next beat.
One new image per sentence or clause (every 10-15 spoken words, 3-5 s). Visuals are literal:
show exactly what the line says. Reusing an image with a different crop 30 s later is fine.

## Example shot prompts (put the master block first)
1. **Wide establishing**: Wide aerial three-quarter view of a planned Bronze-Age brick city beside a broad river at golden hour, flat-roofed mud-brick houses in a grid, covered drains, a granary, dozens of tiny block-head townsfolk carrying pots and baskets, river boats with square sails, empty pale sky across the top third.
2. **Map**: Stylised relief map of the Indian subcontinent seen from above, ocean deep blue with light wave strokes, snow-capped Himalaya along the north, rivers as thin pale-blue lines, a large region across the north and centre filled flat terracotta-red marking an empire, neighbouring regions in muted olive, sand and grey, no labels, no lettering.
3. **Two-shot dialogue**: Medium two-shot inside a sandstone palace hall: on the left a seated emperor in a cream turban with a red jewel and white feather and a maroon robe with gold trim, eyebrows angled down in a stern frown, pointing at a scroll; on the right a nervous advisor in an olive robe and beige turban, eyebrows tilted up in worry, small sweat drop; arched window behind showing a distant fort under a blue sky.
4. **Close-up reaction**: Tight close-up of one block-head farmer filling most of the frame, eyebrows raised and tilted up in dismay, small wavy worried mouth, black curly hair, saffron cloth on the shoulder, holding a withered rice stalk near the face, blurred dry cracked field behind.
5. **Object insert**: Close-up of a small square carved soapstone seal showing a humped bull, lying on bare earth, lit by a soft warm spotlight pool, the rest of the frame dark charcoal, no inscription characters.
6. **Infographic**: Cream paper background, a huge thick black numeral zero standing in the centre like a sculpture, two small block-head scholars on either side, one in an olive robe and one in a saffron robe with a turban, both stroking their chins, soft ground shadow, empty space at the top for a title.
7. **Dark spotlight**: Dark charcoal background with a single diagonal shaft of pale light; a lone king in a maroon robe and gold circlet sits slumped on a stone step, eyebrows tilted up in regret, a battered bronze helmet on the ground beside him in the light, long soft shadow.
8. **Single medium (hero intro)**: Medium shot of a confident young ruler on a carved wooden throne with a red cushion, maroon robe and gold sash, gold headband, eyebrows angled down with a slight smirk, two spear-holding guards in olive tunics on either side, deep blue wall with a hanging banner behind, clear empty band across the top for a name title.

Prompt-writing rules: describe position (left/right), costume colours, eyebrow state, one prop,
one background; ask for empty space at the top when the shot has a title; say "no lettering".
Use real landmarks by name when needed (models render famous monuments well).

## Character consistency
1. Write a **character card** once and paste it verbatim into every shot with that person:
   `KING_A = block-head man, black topknot, thin black moustache, gold circlet with red gem, maroon robe with gold trim over a cream dhoti, gold armband`.
   All faces are the same white square, so identity lives in hair, facial hair, headwear, accessories and 2-3 colours.
2. Make a **reference sheet** per main character (front, three-quarter, side; neutral/angry/sad) on cream paper; keep the best.
3. With a reference-capable image model (edit/reference image input), pass the sheet + card + master block and
   describe only pose, action and eyebrows.
4. Fix model, aspect ratio and style block for the whole video; reuse the seed within a scene; for a recurring set,
   generate one empty background plate and place characters on it.
5. Express emotion only with eyebrow wording, never abstract emotion words.
6. At scale: after 25-40 of your **own** on-style images, train a small style LoRA (SDXL/FLUX) and generate locally
   for almost nothing. Train only on images you made.
7. Reuse: recrop an image for a second beat; Ken Burns on every still; image-to-video only for 2-5 hero shots (ships, cavalry).

## Titles and Hindi
Generate every image without text, then let `assemble.py` draw `title` fields with libass (shapes
Devanagari correctly). For a nicer look download a bold condensed font (Hindi: Mukta ExtraBold or Hind Bold;
English: Oswald or Bebas Neue) into `fonts/` and pass `--fontsdir fonts --title-font "Mukta ExtraBold"`.
One image set then serves both the Hindi and English versions.
