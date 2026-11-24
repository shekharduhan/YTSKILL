"""Build the publishing kit: channel set-up text for every platform plus a post for each episode.

    python3 make_publish_kit.py

Reads episodes.psv and each epNN-*-hindi.md (title, thumbnail words, sources, hook lines, next
episode). Writes:
  publishing-kit.md    channel name, bios, profile fields, playlists, and all 84 episode posts
  publishing-kit.csv   the same episode posts, one row per episode, for spreadsheets / schedulers
  captions/epNN.srt    Hindi subtitles, for every episode whose narration is already rendered
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CHANNEL = "सूर्यवंश कथा | Suryavansh Katha"
HANDLE = "@SuryavanshKatha"
TAGLINE_HI = "हर कथा, स्रोत के साथ।"
TAGLINE_EN = "Every story, with its source."

KINGS = {  # king -> (Hindi name, hashtags)
    "Ikshvaku": ("इक्ष्वाकु", ["#इक्ष्वाकु", "#Ikshvaku"]),
    "Mandhata": ("मान्धाता", ["#मान्धाता", "#Mandhata"]),
    "Trishanku": ("त्रिशंकु", ["#त्रिशंकु", "#Trishanku"]),
    "Harishchandra": ("राजा हरिश्चंद्र", ["#राजाहरिश्चंद्र", "#Harishchandra"]),
    "Sagara": ("राजा सगर", ["#राजासगर", "#KingSagara"]),
    "Bhagiratha": ("भगीरथ", ["#भगीरथ", "#Bhagiratha", "#गंगावतरण"]),
    "Raghu": ("राजा रघु", ["#रघुवंश", "#Raghuvansh"]),
    "Aja and Dasharatha": ("अज और दशरथ", ["#राजादशरथ", "#Dasharatha"]),
    "Shri Ram": ("श्रीराम", ["#श्रीराम", "#Ramayan", "#रामायण"]),
    "Lav and Kush": ("लव और कुश", ["#लवकुश", "#LavKush", "#रामायण"]),
}
CORE = ["#सूर्यवंश", "#Suryavansh", "#भागवतपुराण", "#हिंदूपौराणिककथा", "#IndianMythology",
        "#BhagavataPurana", "#पौराणिककथा", "#सनातनधर्म", "#HindiKahani", "#Mythology"]
DISCLOSE = ("वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित\n"
            "Narration: AI voice (ElevenLabs) · Illustrations: AI-generated · Script: written from the cited texts")


def clean(s):
    s = re.sub(r"\[विराम\]", "", s).replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def field(text, name):
    m = re.search(rf"^{name}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def episode(path):
    t = open(path, encoding="utf-8").read()
    copy = t.split("## कॉपी ब्लॉक")[-1]
    title = field(copy, "शीर्षक") or clean(re.search(r"\*\*शीर्षक[^:]*:\*\*\s*(.+)", t).group(1))
    thumb = field(copy, "थंबनेल")
    nxt = field(copy, "अगला")
    src = clean(re.search(r"\*\*स्रोत:\*\*\s*(.+)", t).group(1))
    body = t.split("\n---\n", 1)[1]
    hook = body.split("## हुक", 1)[-1]
    hook = re.split(r"(?m)^## ", hook, maxsplit=1)[0]
    lines = [clean(l) for l in hook.splitlines()
             if l.strip() and "[स्क्रीन" not in l and not l.startswith(">")]
    lines = [l for l in lines if l.strip(" …")]
    opener, n = [], 0
    for l in lines:
        opener.append(l); n += len(l)
        if n > 220 or len(opener) >= 4:
            break
    sections = re.findall(r"(?m)^## (.+)$", body.split("## जाँच लें")[0])
    return dict(title=title, thumb=thumb, next=nxt, src=src, hook="\n".join(opener),
                hook1=opener[0] if opener else "", sections=sections)


def chapters(ep):
    """YouTube chapters from rendered narration timings, if the narration exists."""
    if not os.path.exists(os.path.join(HERE, "audio", f"ep{ep:02d}.mp3")):
        return None
    try:
        import assemble
        md = glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0]
        secs, _ = assemble.section_times(md)
        names = re.findall(r"(?m)^## (.+)$", open(md, encoding="utf-8").read().split("\n---\n", 1)[1]
                           .split("## जाँच लें")[0])
        return [(a, n) for (a, _), n in zip(secs, names)]
    except Exception as e:  # cache missing: no chapters rather than a wrong guess
        print("chapters skipped for", ep, e)
        return None


def stamp(s, srt=False):
    h, m, sec = int(s // 3600), int(s % 3600 // 60), s % 60
    if srt:
        return f"{h:02d}:{m:02d}:{int(sec):02d},{int(round((sec % 1) * 1000)) % 1000:03d}"
    return f"{m}:{int(sec):02d}" if h == 0 else f"{h}:{m:02d}:{int(sec):02d}"


def write_srt(ep):
    """Hindi subtitles from the rendered chunk timings (one cue per spoken chunk)."""
    import eleven_render as er, assemble
    md = glob.glob(os.path.join(HERE, f"ep{ep:02d}-*-hindi.md"))[0]
    items = er.plan(open(md, encoding="utf-8").read())
    texts = [v for k, v in items if k == "text"]
    t, ti, cues = 0.0, 0, []
    for kind, val in items:
        if kind == "pause":
            t += val; continue
        prev = texts[ti - 1] if ti > 0 else None
        nxt = texts[ti + 1] if ti + 1 < len(texts) else None
        d = assemble.dur(er.tts(val, prev, nxt)); ti += 1
        cues.append((t, t + d, val.strip(" …"))); t += d
    os.makedirs(os.path.join(HERE, "captions"), exist_ok=True)
    out = os.path.join(HERE, "captions", f"ep{ep:02d}.srt")
    with open(out, "w", encoding="utf-8") as f:
        for i, (a, b, txt) in enumerate(cues, 1):
            f.write(f"{i}\n{stamp(a, True)} --> {stamp(b, True)}\n{txt}\n\n")
    return out


def main():
    rows = [l.rstrip("\n").split("|") for l in open(os.path.join(HERE, "episodes.psv"), encoding="utf-8")]
    files = sorted(glob.glob(os.path.join(HERE, "ep*-hindi.md")))
    assert len(rows) == len(files), (len(rows), len(files))
    eps = []
    for i, (row, path) in enumerate(zip(rows, files), 1):
        arc, king, en_title, en_thumb, source, promise = row
        e = episode(path)
        e.update(n=i, arc=int(arc), king=king, en=en_title, en_thumb=en_thumb, promise=promise, en_src=source)
        eps.append(e)
    arc_eps = {}
    for e in eps:
        arc_eps.setdefault(e["arc"], []).append(e)
    for es in arc_eps.values():
        for j, e in enumerate(es, 1):
            e["part"], e["of"] = j, len(es)

    out, csv_rows = [], []
    w = out.append
    w(HEADER)
    w("## 5. Playlists (one per king, plus the full series)\n")
    w("| playlist | title | description |\n| --- | --- | --- |")
    w(f"| all | सूर्यवंश कथा: संपूर्ण शृंखला (84 एपिसोड) | मनु से लव-कुश तक, सूर्यवंश की पूरी कथा क्रम से। श्रीमद्भागवत स्कंध 9 पर आधारित, हर कथा के स्रोत स्क्रीन पर। |")
    for a, es in arc_eps.items():
        hi, _ = KINGS[es[0]["king"]]
        w(f"| arc {a} | {hi}: सूर्यवंश कथा भाग {a} ({len(es)} एपिसोड) | {hi} की पूरी कथा, {len(es)} एपिसोड में, एपिसोड {es[0]['n']} से {es[-1]['n']} तक। स्रोत: {es[0]['en_src'].split(';')[0]} आदि, हर एपिसोड में स्क्रीन पर। |")
    w("")
    w("## 6. Every episode\n")
    w("Each episode below has one block per platform. Copy the box as it is. Where the description says "
      "`[link]`, paste that episode's YouTube link once it is up. Chapters are filled in for episodes whose "
      "narration is already rendered; for the others, run `python3 make_publish_kit.py` again after rendering.\n")

    for e in eps:
        hi_king, ktags = KINGS[e["king"]]
        n = e["n"]
        yt_title = e["title"]
        if len(yt_title) + len(" | सूर्यवंश कथा") <= 100:
            yt_title += " | सूर्यवंश कथा"
        tags3 = ["#सूर्यवंश", ktags[0], "#भागवतपुराण"]
        yt_tags15 = list(dict.fromkeys(tags3 + ktags + CORE))[:15]
        ch = chapters(n)
        chap = ("\n".join(f"{stamp(a)} {name}" for a, name in ch) if ch else
                "(अध्याय-समय: रेंडर के बाद यहाँ आएँगे)\n" + "\n".join(f"0:00 {s}" if j == 0 else f"?:?? {s}"
                                                                     for j, s in enumerate(e["sections"])))
        nxt = e["next"] or "(शृंखला का अंतिम एपिसोड)"
        yt_desc = (f"{e['hook']}\n\n"
                   f"सूर्यवंश कथा · एपिसोड {n} / 84 · {hi_king} (भाग {e['part']} / {e['of']})\n"
                   f"In this episode: {e['promise']}\n\n"
                   f"📜 स्रोत: {e['src']}\n"
                   f"हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।\n\n"
                   f"⏱ अध्याय\n{chap}\n\n"
                   f"▶ अगला एपिसोड: {nxt}\n"
                   f"▶ पूरी शृंखला (प्लेलिस्ट): [link]\n\n"
                   f"{DISCLOSE}\n\n"
                   + " ".join(yt_tags15))
        yt_tag_field = ", ".join([e["title"], e["en"], hi_king, e["king"], "सूर्यवंश", "Suryavansh",
                                  "सूर्यवंश कथा", "भागवत पुराण", "Bhagavata Purana", "Srimad Bhagavatam",
                                  "हिंदू पौराणिक कथा", "Hindu mythology", "Ikshvaku dynasty", "रामायण",
                                  "Hindi story", "पौराणिक कथा"])
        while len(yt_tag_field) > 480:
            yt_tag_field = yt_tag_field.rsplit(",", 1)[0]
        short_tags = [ktags[0], "#सूर्यवंश", "#पौराणिककथा", "#IndianMythology", "#Hindi"]
        ig = (f"{e['hook1']}\n\n"
              f"{e['title']}\n"
              f"सूर्यवंश कथा · एपिसोड {n} 🔱\n\n"
              f"📜 स्रोत: {e['src'].split('·')[0].strip()}\n"
              f"पूरा एपिसोड YouTube पर, लिंक बायो में।\n"
              f"आप क्या करते इस जगह? कमेंट में बताइए 👇\n\n"
              + " ".join(short_tags))
        fb = (f"{e['hook']}\n\n"
              f"👉 {e['title']} (सूर्यवंश कथा, एपिसोड {n})\n"
              f"📜 स्रोत: {e['src']}\n\n"
              f"पूरा वीडियो देखें: [link]\n"
              f"अगर कथा अच्छी लगे, तो परिवार के साथ ज़रूर साझा करें 🙏\n\n"
              + " ".join(["#सूर्यवंश", ktags[0], "#पौराणिककथा"]))
        tt = (f"{e['hook1']} 🔱 {e['title']} | सूर्यवंश कथा #{n}\n"
              f"स्रोत: {e['src'].split('·')[0].strip()} · पूरी कथा प्रोफ़ाइल के लिंक पर\n"
              + " ".join([ktags[0], "#सूर्यवंश", "#mythology", "#hinduism", "#storytime", "#hindi"]))
        pin = (f"आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇\n"
               f"अगला एपिसोड: {nxt}")
        thumb = e["thumb"].strip("`") or e["en_thumb"]

        w(f"### E{n:02d} · {e['title']}\n")
        w(f"*{e['en']}* · {hi_king}, भाग {e['part']}/{e['of']} · थंबनेल पर: **{thumb}** (English: {e['en_thumb']})\n")
        w(f"**YouTube title** ({len(yt_title)}/100)\n```\n{yt_title}\n```")
        w(f"**YouTube description**\n```\n{yt_desc}\n```")
        w(f"**YouTube tags field** ({len(yt_tag_field)}/500)\n```\n{yt_tag_field}\n```")
        w(f"**YouTube pinned comment**\n```\n{pin}\n```")
        w(f"**Instagram Reel caption** (9:16 clip of the hook)\n```\n{ig}\n```")
        w(f"**Facebook post** (full video)\n```\n{fb}\n```")
        w(f"**TikTok caption** (9:16 clip of the hook)\n```\n{tt}\n```\n")
        csv_rows.append(dict(episode=n, arc=e["arc"], king=e["king"], hindi_title=e["title"],
                             english_title=e["en"], thumbnail=thumb, youtube_title=yt_title,
                             youtube_description=yt_desc, youtube_tags=yt_tag_field, pinned_comment=pin,
                             instagram_caption=ig, facebook_post=fb, tiktok_caption=tt))

    open(os.path.join(HERE, "publishing-kit.md"), "w", encoding="utf-8").write("\n".join(out))
    with open(os.path.join(HERE, "publishing-kit.csv"), "w", encoding="utf-8-sig", newline="") as f:
        cw = csv.DictWriter(f, fieldnames=list(csv_rows[0]))
        cw.writeheader(); cw.writerows(csv_rows)
    for p in sorted(glob.glob(os.path.join(HERE, "audio", "ep??.mp3"))):
        print("wrote", write_srt(int(os.path.basename(p)[2:4])))
    print("wrote publishing-kit.md and publishing-kit.csv,", len(eps), "episodes")


HEADER = f"""# Publishing kit: सूर्यवंश कथा

Everything to type into YouTube, Instagram, Facebook and TikTok: the channel name, the profile
fields on each platform, and a ready post for each of the 84 episodes. Made by `make_publish_kit.py`
from the scripts, so each caption quotes that episode's own opening lines and sources.

## 1. Channel name

**Recommended: {CHANNEL}**, handle **{HANDLE}** on every platform.

Why this one:
- It names exactly what the channel is: the story (कथा) of the Sun dynasty (सूर्यवंश), from Manu to Lav and Kush. Nothing in it promises more than the videos give.
- Everyone who grew up with the Ramayan knows the word सूर्यवंश, so it reads as familiar and serious, not clickbait.
- People search for it in both scripts: "सूर्यवंश" in Hindi, "Suryavansh" in English. The name has both.
- **Tagline: "{TAGLINE_HI}" ({TAGLINE_EN})** This is what makes the channel stand out. Most mythology channels never say where a story comes from. This one shows the source (भागवत 9.x, वाल्मीकि, तुलसीदास, लोक-परंपरा) on screen in every episode.

Other names, if the handle is taken:

| name | handle | the feel |
| --- | --- | --- |
| रघुकुल कथा \\| Raghukul Katha | @RaghukulKatha | warm and devotional ("रघुकुल रीति सदा चली आई") |
| वंश कथा \\| Vansh Katha | @VanshKatha | short; leaves room for a Chandravansh series later |
| सूर्यकुल \\| Suryakul Stories | @SuryakulStories | modern, good for Reels and TikTok |
| पुराण पथ \\| Puran Path | @PuranPath | broad, if you later cover other Puranas |

**Before you create anything,** check the handle is free on all four platforms on the same day, then register it everywhere at once. I can't check availability from here. If `@SuryavanshKatha` is taken anywhere, use the same fallback everywhere (for example `@SuryavanshKathaHindi`), so viewers find you by one name.

## 2. YouTube

| field | what to enter |
| --- | --- |
| Channel name (max 50) | `{CHANNEL}` |
| Handle | `{HANDLE}` |
| Category (on each video) | Education (or Entertainment) |
| Video language / caption language | Hindi |
| Audience | **No, it's not made for kids** (it's family-friendly, but "made for kids" switches off comments and the mini-player) |
| Altered or synthetic content | Tick **Yes** if a video shows realistic-looking people or events. For these painted illustrations it's usually not required, but the AI voice and AI images are already disclosed in every description below. |
| Links (shown on banner) | Instagram, Facebook page, playlist "संपूर्ण शृंखला" |
| Banner text (2560×1440, keep text in the middle 1546×423) | **सूर्यवंश कथा** · {TAGLINE_HI} · नए एपिसोड हर मंगलवार और शुक्रवार |
| Watermark | the channel logo (a sun disc with a bow, gold on deep red) |
| Channel trailer | the first 60 seconds of Episode 1 (the fish and the flood) |

**Description (paste into Customisation → Basic info):**
```
मनु की नाव को खींचती एक सुनहरी मछली से लेकर… श्रीराम के पुत्र लव और कुश तक।
यह है सूर्यवंश की पूरी कथा: वह वंश जिसमें इक्ष्वाकु, मान्धाता, हरिश्चंद्र, सगर, भगीरथ, रघु, दशरथ और श्रीराम हुए।

84 एपिसोड, लगभग 10-10 मिनट के, ठीक क्रम में।
आधार: श्रीमद्भागवत महापुराण, स्कंध 9 (अध्याय 6 से 12), साथ में वाल्मीकि रामायण, कालिदास का रघुवंशम् और तुलसीदास का रामचरितमानस।

{TAGLINE_HI}
हर एपिसोड में स्क्रीन पर लिखा होता है कि कथा किस ग्रंथ से है। जहाँ कथा लोक-परंपरा की है, वहाँ भी साफ़ बताया जाता है।

नए एपिसोड: हर मंगलवार और शुक्रवार।
शुरुआत यहाँ से करें: एपिसोड 1, "इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया"।

The story of the Sun dynasty (Suryavansh), from Manu to Lav and Kush, in Hindi.
84 episodes based on the Bhagavata Purana (Book 9), with the source shown on screen in every episode.
Narration: AI voice. Illustrations: AI-generated.
```

**Channel keywords (Settings → Channel → Basic info):**
```
सूर्यवंश, सूर्यवंश कथा, Suryavansh, Suryavanshi, भागवत पुराण, श्रीमद्भागवत, Bhagavata Purana, Srimad Bhagavatam, रामायण, Ramayan, श्रीराम, इक्ष्वाकु, रघुवंश, राजा हरिश्चंद्र, भगीरथ, गंगावतरण, पौराणिक कथा, हिंदू पौराणिक कथा, Indian mythology, Hindu mythology, Hindi kahani, धार्मिक कथा
```

## 3. Instagram

| field | what to enter |
| --- | --- |
| Name (searchable, max 30) | `सूर्यवंश कथा Suryavansh Katha` |
| Username | `suryavanshkatha` |
| Category (professional account) | Digital creator, or Education |
| Link | your YouTube channel (or a link page with YouTube + Facebook) |

**Bio (max 150 characters):**
```
🔱 मनु से लव-कुश तक: सूर्यवंश की पूरी कथा
📜 {TAGLINE_HI}
84 एपिसोड · भागवत स्कंध 9
▶ पूरे एपिसोड YouTube पर 👇
```

Story highlights: one per king (इक्ष्वाकु, हरिश्चंद्र, भगीरथ, श्रीराम …), using each arc's best image as the cover.

## 4. Facebook page and TikTok

**Facebook page**

| field | what to enter |
| --- | --- |
| Page name | `{CHANNEL}` |
| Username | `{HANDLE}` |
| Category | Education website, or Digital creator |
| Intro (max 101) | `मनु से लव-कुश तक: सूर्यवंश की पूरी कथा, हिंदी में। {TAGLINE_HI}` |
| Action button | Watch video, pointing to the YouTube channel |

Facebook "About" text: paste the same text as the YouTube description above.

**TikTok**

| field | what to enter |
| --- | --- |
| Name | `सूर्यवंश कथा` |
| Username | `suryavanshkatha` |
| Bio (max 80) | `मनु से लव-कुश तक 🔱 सूर्यवंश की कथा · {TAGLINE_HI}` |
| Link | YouTube channel (TikTok shows a bio link only on business accounts, or after 1,000 followers) |

**TikTok is blocked in India.** It's only worth running if you want viewers abroad: Hindi speakers in the US, UK, Canada, the Gulf, Nepal and Fiji. For viewers in India, put that effort into Instagram Reels and YouTube Shorts.

**How to post on each platform:**
- **YouTube:** the full 16:9 episode. Then 2-3 Shorts (9:16, under 60 s) cut from the hook and the strongest scene, each linking to the full episode ("Related video" field).
- **Instagram and TikTok:** the same 9:16 hook clips as Reels, with the captions below.
- **Facebook:** upload the full video natively (it gets more reach than a YouTube link), and share the Reels there too.
- **Hashtags:** YouTube ignores *all* hashtags if a video has more than 60, and shows the first 3 above the title, so each description below has 15 at most. Instagram now allows 5 per post, so each Reel caption has 5.
- **Disclosure:** every description says the voice and images are AI-made. Keep that line. Viewers trust a channel that tells them, and every platform asks for it.

**Subtitles:** for each episode whose narration is rendered, `captions/epNN.srt` holds Hindi subtitles timed to the voice. Upload it on YouTube under Subtitles → Hindi → Upload file → With timing, and on Facebook in the video's Captions settings. Viewers watching on mute, and the YouTube search index, both read them.
"""

if __name__ == "__main__":
    main()
