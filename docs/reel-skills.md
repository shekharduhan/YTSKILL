# Skills from the 10 Facebook reels

What each reel actually showed, what got installed in this repo, and what did not (and why).
All of these were watched in full: the speech was transcribed and the on-screen text read from frames,
because several reels only name the repo on screen.

## Installed in this repo

These are switched on in [`.claude/settings.json`](../.claude/settings.json), so any Claude Code session
opened in this repo (cloud or your own computer) installs them automatically and asks you to trust them
the first time. Every one was checked with NVIDIA SkillSpector first. Its "HIGH" flags were all ordinary
tool behaviour (reading an API key from `.env` to call Gemini, a local browser on `localhost`, a benchmark
script), not malware.

| Plugin | From reel | What it gives you | Try |
| --- | --- | --- | --- |
| `watch` ([bradautomates/claude-video](https://github.com/bradautomates/claude-video)) | 4 | Claude watches a video URL: downloads it, pulls frames, transcribes. | `/watch <youtube url>` |
| `replica-skill` ([Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill)) | 6 | 11 skills to clone an app: recon, architect, design, build, backend, test, diff, entrepreneur, brand, launch, deploy. | `/replica-recon` |
| `instagram-agent` ([Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)) | 9 | 13 skills: `ig-reel`, `ig-viral`, `ig-caption`, `ig-comment`, `ig-reply`, `ig-profile`, `ig-plan`, `ig-story`, `ig-carousel`, `ig-dm`, `ig-repurpose`, `ig-audit`, `ig-human`. Same author as this repo's YouTube skills. | `/ig-reel` |
| `task-observer` ([rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all)) | 1 | Watches how you work and suggests new skills or fixes to existing ones. | `/task-observer` |
| `claude-code-setup` ([anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup)) | 1 | Anthropic's own plugin: scans the codebase and recommends hooks, skills, subagents, MCP servers. | `/claude-automation-recommender` |
| `ponytail` ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)) | 2 | Pushes Claude toward the smallest code that works; fewer tokens. Has 4 optional settings. | `/ponytail-help`, `/plugin configure ponytail@ponytail` |
| `lemo-opuscar` ([lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)) | 2 | 99 animation and film styles made in code, for explainer videos. | `/lemo-opuscar` |
| `claude-mem` ([thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)) | 1 | Memory across sessions. Runs a local background worker. Most useful on your own computer, because cloud containers are wiped. | `/mem-search` |

### Also switched on

| Plugin / skill | What it gives you | Try |
| --- | --- | --- |
| `youtube-agent` (this repo's own 11 skills) | Scripts, titles and thumbnails, edit lists, retention, Shorts, chapters, SEO, comments, plans, audits, niche research. Loaded from this repo via the `youtube-agent-skill` marketplace. | `/youtube-agent:yt-script` |
| `illustrated-explainer` (in `.claude/skills/`) | Long narrated explainers made of AI still images with pan/zoom, Hindi or English voice, ffmpeg assembly. Learned from an illustrated history video on YouTube. | `/illustrated-explainer` |

The full learning guide is [`free-video-with-claude-code.pdf`](free-video-with-claude-code.pdf), and
[`demo-reel-code-se-video.mp4`](demo-reel-code-se-video.mp4) is a 23-second Reel made entirely in code
with Lemo-Opuscar.

### Installed but switched off

| Plugin | From reel | Why it is off |
| --- | --- | --- |
| `ecc` ([affaan-m/ECC](https://github.com/affaan-m/ECC), the "288k stars" repo) | 7 | 427 skills and 72 agents. It adds about **50,000 tokens to every session**, which eats your usage limit faster than the token-saving plugins save. Turn it on only when you want it: `claude plugin enable ecc@ecc --scope project`. |

## For your own computer only

These need your Chrome logins or a local proxy, so they don't belong in a throwaway cloud container.

**Agent Reach** (reel 2): reads LinkedIn, Instagram, X and Reddit through its own browser, which copies your
Chrome logins (the project itself recommends using a secondary account). Do **not** `pip install agent-reach`:
the project warns that the PyPI package of that name is someone else's.

```bash
uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip
```

```bash
agent-reach setup
```

**Headroom** (reel 1): compresses tool output before it reaches the model. It works by starting Claude
through a local proxy:

```bash
pip install "headroom-ai[all]"
```

```bash
headroom wrap claude
```

**SkillSpector** (reel 2): NVIDIA's scanner for skills. Run it on any skill before you install it:

```bash
uv tool install --python 3.13 git+https://github.com/NVIDIA/skillspector.git
```

```bash
skillspector scan https://github.com/<owner>/<repo> --no-llm
```

## Not installed, on purpose

**Free-token routers**: OmniRoute (reels 1, 10), FreeLLMAPI (reels 2, 10), Nara Router with Mimo models
(reel 5). They point Claude Code at a different server (`ANTHROPIC_BASE_URL`), so it stops being Claude.
Every prompt and every file Claude reads goes to whoever runs that router, or to the dozens of free providers
it pools. Nara Router also asks for Telegram verification, and the reel's link is a referral link. If you
try one anyway, use it in a throwaway folder with no private code or keys.

**MoneyPrinterTurbo** (reel 3, [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)):
a standalone Python app that makes short videos from a topic. It is not a Claude skill. If you want it, run
it on your computer with its own instructions.

**Eromify** (reel 8): a claude.ai custom connector (`api.eromify.com/mcp`) for generating an AI influencer
to post on Fanvue, a subscription platform. It's not something that installs into Claude Code; you would add
it in claude.ai → Customize → Connectors yourself.

## Reel by reel

1. **Harshit Davee**: 5 plugins: OmniRoute, Claude Mem, Headroom, Claude Code Setup, Task Observer.
2. **Nivedan Rathi**: Agent Reach, Lemo-Opuscar, Ponytail, FreeLLMAPI, NVIDIA SkillSpector.
3. **EzSnippet**: MoneyPrinterTurbo.
4. **Champ McCorkle**: claude-video (`/watch`): Claude watches YouTube and turns it into a skill.
5. **Afzal**: 21-minute walkthrough of Nara Router and Xiaomi's Mimo v2.5 models in Claude Code and OpenCode.
6. **Shashwatagarwal**: Replica, 11 skills to clone an app.
7. **Omkar Desai**: ECC (everything-claude-code), the 288k-star repo.
8. **daruseai**: Eromify connector, then Fanvue.
9. **Harshit Davee**: Instagram Agent Skill (13 skills).
10. **aradhyspeaks.ai**: FreeLLMAPI and OmniRoute.
