"""Build the publishing kit: channel set-up text for every platform plus a post for each episode.

    python3 make_publish_kit.py

Reads episodes.psv and each epNN-*-hindi.md (title, thumbnail words, sources, hook lines, next
episode). Writes:
  publishing-kit.md    YouTube channel set-up, upload settings, playlists, and all 84 episode uploads
  publishing-kit.csv   the same episode posts, one row per episode, for spreadsheets / schedulers
  captions/epNN.srt    Hindi subtitles, for every episode whose narration is rendered (from audio/epNN.timing.json)
"""
import csv, glob, json, os, re, sys

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
            "Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts")


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
    # spoken pieces of the hook, whole sentences (script lines are wrapped, so use the narration plan)
    import eleven_render as er
    items = er.plan(t)
    hook_pieces = []
    for kind, val in items:
        if kind == "scene" and hook_pieces:
            break
        if kind == "text":
            hook_pieces.append(clean(val))
    opener, n = [], 0
    for l in hook_pieces:
        opener.append(l); n += len(l)
        if n > 220 or len(opener) >= 4:
            break
    sections = re.findall(r"(?m)^## (.+)$", body.split("## जाँच लें")[0])
    return dict(title=title, thumb=thumb, next=nxt, src=src, hook="\n".join(opener),
                hook1=opener[0] if opener else "", sections=sections)


def timing(ep):
    p = os.path.join(HERE, "audio", f"ep{ep:02d}.timing.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def chapters(ep):
    """YouTube chapters from the narration's timing file (exact), if the episode is rendered."""
    tm = timing(ep)
    if not tm:
        return None
    return [(it["start"] if i else 0.0, it["text"]) for i, it in enumerate(x for x in tm["items"] if x["kind"] == "scene")]


def stamp(s, srt=False):
    if srt:
        ms = int(round(s * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    h, m, sec = int(s // 3600), int(s % 3600 // 60), s % 60
    return f"{m}:{int(sec):02d}" if h == 0 else f"{h}:{m:02d}:{int(sec):02d}"


def write_srt(ep, max_chars=80):
    """Hindi subtitles from the timing file: one cue per sentence, long sentences split at a pause."""
    tm = timing(ep)
    cues = []
    for it in (x for x in tm["items"] if x["kind"] == "text"):
        text, a, b = it["text"], it["start"], it["end"]
        parts = [p.strip(" …") for p in re.split(r"(?<=[।?!])\s+", text)]
        parts = [p for p in parts if re.search(r"[\u0900-\u097F]", p)]
        split = []
        for p in parts:
            while len(p) > max_chars:                       # break at the pause nearest the middle
                cuts = [m.end() for m in re.finditer(r"…|,", p) if 15 <= m.end() <= len(p) - 15]
                if not cuts:                                # no pause mark: cut at the space nearest the middle
                    cuts = [m.start() for m in re.finditer(" ", p) if 15 <= m.start() <= len(p) - 15]
                if not cuts:
                    break
                c = min(cuts, key=lambda x: abs(x - len(p) / 2))
                split.append(p[:c].strip()); p = p[c:].strip()
            split.append(p)
        merged = []
        for p in split:                              # a very short fragment is merged with its neighbour
            if merged and len(p) < 14:
                merged[-1] = merged[-1] + " " + p
            else:
                merged.append(p)
        if len(merged) > 1 and len(merged[0]) < 14:
            merged[1] = merged[0] + " " + merged[1]; merged.pop(0)
        split = merged
        total = sum(len(p) for p in split)
        t = a
        for p in split:
            d = (b - a) * len(p) / total
            cues.append((t, t + d, p.strip(" …") or p)); t += d
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
    w("## 5. Playlists (create these once; add each episode to its king's playlist and to the full series)\n")
    w("| playlist | title | description |\n| --- | --- | --- |")
    w(f"| all | सूर्यवंश कथा: संपूर्ण शृंखला (84 एपिसोड) | मनु से लव-कुश तक, सूर्यवंश की पूरी कथा क्रम से। श्रीमद्भागवत स्कंध 9 पर आधारित, हर कथा के स्रोत स्क्रीन पर। |")
    for a, es in arc_eps.items():
        hi, _ = KINGS[es[0]["king"]]
        w(f"| arc {a} | {hi}: सूर्यवंश कथा भाग {a} ({len(es)} एपिसोड) | {hi} की पूरी कथा, {len(es)} एपिसोड में, एपिसोड {es[0]['n']} से {es[-1]['n']} तक। स्रोत: {es[0]['en_src'].split(';')[0]} आदि, हर एपिसोड में स्क्रीन पर। |")
    w("")
    w("## 6. Every episode\n")
    w("Each episode below has everything for its YouTube upload. Copy each box as it is. Where the description says "
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
        short = (f"{e['hook1']} 🔱 {e['title']}\n"
                 f"पूरी कथा: सूर्यवंश कथा · एपिसोड {n} (Related video में लिंक)\n"
                 f"#Shorts #सूर्यवंश {ktags[0]} #पौराणिककथा")
        pin = (f"आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇\n"
               f"अगला एपिसोड: {nxt}")
        thumb = e["thumb"].strip("`") or e["en_thumb"]

        w(f"### E{n:02d} · {e['title']}\n")
        w(f"*{e['en']}* · {hi_king}, भाग {e['part']}/{e['of']} · थंबनेल पर: **{thumb}** (English: {e['en_thumb']})\n")
        w(f"**YouTube title** ({len(yt_title)}/100)\n```\n{yt_title}\n```")
        w(f"**YouTube description**\n```\n{yt_desc}\n```")
        w(f"**YouTube tags field** ({len(yt_tag_field)}/500)\n```\n{yt_tag_field}\n```")
        w(f"**YouTube pinned comment**\n```\n{pin}\n```")
        w(f"**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)\n```\n{short}\n```\n")
        csv_rows.append(dict(episode=n, arc=e["arc"], king=e["king"], hindi_title=e["title"],
                             english_title=e["en"], thumbnail=thumb, youtube_title=yt_title,
                             youtube_description=yt_desc, youtube_tags=yt_tag_field, pinned_comment=pin,
                             youtube_short=short, thumbnail_file=f"ep{n:02d}-thumbnail-1280x720.jpg",
                             subtitles_file=f"ep{n:02d}.srt"))

    open(os.path.join(HERE, "publishing-kit.md"), "w", encoding="utf-8").write("\n".join(out))
    with open(os.path.join(HERE, "publishing-kit.csv"), "w", encoding="utf-8-sig", newline="") as f:
        cw = csv.DictWriter(f, fieldnames=list(csv_rows[0]))
        cw.writeheader(); cw.writerows(csv_rows)
    for p in sorted(glob.glob(os.path.join(HERE, "audio", "ep??.timing.json"))):
        print("wrote", write_srt(int(os.path.basename(p)[2:4])))
    upload_folders(csv_rows, arc_eps)
    print("wrote publishing-kit.md and publishing-kit.csv,", len(eps), "episodes")


def upload_folders(rows, arc_eps):
    """youtube-upload/EpNN/: thumbnail, subtitles and upload.txt for every episode whose video exists."""
    import shutil
    base = os.path.join(HERE, "youtube-upload")
    for r in rows:
        n = r["episode"]
        if not os.path.exists(os.path.join(HERE, "video", f"ep{n:02d}.mp4")):
            continue
        d = os.path.join(base, f"Ep{n:02d}"); os.makedirs(d, exist_ok=True)
        thumb = os.path.join(HERE, "brand", "out", "thumbnails", r["thumbnail_file"])
        srt = os.path.join(HERE, "captions", r["subtitles_file"])
        for src in (thumb, srt):
            if os.path.exists(src):
                shutil.copy(src, d)
        hi_king = KINGS[r["king"]][0]
        a = r["arc"]
        txt = (f"EPISODE {n} — YouTube upload\n"
               f"Video file: ep{n:02d}.mp4\n\n"
               f"== TITLE ==\n{r['youtube_title']}\n\n"
               f"== DESCRIPTION ==\n{r['youtube_description']}\n\n"
               f"== TAGS ==\n{r['youtube_tags']}\n\n"
               f"== THUMBNAIL ==\n{r['thumbnail_file']}\n\n"
               f"== SUBTITLES ==\nHindi, upload with timing: {r['subtitles_file']}\n\n"
               f"== PLAYLISTS ==\n{hi_king}: सूर्यवंश कथा भाग {a} ({len(arc_eps[a])} एपिसोड)\n"
               f"सूर्यवंश कथा: संपूर्ण शृंखला (84 एपिसोड)\n\n"
               f"== SETTINGS ==\nAudience: No, not made for kids · Altered/synthetic content: No · "
               f"Category: Education · Language: Hindi\n\n"
               f"== PINNED COMMENT ==\n{r['pinned_comment']}\n\n"
               f"== YOUTUBE SHORT (optional) ==\n{r['youtube_short']}\n")
        open(os.path.join(d, "upload.txt"), "w", encoding="utf-8").write(txt)
    print("wrote upload folders in", base)


HEADER = f"""# YouTube upload kit: सूर्यवंश कथा

Everything to type into YouTube: the channel set-up, the settings for every upload, the playlists,
and for each of the 84 episodes its title, description (with chapters once the episode is made),
tags, pinned comment and thumbnail words. Made by `make_publish_kit.py` from the scripts, so every
description quotes that episode's own opening lines and sources.

For every finished episode there is also a ready folder in `youtube-upload/EpNN/`: the thumbnail,
the Hindi subtitle file, and `upload.txt` with all the text below for that episode.

## 1. Channel name

**{CHANNEL}**, handle **{HANDLE}**. If the handle is taken, use `@SuryavanshKathaHindi`.

Why: it says exactly what the channel is (the story of the Sun dynasty, from Manu to Lav and Kush),
people search the word in both Hindi and English, and the tagline **"{TAGLINE_HI}"** ({TAGLINE_EN})
is what sets it apart: every episode shows its source on screen.

## 2. Channel set-up (YouTube Studio → Customisation)

| field | what to enter |
| --- | --- |
| Name (max 50) | `{CHANNEL}` |
| Handle | `{HANDLE}` |
| Picture | `youtube/profile-picture-800x800.png` (channel pictures zip) |
| Banner | `youtube/banner-2560x1440.jpg` |
| Video watermark | `youtube/watermark-150x150.png`, display: entire video |
| Channel trailer | Episode 1 (the fish and the flood) |
| Featured section | playlist "सूर्यवंश कथा: संपूर्ण शृंखला" |
| Country | India |
| Banner text | **सूर्यवंश कथा** · {TAGLINE_HI} · नए एपिसोड हर मंगलवार और शुक्रवार (change the days in the banner if you post on other days) |

**Description (Customisation → Basic info):**
```
मनु की नाव को खींचती एक सुनहरी मछली से लेकर… श्रीराम के पुत्र लव और कुश तक।
यह है सूर्यवंश की पूरी कथा: वह वंश जिसमें इक्ष्वाकु, मान्धाता, हरिश्चंद्र, सगर, भगीरथ, रघु, दशरथ और श्रीराम हुए।

84 एपिसोड, लगभग 7 से 9 मिनट के, ठीक क्रम में।
आधार: श्रीमद्भागवत महापुराण, स्कंध 9 (अध्याय 6 से 12), साथ में वाल्मीकि रामायण, कालिदास का रघुवंशम् और तुलसीदास का रामचरितमानस।

{TAGLINE_HI}
हर एपिसोड में स्क्रीन पर लिखा होता है कि कथा किस ग्रंथ से है। जहाँ कथा लोक-परंपरा की है, वहाँ भी साफ़ बताया जाता है।

नए एपिसोड: हर मंगलवार और शुक्रवार।
शुरुआत यहाँ से करें: एपिसोड 1, "इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया"।

The story of the Sun dynasty (Suryavansh), from Manu to Lav and Kush, in Hindi.
84 episodes based on the Bhagavata Purana (Book 9), with the source shown on screen in every episode.
Narration: AI voice (ElevenLabs). Illustrations: AI-generated (Google).
```

**Channel keywords (Settings → Channel → Basic info):**
```
सूर्यवंश, सूर्यवंश कथा, Suryavansh, Suryavanshi, भागवत पुराण, श्रीमद्भागवत, Bhagavata Purana, Srimad Bhagavatam, रामायण, Ramayan, श्रीराम, इक्ष्वाकु, रघुवंश, राजा हरिश्चंद्र, भगीरथ, गंगावतरण, पौराणिक कथा, हिंदू पौराणिक कथा, Indian mythology, Hindu mythology, Hindi kahani, धार्मिक कथा
```

## 3. Upload defaults (Settings → Upload defaults, set once)

| field | value |
| --- | --- |
| Category | Education |
| Video language | Hindi |
| Title and description language | Hindi |
| Caption certification | None of these / not aired on TV |
| Licence | Standard YouTube licence |
| Comments | On, hold potentially inappropriate comments for review |
| Shorts remixing | Allow |

## 4. For every upload

1. **Video:** the episode's MP4 (1920×1080, 25 fps).
2. **Title, description, tags:** copy from the episode's section below (or its `upload.txt`).
3. **Thumbnail:** `epNN-thumbnail-1280x720.jpg`.
4. **Playlists:** the king's playlist and "सूर्यवंश कथा: संपूर्ण शृंखला".
5. **Audience:** **No, it's not made for kids** (made-for-kids turns off comments and the mini-player).
6. **Altered or synthetic content:** **No** for these painted illustrations (they don't show realistic people or events). The AI voice and AI pictures are disclosed in every description anyway.
7. **Subtitles:** Subtitles → Add language Hindi → Upload file → *With timing* → `epNN.srt`.
8. **Chapters:** already in the description (the timestamps make YouTube chapters automatically).
9. **End screen:** "Video: best for viewer" + "Playlist: सूर्यवंश कथा: संपूर्ण शृंखला" + Subscribe, from the last 15 s.
10. **Cards:** at the end of each episode, a card to the next episode once it's published.
11. **Pinned comment:** post the episode's pinned comment from your channel and pin it.
12. **Visibility:** Schedule (two episodes a week works well), so new episodes go out at the same time.

**YouTube Shorts (optional):** cut a 30-60 s vertical clip from each episode's hook, upload it as a
Short with the text in the episode's "YouTube Short" box, and set **Related video** to the full
episode. Shorts bring new viewers to the long episodes.

**Hashtags:** each description carries at most 15 (YouTube ignores all of them above 60, and shows
the first three above the title).
"""

if __name__ == "__main__":
    main()
