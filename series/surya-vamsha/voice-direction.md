# आवाज़ का निर्देश (Voice direction)

The narrator's voice for every episode: **confident, deep, slow and weighty Hindi**. Use this
sheet to brief a voice artist, or to set up a text-to-speech voice.

> This is a description of a *style*. Do not clone, imitate or credit any real actor's voice
> without their written permission and a licence, and never claim in the video that a famous
> person is narrating.

## The voice in one line

A grave, unhurried storyteller who sounds sure of every word, never loud, and lets silence do half
the work.

## For a voice artist

| quality | what to aim for |
| --- | --- |
| register | low baritone, chest voice; never strained or nasal |
| pace | about 110 words a minute; slower on every **सूत्र-पंक्ति** |
| emphasis | words in **bold** are stressed by slowing down and lowering the voice, not by getting louder |
| pauses | `…` is a short breath (about half a second); `[विराम]` is a full two-second silence; keep both |
| diction | clean शुद्ध हिंदी; Sanskrit words (श्लोक, नाम) said fully and carefully, never rushed |
| attitude | authority without anger; warmth in the reflective lines; real stillness in the sad scenes |
| questions | when the script asks the viewer something, say it directly to them, then wait |

**Audition test:** have the artist read the E01 hook and one सूत्र-पंक्ति. Pick the take where the
pauses feel natural rather than performed.

## For text-to-speech

`make_narration.py` turns every script into narration files in `narration/`:

- `epNN.txt` has the spoken words only, for a human narrator.
- `epNN.ssml` is ready for a neural TTS service. It defaults to Azure's stock male Hindi neural
  voice `hi-IN-MadhurNeural`, slowed (rate −12%) and lowered (pitch −6%), with the marked pauses
  turned into real silences.

Use a service whose licence allows commercial YouTube use with your own account, for example
Azure AI Speech or ElevenLabs on a paid plan. Pick a deep male Hindi stock voice, then adjust rate
and pitch at the top of `make_narration.py` until a test paragraph sounds right.

YouTube asks creators to disclose realistic synthetic content when uploading; mark the videos as
using a synthetic narrator if you use TTS.
