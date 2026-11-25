# Production stack: free and cheap options

Evidence about the reference format (from metadata, auto-captions and ~5 s storyboard frames;
the audio itself could not be heard): AI still images in one consistent cartoon style, roughly
170-250 per 14 minutes, slow pan/zoom on each still with cuts/short fades, a few shots where
one object moves on a fixed background (image-to-video or a moving layer), one steady narrator
with no ad-libs (likely premium TTS, unconfirmed), music unknown. **No AI video generator is
needed for this look**, which is the main saving: video generators bill per second (~840 s of
footage per video plus retries) and keep characters and text less consistent.

## Per-step options (cheapest first)

### Script
Claude (this session). Ask for the formula in `script-formula.md`, one sentence per line.

### Images (Claude cannot make raster images; pick one)
1. **Gemini image models via a free Google AI Studio key** - strong style consistency with a
   reference image, decent text; free-tier rate limits mean ~170 images may take a day or two.
2. **Local FLUX.1-schnell (Apache-2.0) or SDXL** - free per image if you have a GPU
   (FLUX comfortable at ~12 GB+ VRAM; SDXL on 8 GB). Lock the look with a style LoRA trained on
   your own images or IP-Adapter. Tools: ComfyUI, Forge, or diffusers.
3. **Paid subscriptions** (ChatGPT image generation, Midjourney, others) - highest quality,
   good consistency; check current prices yourself.
4. **Image-to-video** only for 2-5 hero shots per video (ships, cavalry, crowds). Drop the `.mp4`
   into `images/` and point the shot's `image` at it; `assemble.py` handles it.

Rough count: minutes x 12-17 images (one per 3.5-5 s). 14 min ≈ 170-240.

### Voice
| option | cost | Hindi voices | English voices | notes |
|---|---|---|---|---|
| **edge-tts** (default in `make_voice.py`) | free | `hi-IN-MadhurNeural` (m), `hi-IN-SwaraNeural` (f) | `en-US-GuyNeural`, `en-US-AndrewNeural`, `en-GB-RyanNeural`, `en-IN-PrabhatNeural`, `en-IN-NeerjaNeural` | needs `speech.platform.bing.com`; unofficial API, can change; good quality |
| **ElevenLabs** (`--backend elevenlabs`) | paid per character | multilingual models: `eleven_multilingual_v2`, `eleven_v3`, `eleven_flash_v2_5`, `eleven_turbo_v2_5`; Hindi narrator voices in the voice library | many | best quality; one 14-min video ≈ 13k characters per language (~26k for EN+HI) |
| **Kokoro-82M** (local, Apache-2.0, CPU ok) | free | `hf_alpha`, `hf_beta` (f), `hm_omega`, `hm_psi` (m), lang code `h` | very good | Hindi usable, less natural; needs your own wrapper (write per-line WAVs, then use the same join logic) |
| **Piper** (local) | free | `hi_IN` pratham, priyamvada, rohan | many | fastest, more robotic; drafts |

Delivery tips: one calm, steady narrator; `--rate -5%` on edge-tts; leave the 0.6 s act-break pauses.
Claude cannot listen to the result; the user should check the first 30 s before generating images.

### Motion and assembly
`scripts/assemble.py` (ffmpeg 6.1+): zoompan Ken Burns on a 2x upscaled copy (no jitter),
0.4 s crossfades, titles/captions via libass, music ducking, loudness to -14 LUFS, 16:9 or 9:16.
A 26 s, 6-shot test renders in ~16 s on 4 cores; expect a 14-minute video in roughly 10-20 minutes
on a normal PC. Alternative for template-heavy channels: Remotion (Node).

### Captions
`make_voice.py` writes an SRT from exact per-line timings (chunks of ≤42 characters). For
word-level timing use faster-whisper (`large-v3`, `word_timestamps=True`) or ElevenLabs speech-to-text.
Upload both Hindi and English SRTs to YouTube even if you also burn one in.

### Music (free)
YouTube Audio Library (filter "attribution not required"), Pixabay Music, incompetech (attribution).
`assemble.py --music bed.mp3` loops it, sets it to -18 dB and ducks it under the voice.

## Cost per 14-minute bilingual video (cash)
| route | script | images | voice | edit | total |
|---|---|---|---|---|---|
| all-free | Claude | AI Studio free tier or local GPU | edge-tts / Kokoro | ffmpeg | ~₹0 (time + electricity) |
| quality | Claude | free tier or one image subscription | ElevenLabs ~26k chars | ffmpeg | one low-tier TTS plan covers a few videos/month |
| AI video generator | - | ~840 s of generated clips + retries | - | - | many times the image route, worse consistency |

Prices change; check current plans yourself before committing.

## Environment notes
- edge-tts fails in many sandboxes (DNS error or proxy 403 on `speech.platform.bing.com`, then
  "No server date in headers"). Run voice on your own PC or use `--backend elevenlabs`.
- ElevenLabs key: `ELEVENLABS_API_KEY` env var (in a proxied cloud session a credential may be injected by the proxy).
- Fonts: Devanagari needs a font with Devanagari glyphs installed or passed via `--fontsdir`
  (Noto Sans Devanagari, Mukta, Hind; on Windows "Nirmala UI" works via `--font "Nirmala UI"`).
