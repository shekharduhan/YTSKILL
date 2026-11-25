# Script formula: "The ENTIRE History of [X] in [N] Minutes"

Derived from measuring one successful 14-minute example of the format (844 s, 2,193 words,
auto-caption transcript). The audio could not be heard, so delivery notes are inferred from
the text only. Quotes below are short examples for study; write your own lines.

## Measured benchmarks (14-minute reference)

| metric | value | use as target |
|---|---|---|
| pace | 156 words/min | English: minutes x 155 words |
| sentences | ~165, avg 13.1 words, median 12, longest 30 | avg ≈ 13 words |
| punch lines (≤5 words) | 21 (one every ~40 s) | one short line every 30-45 s |
| long sentences (≥20 words) | 25 | max ~1 in 7 |
| questions | 4 total (thesis, callback, comment prompt) | almost none |
| numbers | ~4 per minute; 12 sentences start "In [year]," | date at the start of the sentence |
| hedges ("historians debate", "estimates", "probably") | ~16 (one per ~50 s) | ~1 per minute |
| sections | 11, each 6-12% of words | 8-12 eras |
| intro / outro | none: line 1 is the story; ends on the comment prompt and next-video line | no channel intro |
| sound markers in captions | 4, at act breaks (probably stings; unverified) | 3-4 act breaks |

Time is compressed unevenly: 100 million years got 49 s, the last 75 years got ~75 s.
Roughly 38% ancient, 25% medieval, 35% colonial-to-modern. Recent periods get more words per century.

## Structure

**Word budget**: total = minutes x 155 (English) or x 130 (Hindi). Cold open 6-7%,
eras 6-12% each, modern era + ending ~15%.

**[0-6%] Cold open, 3 beats, no channel intro**
1. "[Deep-time number] years ago, [physical event with a strong verb: slammed / drifted / flooded]. [Consequence]."
2. Present-tense wonder fact: "Today you can still [find/see] [surprising object] [in surprising place]."
3. "That [event] shaped almost everything in this story." + three consequences
   (e.g. a mountain wall, river plains, monsoon trade). **Plant all three: pay each off later.**

**[by ~0:35] Thesis**
- "So, here is our question. How did [fragmented start: tribes / kingdoms / languages / faiths] become [modern X]?"
- Paradox: "[Modern X] is only [age] years old, and most of this story happened long before anyone could imagine it."

**Each era (120-260 words)**
1. Time/place pivot, one sentence, no "Chapter 3": "Around [date], …" / "[Region], meanwhile, was never a sideshow." / "Over the following centuries…"
2. 2-3 concrete details: objects, buildings, trade goods; big numbers with a comparison ("as tall as a 20-story building").
3. One signposted curiosity: "And here is the mystery: …" / "And here we have something rare: …"
4. One myth-correction: "It is often called [myth]. It looks more like [nuance]." / "Be careful with the popular story of …" / "It was less a great battle than a deal."
5. One cause chain with repeated words: "Farms created surpluses, and surpluses created towns and kings."
6. One hedge with a named source: "Historians still debate …" / "Estimates range from A to B, with many historians near C."
7. Exit: collapse line ("Yet, within about 50 years, the empire was gone."), legacy line ("…we still use it every day."), or bridge ("So, when [next power] arrived, [X] was crowded with rivals.").

**Modern era**: founding document/date, 2-3 stress tests ("It survived real tests."), an economic
turning point, then "Today, [X] is [superlative], with [strength], [problem], and [unresolved issue]."

**[last ~6%] Ending**
1. Repeat the thesis almost word for word: "So, how did [X] become [Y]?"
2. Triple negation: "Not through one conqueror, one religion, or one idea."
3. Three-force synthesis that pays off the cold-open plants: "[Geography] made variety. [Empires A, B, C] linked … but none held everything for long. [Late force] created [thing] and also [its opposite]."
4. Mirror of the opening paradox: "[X] is old. [X] as a nation is young."
5. Comment prompt with three named options: "Which mattered most? [A], [B], or [C]?"
6. Next video tied to the story: "If you want to see where [element of this story] came from, watch our history of [neighbour] next."

## Ten reusable patterns
1. Deep-time hook, then a present-tense wonder fact.
2. Geography as the cause, planted early, paid off in the conclusion.
3. Thesis question labelled as such ("here is our question").
4. "And here is the [mystery/something rare]" signpost before a curiosity.
5. Myth-correction ("the popular story is too simple").
6. "No single cause" / "not one great invasion".
7. Cause chain with repeated words (A created B, and B created C).
8. Short collapse sentence to close an era.
9. Balanced hedging that names who disagrees.
10. Irony/paradox line, mirrored in two short sentences at the close.

## Checklist before recording
- [ ] Word count within ±5% of budget.
- [ ] Thesis question by ~0:35; repeated in the ending.
- [ ] Three cold-open plants each paid off.
- [ ] ~4 numbers/min, dates first in their sentences, approximations marked ("around", "lagbhag").
- [ ] ≥2 myth-corrections, ~1 hedge/min, every disputed number given as a range with a source.
- [ ] Avg sentence ≈13 words, a ≤5-word punch line every 30-45 s.
- [ ] ≤4 questions; only "we"/"our question", no "I", no sponsor talk.
- [ ] One sentence per line in the TTS file, `## ` section lines, blank line at act breaks.

## Hindi / Hinglish adaptation (inference; no Hindi version of the reference exists)
- **Length**: Hindi needs more words for the same meaning (postpositions, hai/tha/ki). Plan ~130 words/min;
  a 14-minute Hindi script is ~1,800-1,900 words. Cut an era or details rather than speeding up the voice.
- **Sentences**: keep to ~13 words or fewer: the verb comes last in Hindi, so long sentences drag.
- **Dates**: keep numerals ("1526 में", "लगभग 320 ईसा पूर्व"); for mass audiences gloss BCE dates
  ("आज से करीब 4,600 साल पहले"). "around" → लगभग / करीब. Avoid heavy shuddh terms unless you want a formal register.
- **Signposts**: thesis "तो सवाल ये है…"; curiosity "और यहीं है असली रहस्य…"; myth-correction
  "पॉपुलर कहानी थोड़ी ज़्यादा सिंपल है…" / "इसे अक्सर जीत कहा जाता है, लेकिन असल में…";
  collapse "और 50 साल के अंदर… साम्राज्य ख़त्म।"; closing mirror "भारत पुराना है। भारत एक राष्ट्र के रूप में नया है।"
- **TTS spelling**: write the TTS file in Devanagari. Latin-script Hinglish is read poorly by Hindi voices.
  Keep proper nouns consistent across both languages.
- **Sensitive topics** for Indian audiences (migration theories, caste origins, specific rulers, Partition
  deaths, borders/Kashmir): keep the hedges and sources in the Hindi version too; they prevent
  misinformation flags and comment wars.
- **Bilingual workflow**: English master → Hindi adaptation; identical names/numbers/title cards so one
  image set serves both voiceovers; act-break stings need no translation.
