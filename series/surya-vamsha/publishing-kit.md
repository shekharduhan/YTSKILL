# YouTube upload kit: सूर्यवंश कथा

Everything to type into YouTube: the channel set-up, the settings for every upload, the playlists,
and for episodes 1 to 26 (the rest of the 84 come later) the title, description (with chapters once the episode is made),
tags, pinned comment and thumbnail words. Made by `make_publish_kit.py` from the scripts, so every
description quotes that episode's own opening lines and sources.

For every finished episode there is also a ready folder in `youtube-upload/EpNN/`: the thumbnail,
the Hindi subtitle file, and `upload.txt` with all the text below for that episode.

## 1. Channel name

**सूर्यवंश कथा | Suryavansh Katha**, handle **@SuryavanshKatha**. If the handle is taken, use `@SuryavanshKathaHindi`.

Why: it says exactly what the channel is (the story of the Sun dynasty, from Manu to Lav and Kush),
people search the word in both Hindi and English, and the tagline **"हर कथा, स्रोत के साथ।"** (Every story, with its source.)
is what sets it apart: every episode shows its source on screen.

## 2. Channel set-up (YouTube Studio → Customisation)

| field | what to enter |
| --- | --- |
| Name (max 50) | `सूर्यवंश कथा | Suryavansh Katha` |
| Handle | `@SuryavanshKatha` |
| Picture | `youtube/profile-picture-800x800.png` (channel pictures zip) |
| Banner | `youtube/banner-2560x1440.jpg` |
| Video watermark | `youtube/watermark-150x150.png`, display: entire video |
| Channel trailer | Episode 1 (the fish and the flood) |
| Featured section | playlist "सूर्यवंश कथा: संपूर्ण शृंखला" |
| Country | India |
| Banner text | **सूर्यवंश कथा** · हर कथा, स्रोत के साथ। · नए एपिसोड हर मंगलवार और शुक्रवार (change the days in the banner if you post on other days) |

**Description (Customisation → Basic info):**
```
मनु की नाव को खींचती एक सुनहरी मछली से लेकर… श्रीराम के पुत्र लव और कुश तक।
यह है सूर्यवंश की पूरी कथा: वह वंश जिसमें इक्ष्वाकु, मान्धाता, हरिश्चंद्र, सगर, भगीरथ, रघु, दशरथ और श्रीराम हुए।

84 एपिसोड, लगभग 7 से 9 मिनट के, ठीक क्रम में।
आधार: श्रीमद्भागवत महापुराण, स्कंध 9 (अध्याय 6 से 12), साथ में वाल्मीकि रामायण, कालिदास का रघुवंशम् और तुलसीदास का रामचरितमानस।

हर कथा, स्रोत के साथ।
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

## 5. Playlists (create these once; add each episode to its king's playlist and to the full series)

| playlist | title | description |
| --- | --- | --- |
| all | सूर्यवंश कथा: संपूर्ण शृंखला (84 एपिसोड) | मनु से लव-कुश तक, सूर्यवंश की पूरी कथा क्रम से। श्रीमद्भागवत स्कंध 9 पर आधारित, हर कथा के स्रोत स्क्रीन पर। |
| arc 1 | इक्ष्वाकु: सूर्यवंश कथा भाग 1 (6 एपिसोड) | इक्ष्वाकु की पूरी कथा, 6 एपिसोड में, एपिसोड 1 से 6 तक। स्रोत: SB 9.1 आदि, हर एपिसोड में स्क्रीन पर। |
| arc 2 | मान्धाता: सूर्यवंश कथा भाग 2 (7 एपिसोड) | मान्धाता की पूरी कथा, 7 एपिसोड में, एपिसोड 7 से 13 तक। स्रोत: SB 9.6 आदि, हर एपिसोड में स्क्रीन पर। |
| arc 3 | त्रिशंकु: सूर्यवंश कथा भाग 3 (6 एपिसोड) | त्रिशंकु की पूरी कथा, 6 एपिसोड में, एपिसोड 14 से 19 तक। स्रोत: SB 9.7 आदि, हर एपिसोड में स्क्रीन पर। |
| arc 4 | राजा हरिश्चंद्र: सूर्यवंश कथा भाग 4 (7 एपिसोड) | राजा हरिश्चंद्र की पूरी कथा, 7 एपिसोड में, एपिसोड 20 से 26 तक। स्रोत: SB 9.7 आदि, हर एपिसोड में स्क्रीन पर। |

## 6. Every episode

Each episode below has everything for its YouTube upload. Copy each box as it is. Where the description says `[link]`, paste that episode's YouTube link once it is up. Chapters are filled in for episodes whose narration is already rendered; for the others, run `python3 make_publish_kit.py` again after rendering.

### E01 · इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया

*The Sun's Family: Before Ikshvaku Was Born* · इक्ष्वाकु, भाग 1/6 · थंबनेल पर: **मनु की मछली** (English: MANU'S FISH)

**YouTube title** (65/100)
```
इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया | सूर्यवंश कथा
```
**YouTube description**
```
एक समय था… जब पूरी पृथ्वी जल में डूब गई थी।
न पर्वत बचे… न नगर… न राजा।
बची थी… एक नाव। और उस नाव को खींच रही थी… एक मछली।
सोचिए… जिस वंश में श्रीराम जन्मे… उस वंश का बीज… एक मछली की कृपा से बचा था।

सूर्यवंश कथा · एपिसोड 1 / 84 · इक्ष्वाकु (भाग 1 / 6)
In this episode: Who the Sun dynasty descends from: Vivasvan, Vaivasvata Manu, and the fish that saved Manu.

📜 स्रोत: श्रीमद्भागवत 8.24 (मत्स्य अवतार) · 9.1 (मनु, इला, सुद्युम्न) · 9.2 · 9.6
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:46 पहला दृश्य: चोरी हुए वेद
1:39 दूसरा दृश्य: अंजलि में मछली
2:50 तीसरा दृश्य: सात दिन
4:23 चौथा दृश्य: सत्यव्रत बने मनु
4:41 पाँचवाँ दृश्य: इला, जो सुद्युम्न बनी
6:47 समाधान: इक्ष्वाकु का आगमन
7:07 समापन

▶ अगला एपिसोड: E02 इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (289/500)
```
इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया, The Sun's Family: Before Ikshvaku Was Born, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E02 इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक समय था… जब पूरी पृथ्वी जल में डूब गई थी। 🔱 इक्ष्वाकु से पहले: वह मछली जिसने सूर्यवंश को बचाया
पूरी कथा: सूर्यवंश कथा · एपिसोड 1 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E02 · इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला

*Ikshvaku: The King Born From a Sneeze* · इक्ष्वाकु, भाग 2/6 · थंबनेल पर: **एक खरगोश। देश निकाला।** (English: 1 RABBIT. EXILED.)

**YouTube title** (69/100)
```
इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला | सूर्यवंश कथा
```
**YouTube description**
```
अयोध्या का नाम आपने सुना है। … लेकिन बहुत कम लोग जानते हैं कि अयोध्या के पहले राजा ने अपने ही ज्येष्ठ पुत्र को राज्य से क्यों निकाल दिया था।
कारण था… एक खरगोश।
और जिस पुत्र को निकाला गया… उसी के वंश से श्रीराम को उनका एक नाम मिला।

सूर्यवंश कथा · एपिसोड 2 / 84 · इक्ष्वाकु (भाग 2 / 6)
In this episode: Ikshvaku's birth, his hundred sons, and the rabbit that got his eldest son exiled.

📜 स्रोत: श्रीमद्भागवत महापुराण, नवम स्कंध, अध्याय 6 (श्रीमद्भा. 9.6)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:21 कथा का द्वार
1:01 पहला दृश्य: सूर्य से मनु तक
1:44 दूसरा दृश्य: छींक से जन्म
2:27 तीसरा दृश्य: सौ पुत्र और एक नक्शा
3:28 चौथा दृश्य: खरगोश
4:55 पाँचवाँ दृश्य: दंड
6:17 छठा दृश्य: राजा ने सब त्याग दिया
6:56 सातवाँ दृश्य: शशाद लौटता है
7:31 समाधान: श्रीराम "काकुत्स्थ" क्यों कहलाए
8:14 समापन

▶ अगला एपिसोड: E03 निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (288/500)
```
इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला, Ikshvaku: The King Born From a Sneeze, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E03 निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
अयोध्या का नाम आपने सुना है। … लेकिन बहुत कम लोग जानते हैं कि अयोध्या के पहले राजा ने अपने ही ज्येष्ठ पुत्र को राज्य से क्यों निकाल दिया था। 🔱 इक्ष्वाकु: छींक से जन्मा राजा, जिससे इक्ष्वाकु वंश चला
पूरी कथा: सूर्यवंश कथा · एपिसोड 2 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E03 · निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है

*Nimi: Ikshvaku's Son Who Lives in Every Blink* · इक्ष्वाकु, भाग 3/6 · थंबनेल पर: **देह नहीं बची** (English: NO BODY LEFT)

**YouTube title** (59/100)
```
निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है | सूर्यवंश कथा
```
**YouTube description**
```
अभी… आपने पलक झपकाई।
भागवत कहता है… उस पल में एक राजा रहता है। एक राजा, जिसने अपनी देह लौटाने से मना कर दिया था। उसका नाम था… निमि।

सूर्यवंश कथा · एपिसोड 3 / 84 · इक्ष्वाकु (भाग 3 / 6)
In this episode: Ikshvaku's son Nimi, the curse he and Vasishtha traded, and the line that leads to Sita's father Janaka.

📜 स्रोत: श्रीमद्भागवत 9.13 (निमि और मिथिला का वंश)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:16 कथा का द्वार
0:38 पहला दृश्य: एक यज्ञ, दो निमंत्रण
1:30 दूसरा दृश्य: शाप के बदले शाप
2:18 तीसरा दृश्य: "मुझे देह नहीं चाहिए"
4:01 चौथा दृश्य: बिना माँ के जन्मा राजा
4:57 पाँचवाँ दृश्य: राजा भी, योगी भी
6:02 समाधान: सीता तक
6:39 समापन

▶ अगला एपिसोड: E04 ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (286/500)
```
निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है, Nimi: Ikshvaku's Son Who Lives in Every Blink, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E04 ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
अभी… आपने पलक झपकाई। 🔱 निमि: इक्ष्वाकु का वह पुत्र जो हर पलक में है
पूरी कथा: सूर्यवंश कथा · एपिसोड 3 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E04 · ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ

*Kakutstha: The Prince Who Rode Indra Into Battle* · इक्ष्वाकु, भाग 4/6 · थंबनेल पर: **देवता पर सवार** (English: RIDING A GOD)

**YouTube title** (57/100)
```
ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ | सूर्यवंश कथा
```
**YouTube description**
```
देवताओं का राजा… इंद्र। … और एक दिन इंद्र को एक मनुष्य राजा की सवारी बनना पड़ा।
और उस दिन जो नाम पड़ा… उसी से बना नाम हज़ारों वर्ष बाद श्रीराम को पुकारने के लिए इस्तेमाल हुआ।

सूर्यवंश कथा · एपिसोड 4 / 84 · इक्ष्वाकु (भाग 4 / 6)
In this episode: Puranjaya rides Indra in bull form against the asuras, and why Rama is called Kakutstha.

📜 स्रोत: श्रीमद्भागवत 9.6 · संदर्भ: 9.9 (खट्वांग), 10.51 (मुचुकुंद), वाल्मीकि रामायण (दशरथ)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:16 कथा का द्वार
0:35 पहला दृश्य: देवता हार रहे थे
1:13 बीच का दृश्य: देवताओं को मनुष्य क्यों चाहिए?
2:09 दूसरा दृश्य: शर्त
2:44 तीसरा दृश्य: ककुद पर बैठा योद्धा
3:30 चौथा दृश्य: तीन नाम
4:10 पाँचवाँ दृश्य: एक पैटर्न
5:08 छठा दृश्य: इंद्र का अहंकार
6:07 समाधान: आगे का वंश
6:20 समापन

▶ अगला एपिसोड: E05 धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (287/500)
```
ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ, Kakutstha: The Prince Who Rode Indra Into Battle, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E05 धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
देवताओं का राजा… इंद्र। … और एक दिन इंद्र को एक मनुष्य राजा की सवारी बनना पड़ा। 🔱 ककुत्स्थ: वह राजकुमार जो इंद्र पर सवार हुआ
पूरी कथा: सूर्यवंश कथा · एपिसोड 4 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E05 · धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र

*Dhundhumara: 21,000 Sons Against 1 Demon* · इक्ष्वाकु, भाग 5/6 · थंबनेल पर: **केवल 3 लौटे** (English: ONLY 3 CAME BACK)

**YouTube title** (57/100)
```
धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र | सूर्यवंश कथा
```
**YouTube description**
```
रेत के नीचे… कोई सो रहा था।
और जब वह साँस लेता… तो धरती काँप उठती। आकाश धुएँ से भर जाता।
एक राजा अपने इक्कीस हज़ार पुत्रों को लेकर उसे जगाने गया।
और लौटे… केवल तीन।

सूर्यवंश कथा · एपिसोड 5 / 84 · इक्ष्वाकु (भाग 5 / 6)
In this episode: Kuvalayashva and the demon Dhundhu under the sand, and the three sons who survived.

📜 स्रोत: श्रीमद्भागवत 9.6 (मूल घटना) · महाभारत, वन पर्व (विस्तृत कथा)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:19 कथा का द्वार
0:45 पहला दृश्य: भागवत क्या कहता है
1:26 दूसरा दृश्य: रेत का सागर
2:15 बीच का दृश्य: मधु और कैटभ कौन थे?
3:33 तीसरा दृश्य: बूढ़ा राजा, युवा पुत्र
4:21 चौथा दृश्य: सात दिन की खुदाई
5:07 पाँचवाँ दृश्य: आग पर जल
5:52 अंतिम दृश्य: धुंधुमार नाम का अर्थ
6:35 समाधान: तीन पुत्र
7:07 समापन

▶ अगला एपिसोड: E06 श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (279/500)
```
धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र, Dhundhumara: 21,000 Sons Against 1 Demon, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E06 श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
रेत के नीचे… कोई सो रहा था। 🔱 धुंधुमार: एक दैत्य के विरुद्ध 21,000 पुत्र
पूरी कथा: सूर्यवंश कथा · एपिसोड 5 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E06 · श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया

*Shravasti: The City a Sun King Founded* · इक्ष्वाकु, भाग 6/6 · थंबनेल पर: **आज भी खड़ा है** (English: STILL STANDING)

**YouTube title** (62/100)
```
श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया | सूर्यवंश कथा
```
**YouTube description**
```
उत्तर प्रदेश में… कुछ पुरानी ईंटें हैं।
लोग उन्हें देखने दुनिया भर से आते हैं। श्रीलंका से, थाईलैंड से, जापान से।
पर बहुत कम लोग जानते हैं… भागवत के अनुसार इस नगर को बसाया था… श्रीराम के एक पूर्वज ने।
और इसी नगर का राजा बना… श्रीराम का पुत्र लव।

सूर्यवंश कथा · एपिसोड 6 / 84 · इक्ष्वाकु (भाग 6 / 6)
In this episode: The city King Shravasta founded, later Lava's capital and the Buddha's Jetavana, still standing as ruins.

📜 स्रोत: श्रीमद्भागवत 9.6 (शावस्त और श्रावस्ती) · वाल्मीकि रामायण, उत्तर कांड (लव और श्रावस्ती) · बौद्ध और जैन परंपरा · पुरातत्व
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:24 कथा का द्वार
0:43 पहला दृश्य: शावस्त
1:23 दूसरा दृश्य: लव का राज्य
2:10 तीसरा दृश्य: सोने से ढकी भूमि
3:15 चौथा दृश्य: बुद्ध की नगरी
4:05 बीच का दृश्य: दो नगर, एक राज्य
4:59 पाँचवाँ दृश्य: जैन परंपरा
5:29 छठा दृश्य: आज के खंडहर
6:12 समाधान
6:30 समापन

▶ अगला एपिसोड: E07 मांधाता: पिता से जन्मे, इंद्र ने पाला
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #इक्ष्वाकु #भागवतपुराण #Ikshvaku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (282/500)
```
श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया, Shravasti: The City a Sun King Founded, इक्ष्वाकु, Ikshvaku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E07 मांधाता: पिता से जन्मे, इंद्र ने पाला
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
उत्तर प्रदेश में… कुछ पुरानी ईंटें हैं। 🔱 श्रावस्ती: वह नगर जो एक सूर्यवंशी राजा ने बसाया
पूरी कथा: सूर्यवंश कथा · एपिसोड 6 (Related video में लिंक)
#Shorts #सूर्यवंश #इक्ष्वाकु #पौराणिककथा
```

### E07 · मांधाता: पिता से जन्मे, इंद्र ने पाला

*Mandhata: Born From His Father, Fed by Indra* · मान्धाता, भाग 1/7 · थंबनेल पर: **उन्होंने पी लिया** (English: HE DRANK IT)

**YouTube title** (52/100)
```
मांधाता: पिता से जन्मे, इंद्र ने पाला | सूर्यवंश कथा
```
**YouTube description**
```
एक रात… एक राजा को प्यास लगी।
उसने एक कलश का जल पी लिया। वह जल… उसकी रानी के लिए अभिमंत्रित था।
और कुछ महीनों बाद… उस राजा ने स्वयं… एक पुत्र को जन्म दिया।
यह कोई लोककथा नहीं है। यह भागवत का नवम स्कंध है।

सूर्यवंश कथा · एपिसोड 7 / 84 · मान्धाता (भाग 1 / 7)
In this episode: How a childless king drank the consecrated water and gave birth himself.

📜 स्रोत: श्रीमद्भागवत 9.6
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:43 पहला दृश्य: निःसंतान राजा
1:33 दूसरा दृश्य: ऋषियों का यज्ञ
2:03 तीसरा दृश्य: प्यास
3:04 चौथा दृश्य: जन्म
3:53 पाँचवाँ दृश्य: "मां धाता"
4:48 छठा दृश्य: दो ग्रंथ, एक कथा
6:02 समाधान: बालक, जिससे दस्यु डरते थे
6:30 समापन

▶ अगला एपिसोड: E08 मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (277/500)
```
मांधाता: पिता से जन्मे, इंद्र ने पाला, Mandhata: Born From His Father, Fed by Indra, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E08 मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक रात… एक राजा को प्यास लगी। 🔱 मांधाता: पिता से जन्मे, इंद्र ने पाला
पूरी कथा: सूर्यवंश कथा · एपिसोड 7 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E08 · मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे

*Mandhata's 2 Names: The King Thieves Feared* · मान्धाता, भाग 2/7 · थंबनेल पर: **मां धाता** (English: MAM DHATA)

**YouTube title** (63/100)
```
मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे | सूर्यवंश कथा
```
**YouTube description**
```
भागवत में एक पंक्ति है।
"जहाँ से सूर्य उगता है… और जहाँ वह अस्त होता है… वह सारी भूमि मांधाता की कहलाती है।"
इतना बड़ा सम्राट। इतना अजेय।
और फिर भी… एक दिन… एक ही त्रिशूल के सामने… वह राख हो गया।

सूर्यवंश कथा · एपिसोड 8 / 84 · मान्धाता (भाग 2 / 7)
In this episode: What 'Mandhata' and 'Trasaddasyu' mean, and the empire from sunrise to sunset.

📜 स्रोत: श्रीमद्भागवत 9.6 (साम्राज्य, यज्ञ, विवाह) · वाल्मीकि रामायण, उत्तर कांड (मांधाता और लवणासुर)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:21 कथा का द्वार
0:42 पहला दृश्य: दो नाम
1:29 दूसरा दृश्य: सात द्वीपों का सम्राट
2:26 तीसरा दृश्य: बिंदुमती
3:03 चौथा दृश्य: इंद्र का प्रश्न
3:54 पाँचवाँ दृश्य: एक त्रिशूल
4:30 छठा दृश्य: राजधर्म का प्रश्न
5:39 सातवाँ दृश्य: नर्मदा का द्वीप "मांधाता"
6:31 समाधान: कथा क्यों सुनाई गई?
6:55 समापन

▶ अगला एपिसोड: E09 सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (287/500)
```
मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे, Mandhata's 2 Names: The King Thieves Feared, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E09 सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
भागवत में एक पंक्ति है। 🔱 मांधाता के दो नाम: वह सम्राट जिससे दस्यु डरते थे
पूरी कथा: सूर्यवंश कथा · एपिसोड 8 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E09 · सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई

*Saubhari: The Sage Who Envied a Fish* · मान्धाता, भाग 3/7 · थंबनेल पर: **परिवार चाहिए** (English: HE WANTED A FAMILY)

**YouTube title** (56/100)
```
सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई | सूर्यवंश कथा
```
**YouTube description**
```
एक ऋषि… यमुना के जल के भीतर तप कर रहे थे।
न भूख। न प्यास। न संसार।
और एक दिन… उनकी आँख खुली। सामने एक मछली थी… अपने परिवार के साथ।
और उस एक दृश्य ने… वर्षों का तप हिला दिया।

सूर्यवंश कथा · एपिसोड 9 / 84 · मान्धाता (भाग 3 / 7)
In this episode: Why a sage meditating under the Yamuna decided to marry.

📜 स्रोत: श्रीमद्भागवत 9.6 (सौभरि का तप और इच्छा) · 10.17 (सौभरि और गरुड़) · ऋग्वेद, अष्टम मंडल (सोभरि काण्व)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:20 कथा का द्वार
0:46 पहला दृश्य: वेद का ऋषि
1:12 दूसरा दृश्य: जल के भीतर तप
1:47 तीसरा दृश्य: मछली का परिवार
2:38 चौथा दृश्य: गरुड़ को शाप
3:44 पाँचवाँ दृश्य: जल से बाहर
4:29 छठा दृश्य: इस शृंखला की दूसरी मछली
5:39 सातवाँ दृश्य: जल में तप क्यों?
6:28 समाधान
6:38 समापन

▶ अगला एपिसोड: E10 सौभरि और मांधाता की 50 पुत्रियाँ
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (273/500)
```
सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई, Saubhari: The Sage Who Envied a Fish, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E10 सौभरि और मांधाता की 50 पुत्रियाँ
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक ऋषि… यमुना के जल के भीतर तप कर रहे थे। 🔱 सौभरि: वह ऋषि जिसे एक मछली से ईर्ष्या हुई
पूरी कथा: सूर्यवंश कथा · एपिसोड 9 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E10 · सौभरि और मांधाता की 50 पुत्रियाँ

*Saubhari and Mandhata's 50 Daughters* · मान्धाता, भाग 4/7 · थंबनेल पर: **हर एक ने उन्हें चुना** (English: EVERY ONE CHOSE HIM)

**YouTube title** (47/100)
```
सौभरि और मांधाता की 50 पुत्रियाँ | सूर्यवंश कथा
```
**YouTube description**
```
पचास राजकुमारियाँ।
एक-एक करके… सबने एक ही व्यक्ति को चुना।
और कुछ ही क्षण पहले… वही व्यक्ति… एक बूढ़ा, काँपता हुआ ऋषि था।

सूर्यवंश कथा · एपिसोड 10 / 84 · मान्धाता (भाग 4 / 7)
In this episode: The old sage's request, his transformation, and the palaces he built.

📜 स्रोत: श्रीमद्भागवत 9.6
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:14 कथा का द्वार
0:33 पहला दृश्य: एक माँग
1:23 दूसरा दृश्य: विनम्र रास्ता
2:07 तीसरा दृश्य: रूप का परिवर्तन
2:47 चौथा दृश्य: पचास ने चुना
3:28 पाँचवाँ दृश्य: सम्राट का अहंकार टूटा
4:34 छठा दृश्य: वेद में पचास वधुएँ
5:45 सातवाँ दृश्य: स्वयंवर की परंपरा
6:35 समाधान: क्या यही सुख था?
7:04 समापन

▶ अगला एपिसोड: E11 सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (264/500)
```
सौभरि और मांधाता की 50 पुत्रियाँ, Saubhari and Mandhata's 50 Daughters, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E11 सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
पचास राजकुमारियाँ। 🔱 सौभरि और मांधाता की 50 पुत्रियाँ
पूरी कथा: सूर्यवंश कथा · एपिसोड 10 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E11 · सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा

*Saubhari's Regret: The Sage Who Called It His Fall* · मान्धाता, भाग 5/7 · थंबनेल पर: **अब मुझे देखो** (English: LOOK AT ME NOW)

**YouTube title** (56/100)
```
सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा | सूर्यवंश कथा
```
**YouTube description**
```
उसके पास पचास पत्नियाँ थीं। महल थे। संतानें थीं।
और एक रात… उसने कहा…
"मेरा पतन देखो।"

सूर्यवंश कथा · एपिसोड 11 / 84 · मान्धाता (भाग 5 / 7)
In this episode: Saubhari's own words on desire, and what he did next.

📜 स्रोत: श्रीमद्भागवत 9.6 (अंतिम भाग)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:11 कथा का द्वार
0:35 पहला दृश्य: सुख, और सुख, और सुख
1:17 दूसरा दृश्य: एक रात का प्रश्न
1:47 तीसरा दृश्य: सौभरि के शब्द
2:39 चौथा दृश्य: एक से अनेक
3:19 पाँचवाँ दृश्य: वन की ओर, साथ में
4:02 छठा दृश्य: ययाति ने भी यही कहा
5:09 सातवाँ दृश्य: पचास राजकुमारियों का पक्ष
5:59 समाधान: एक कथा, एक दर्पण
6:18 समापन

▶ अगला एपिसोड: E12 पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (287/500)
```
सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा, Saubhari's Regret: The Sage Who Called It His Fall, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E12 पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
उसके पास पचास पत्नियाँ थीं। महल थे। संतानें थीं। 🔱 सौभरि का पश्चाताप: जिसने इसे अपना पतन कहा
पूरी कथा: सूर्यवंश कथा · एपिसोड 11 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E12 · पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा

*Purukutsa and Narmada: A King Sent to the Underworld* · मान्धाता, भाग 6/7 · थंबनेल पर: **नागों का सौदा** (English: THE NAGAS' DEAL)

**YouTube title** (58/100)
```
पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा | सूर्यवंश कथा
```
**YouTube description**
```
नागों के पास शक्ति थी। विष था। रत्न थे।
फिर भी एक युद्ध था… जो वे नहीं जीत सकते थे।
तो उन्होंने एक मनुष्य राजा को पाताल बुलाया। और उसे लेने भेजा… एक नदी को।

सूर्यवंश कथा · एपिसोड 12 / 84 · मान्धाता (भाग 6 / 7)
In this episode: Mandhata's son marries the river Narmada and fights the Gandharvas below the earth.

📜 स्रोत: श्रीमद्भागवत 9.7 · विष्णु पुराण, अंश 4 (विस्तृत कथा) · ऋग्वेद 4.42 (पुरुकुत्स और त्रसदस्यु)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:17 कथा का द्वार
0:36 पहला दृश्य: एक भ्रम, जो दूर करना ज़रूरी है
1:11 दूसरा दृश्य: पाताल का संकट
1:58 तीसरा दृश्य: नर्मदा
2:50 चौथा दृश्य: रसातल का युद्ध
3:32 पाँचवाँ दृश्य: वेद में एक नाम
4:21 छठा दृश्य: नर्मदा, जो आज भी बहती है
5:27 सातवाँ दृश्य: नर्मदा का मंत्र
6:23 समाधान: त्रिशंकु की ओर
6:45 समापन

▶ अगला एपिसोड: E13 मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (291/500)
```
पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा, Purukutsa and Narmada: A King Sent to the Underworld, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E13 मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
नागों के पास शक्ति थी। विष था। रत्न थे। 🔱 पुरुकुत्स और नर्मदा: पाताल भेजा गया एक राजा
पूरी कथा: सूर्यवंश कथा · एपिसोड 12 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E13 · मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया

*Muchukunda: Mandhata's Son Who Slept for Ages* · मान्धाता, भाग 7/7 · थंबनेल पर: **उन्हें मत जगाना** (English: DON'T WAKE HIM)

**YouTube title** (58/100)
```
मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया | सूर्यवंश कथा
```
**YouTube description**
```
एक गुफा में… एक राजा सो रहा था। युगों से।
और एक दिन… श्रीकृष्ण एक शत्रु को अपने पीछे दौड़ाते-दौड़ाते… जानबूझकर… उसी गुफा में ले आए।
शत्रु ने सोए हुए राजा को लात मारी।
और राजा ने आँखें खोलीं।

सूर्यवंश कथा · एपिसोड 13 / 84 · मान्धाता (भाग 7 / 7)
In this episode: Mandhata's son, his long sleep, and the day Krishna led Kalayavana into his cave.

📜 स्रोत: श्रीमद्भागवत 10.51 (और 10.52 का आरंभ)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:20 कथा का द्वार
0:42 पहला दृश्य: देवताओं का रक्षक
1:28 दूसरा दृश्य: सब चले गए
2:17 तीसरा दृश्य: नींद का वर
2:38 चौथा दृश्य: कालयवन
3:31 पाँचवाँ दृश्य: आँखें खुलीं
4:11 छठा दृश्य: साँप और चूहा
5:22 समाधान: दर्शन
6:20 समापन

▶ अगला एपिसोड: E14 वह राजा जिसने मरते समय रावण को शाप दिया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #मान्धाता #भागवतपुराण #Mandhata #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (284/500)
```
मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया, Muchukunda: Mandhata's Son Who Slept for Ages, मान्धाता, Mandhata, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E14 वह राजा जिसने मरते समय रावण को शाप दिया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक गुफा में… एक राजा सो रहा था। युगों से। 🔱 मुचुकुंद: मांधाता का पुत्र जो युगों तक सोया
पूरी कथा: सूर्यवंश कथा · एपिसोड 13 (Related video में लिंक)
#Shorts #सूर्यवंश #मान्धाता #पौराणिककथा
```

### E14 · वह राजा जिसने मरते समय रावण को शाप दिया

*The King Who Cursed Ravana Before He Died* · त्रिशंकु, भाग 1/6 · थंबनेल पर: **अनरण्य का शाप** (English: ANARANYA'S CURSE)

**YouTube title** (54/100)
```
वह राजा जिसने मरते समय रावण को शाप दिया | सूर्यवंश कथा
```
**YouTube description**
```
रावण ने एक राजा को युद्ध में गिरा दिया।
राजा मर रहा था। उसकी सेना नष्ट हो चुकी थी।
और उसने अंतिम साँस में… रावण की ओर देखकर कहा…
"मेरे ही वंश में एक राजकुमार जन्म लेगा… और वह तुम्हें मारेगा।"

सूर्यवंश कथा · एपिसोड 14 / 84 · त्रिशंकु (भाग 1 / 6)
In this episode: Anaranya of Trishanku's line and his dying curse on Ravana.

📜 स्रोत: श्रीमद्भागवत 9.7 (वंश-रेखा) · वाल्मीकि रामायण, उत्तर कांड (रावण की दिग्विजय और अनरण्य का शाप)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:20 कथा का द्वार
0:45 पहला दृश्य: वंश में एक नाम
1:24 दूसरा दृश्य: रावण की दिग्विजय
2:14 तीसरा दृश्य: अयोध्या ने झुकना नहीं चुना
2:57 चौथा दृश्य: युद्ध
3:44 पाँचवाँ दृश्य: उपहास
4:19 छठा दृश्य: शाप
5:04 सातवाँ दृश्य: रावण के शाप
6:01 समाधान: शाप कब पूरा हुआ?
6:31 समापन

▶ अगला एपिसोड: E15 त्रिशंकु स्वर्ग क्यों नहीं पहुँचे
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (277/500)
```
वह राजा जिसने मरते समय रावण को शाप दिया, The King Who Cursed Ravana Before He Died, त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E15 त्रिशंकु स्वर्ग क्यों नहीं पहुँचे
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
रावण ने एक राजा को युद्ध में गिरा दिया। 🔱 वह राजा जिसने मरते समय रावण को शाप दिया
पूरी कथा: सूर्यवंश कथा · एपिसोड 14 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E15 · त्रिशंकु स्वर्ग क्यों नहीं पहुँचे

*Why Trishanku Never Reached Heaven* · त्रिशंकु, भाग 2/6 · थंबनेल पर: **सिर के बल** (English: HEAD FIRST)

**YouTube title** (48/100)
```
त्रिशंकु स्वर्ग क्यों नहीं पहुँचे | सूर्यवंश कथा
```
**YouTube description**
```
एक राजा… शरीर सहित स्वर्ग गया।
देवताओं ने उसे वहाँ से सिर के बल नीचे फेंक दिया।
और वह गिरा भी नहीं।
भागवत कहता है… वह आज भी आकाश में दिखाई देता है।

सूर्यवंश कथा · एपिसोड 15 / 84 · त्रिशंकु (भाग 2 / 6)
In this episode: The Bhagavata's two verses on Trishanku, read in full, and what 'still seen in the sky' means.

📜 स्रोत: श्रीमद्भागवत 9.7 (त्रिशंकु के दो श्लोक) · परंपरा (आकाश में त्रिशंकु तारामंडल) · आधुनिक हिंदी प्रयोग
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:16 कथा का द्वार
0:43 पहला दृश्य: दो श्लोक
1:23 दूसरा दृश्य: हर शब्द एक प्रश्न
2:23 तीसरा दृश्य: शरीर सहित स्वर्ग
3:10 चौथा दृश्य: सिर के बल
3:46 पाँचवाँ दृश्य: बीच में रुका हुआ
4:21 छठा दृश्य: "आज भी दिखाई देते हैं"
5:17 सातवाँ दृश्य: भागवत ने इतना कम क्यों कहा?
6:06 समाधान
6:31 समापन

▶ अगला एपिसोड: E16 त्रिशंकु के तीन पाप: नाम कहाँ से आया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (264/500)
```
त्रिशंकु स्वर्ग क्यों नहीं पहुँचे, Why Trishanku Never Reached Heaven, त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E16 त्रिशंकु के तीन पाप: नाम कहाँ से आया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक राजा… शरीर सहित स्वर्ग गया। 🔱 त्रिशंकु स्वर्ग क्यों नहीं पहुँचे
पूरी कथा: सूर्यवंश कथा · एपिसोड 15 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E16 · त्रिशंकु के तीन पाप: नाम कहाँ से आया

*Trishanku's 3 Sins: Where His Name Comes From* · त्रिशंकु, भाग 3/6 · थंबनेल पर: **तीन शंकु** (English: THREE THORNS)

**YouTube title** (51/100)
```
त्रिशंकु के तीन पाप: नाम कहाँ से आया | सूर्यवंश कथा
```
**YouTube description**
```
एक राजकुमार ने… विवाह-मंडप से… किसी और की दुल्हन उठा ली।
उसके पिता ने उसे राज्य से निकाल दिया।
और फिर… बारह वर्ष के अकाल में… उसी निकाले हुए राजकुमार ने… एक ऋषि के भूखे परिवार को बचाया।
एक ही व्यक्ति। पाप भी। पुण्य भी।

सूर्यवंश कथा · एपिसोड 16 / 84 · त्रिशंकु (भाग 3 / 6)
In this episode: The prince who stole a bride, fed a sage's family in famine, and killed a sacred cow.

📜 स्रोत: हरिवंश (हरिवंश पर्व, सत्यव्रत की कथा) · संदर्भ: श्रीमद्भागवत 9.7
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:50 पहला दृश्य: विवाह-मंडप
1:28 दूसरा दृश्य: पिता का निर्णय
2:11 तीसरा दृश्य: बारह वर्ष का अकाल
2:43 चौथा दृश्य: गले में रस्सी
3:35 पाँचवाँ दृश्य: पेड़ पर टँगा भोजन
4:09 छठा दृश्य: तीसरा पाप
5:06 सातवाँ दृश्य: विश्वामित्र का ऋण
5:55 समाधान
6:20 समापन

▶ अगला एपिसोड: E17 वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (278/500)
```
त्रिशंकु के तीन पाप: नाम कहाँ से आया, Trishanku's 3 Sins: Where His Name Comes From, त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E17 वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक राजकुमार ने… विवाह-मंडप से… किसी और की दुल्हन उठा ली। 🔱 त्रिशंकु के तीन पाप: नाम कहाँ से आया
पूरी कथा: सूर्यवंश कथा · एपिसोड 16 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E17 · वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा

*Vasishtha's Sons Said No. Vishvamitra Said Yes.* · त्रिशंकु, भाग 4/6 · थंबनेल पर: **एक रात में चांडाल** (English: CURSED TO CHANDALA)

**YouTube title** (68/100)
```
वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा | सूर्यवंश कथा
```
**YouTube description**
```
रात को वह एक राजा था।
सुबह जब उठा… तो उसका रंग बदल चुका था। वस्त्र काले थे। आभूषण लोहे के। गले में श्मशान के फूलों की माला।
उसके मंत्री उसे देखकर भाग गए। प्रजा ने मुँह फेर लिया।
एक रात। एक शाप। और एक राजा… चांडाल।

सूर्यवंश कथा · एपिसोड 17 / 84 · त्रिशंकु (भाग 4 / 6)
In this episode: How Trishanku became an outcast and found the one sage who would help.

📜 स्रोत: वाल्मीकि रामायण, बाल कांड (त्रिशंकु की कथा, शतानंद द्वारा सुनाई गई) · संदर्भ: श्रीमद्भागवत 9.7
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:25 कथा का द्वार
1:00 पहला दृश्य: एक इच्छा
1:33 दूसरा दृश्य: गुरु ने कहा "असंभव"
2:06 तीसरा दृश्य: गुरु-पुत्रों के पास
2:46 चौथा दृश्य: त्रिशंकु का उत्तर
3:17 पाँचवाँ दृश्य: एक रात
4:01 छठा दृश्य: एक ही द्वार बचा
4:45 सातवाँ दृश्य: विश्वामित्र का वचन
5:29 आठवाँ दृश्य: कथा सुनाने वाला कौन था?
6:27 समाधान
6:51 समापन

▶ अगला एपिसोड: E18 विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (297/500)
```
वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा, Vasishtha's Sons Said No. Vishvamitra Said Yes., त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E18 विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
रात को वह एक राजा था। 🔱 वसिष्ठ के पुत्रों ने मना किया, विश्वामित्र ने हाँ कहा
पूरी कथा: सूर्यवंश कथा · एपिसोड 17 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E18 · विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया

*Vishvamitra Built a Second Heaven for 1 King* · त्रिशंकु, भाग 5/6 · थंबनेल पर: **नए तारे** (English: NEW STARS)

**YouTube title** (63/100)
```
विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया | सूर्यवंश कथा
```
**YouTube description**
```
देवताओं ने एक राजा को स्वर्ग में आने नहीं दिया।
तो एक ऋषि ने कहा… "ठीक है। मैं उसके लिए दूसरा स्वर्ग बना दूँगा।"
और उसने आकाश में… नए तारे जलाने शुरू कर दिए।
नए सप्तर्षि। नए नक्षत्र। और फिर… वह एक नया इंद्र बनाने वाला था।

सूर्यवंश कथा · एपिसोड 18 / 84 · त्रिशंकु (भाग 5 / 6)
In this episode: The sacrifice the gods refused, the fall, and the stars Vishvamitra made.

📜 स्रोत: वाल्मीकि रामायण, बाल कांड (त्रिशंकु का यज्ञ और नया स्वर्ग) · संदर्भ: श्रीमद्भागवत 9.7
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:47 पहला दृश्य: निमंत्रण
1:19 दूसरा दृश्य: जो नहीं आए
2:10 तीसरा दृश्य: यज्ञ, और खाली आसन
2:41 चौथा दृश्य: "अपने तप से जाओ"
3:22 पाँचवाँ दृश्य: "उलटे गिरो"
4:00 छठा दृश्य: नया स्वर्ग
4:40 सातवाँ दृश्य: समझौता
5:24 आठवाँ दृश्य: तीन ग्रंथ, एक त्रिशंकु
6:38 समाधान: वचन, जो आधा पूरा हुआ
7:14 समापन

▶ अगला एपिसोड: E19 वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (289/500)
```
विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया, Vishvamitra Built a Second Heaven for 1 King, त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E19 वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
देवताओं ने एक राजा को स्वर्ग में आने नहीं दिया। 🔱 विश्वामित्र ने एक राजा के लिए दूसरा स्वर्ग बनाया
पूरी कथा: सूर्यवंश कथा · एपिसोड 18 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E19 · वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ

*Vasishtha vs Vishvamitra: How the Feud Began* · त्रिशंकु, भाग 6/6 · थंबनेल पर: **कामधेनु छीनी** (English: THE WISH COW)

**YouTube title** (59/100)
```
वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ | सूर्यवंश कथा
```
**YouTube description**
```
एक राजा ने… एक ऋषि पर… सारे दिव्य अस्त्र चला दिए।
अग्नि-अस्त्र। वरुण-अस्त्र। और अंत में… ब्रह्मास्त्र।
और ऋषि के हाथ में था… केवल एक लकड़ी का दंड।
हर अस्त्र… उस दंड में समा गया।

सूर्यवंश कथा · एपिसोड 19 / 84 · त्रिशंकु (भाग 6 / 6)
In this episode: The king who tried to take a cow from a sage, and became a sage to beat him.

📜 स्रोत: वाल्मीकि रामायण, बाल कांड (शबला की कथा और विश्वामित्र का ब्रह्मर्षि बनना) · श्रीमद्भागवत 9.15-16 (विश्वामित्र का वंश) · ऋग्वेद 3.62.10 (गायत्री मंत्र)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:19 कथा का द्वार
0:46 पहला दृश्य: एक राजा, जो ऋषि नहीं था
1:31 दूसरा दृश्य: वसिष्ठ का आतिथ्य
2:17 तीसरा दृश्य: माँग
3:10 चौथा दृश्य: बलपूर्वक
3:54 पाँचवाँ दृश्य: सेनाएँ जो गाय से जन्मीं
4:43 छठा दृश्य: ब्रह्मदंड
5:35 सातवाँ दृश्य: राजा से ब्रह्मर्षि
6:31 समाधान: गायत्री
6:55 समापन

▶ अगला एपिसोड: E20 हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #त्रिशंकु #भागवतपुराण #Trishanku #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (285/500)
```
वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ, Vasishtha vs Vishvamitra: How the Feud Began, त्रिशंकु, Trishanku, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E20 हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक राजा ने… एक ऋषि पर… सारे दिव्य अस्त्र चला दिए। 🔱 वसिष्ठ बनाम विश्वामित्र: झगड़ा कैसे शुरू हुआ
पूरी कथा: सूर्यवंश कथा · एपिसोड 19 (Related video में लिंक)
#Shorts #सूर्यवंश #त्रिशंकु #पौराणिककथा
```

### E20 · हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि

*Harishchandra's Deal With Varuna: A Son, Then a Sacrifice* · राजा हरिश्चंद्र, भाग 1/7 · थंबनेल पर: **कीमत** (English: THE PRICE)

**YouTube title** (62/100)
```
हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि | सूर्यवंश कथा
```
**YouTube description**
```
एक राजा… पुत्र के लिए तड़प रहा था।
उसने जल के देवता वरुण से कहा… "मुझे एक पुत्र दीजिए।"
और फिर उसने एक ऐसा वचन दिया… जिसे सुनकर रोंगटे खड़े हो जाते हैं…
"और उसी पुत्र से… मैं आपके लिए यज्ञ करूँगा। उसकी बलि दूँगा।"

सूर्यवंश कथा · एपिसोड 20 / 84 · राजा हरिश्चंद्र (भाग 1 / 7)
In this episode: A childless king's promise and the birth of Rohita.

📜 स्रोत: श्रीमद्भागवत 9.7 · ऐतरेय ब्राह्मण 7.13 (नारद के पुत्र-विषयक वचन, शुनःशेप-आख्यान का आरंभ)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:55 पहला दृश्य: सौ रानियाँ, एक भी पुत्र नहीं
1:39 दूसरा दृश्य: नारद आए
2:27 तीसरा दृश्य: नारद की सलाह
3:03 चौथा दृश्य: वचन
3:49 पाँचवाँ दृश्य: "तथास्तु"
4:34 छठा दृश्य: वरुण का पहला आगमन
5:03 सातवाँ दृश्य: सत्यवादी का पहला असत्य?
5:53 समाधान
6:11 समापन

▶ अगला एपिसोड: E21 हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (312/500)
```
हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि, Harishchandra's Deal With Varuna: A Son, Then a Sacrifice, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E21 हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक राजा… पुत्र के लिए तड़प रहा था। 🔱 हरिश्चंद्र का वरुण से सौदा: पहले पुत्र, फिर बलि
पूरी कथा: सूर्यवंश कथा · एपिसोड 20 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E21 · हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन

*Harishchandra's 5 Delays: The Son He Promised Varuna* · राजा हरिश्चंद्र, भाग 2/7 · थंबनेल पर: **देवता को टालना** (English: STALLING A GOD)

**YouTube title** (59/100)
```
हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन | सूर्यवंश कथा
```
**YouTube description**
```
एक देवता… पाँच बार एक राजा के द्वार पर आए।
हर बार राजा ने कहा… "थोड़ा और समय।"
और हर बार… देवता मान गए।
पर छठी बार… देवता नहीं आए। और जो आया… वह उससे भी भयानक था।

सूर्यवंश कथा · एपिसोड 21 / 84 · राजा हरिश्चंद्र (भाग 2 / 7)
In this episode: The five times Harishchandra put off Varuna, and the illness that followed.

📜 स्रोत: श्रीमद्भागवत 9.7 · ऐतरेय ब्राह्मण 7.14 (वही पाँच टालमटोल, राजा के कारणों सहित)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:19 कथा का द्वार
0:43 पहला दृश्य: पहली टालमटोल — दस दिन
1:17 दूसरा दृश्य: दूसरी टालमटोल — दाँत आने दो
1:44 तीसरा दृश्य: तीसरी टालमटोल — दाँत गिरने दो
2:25 चौथा दृश्य: चौथी टालमटोल — नए दाँत आने दो
2:54 पाँचवाँ दृश्य: पाँचवीं टालमटोल — कवच
3:30 छठा दृश्य: रोहित को पता चला
4:03 सातवाँ दृश्य: जलोदर
4:41 आठवाँ दृश्य: वरुण का पाश
5:39 समाधान: वरुण ने इतनी प्रतीक्षा क्यों की?
6:06 समापन

▶ अगला एपिसोड: E22 रोहित के छह वर्ष वन में: चलते रहो
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (304/500)
```
हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन, Harishchandra's 5 Delays: The Son He Promised Varuna, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E22 रोहित के छह वर्ष वन में: चलते रहो
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक देवता… पाँच बार एक राजा के द्वार पर आए। 🔱 हरिश्चंद्र की पाँच टालमटोल: वरुण को दिया वचन
पूरी कथा: सूर्यवंश कथा · एपिसोड 21 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E22 · रोहित के छह वर्ष वन में: चलते रहो

*Rohita's 6 Years in the Forest: 'Keep Walking'* · राजा हरिश्चंद्र, भाग 3/7 · थंबनेल पर: **चरैवेति** (English: CHARAIVETI)

**YouTube title** (48/100)
```
रोहित के छह वर्ष वन में: चलते रहो | सूर्यवंश कथा
```
**YouTube description**
```
"जो बैठा है… उसका भाग्य भी बैठ जाता है।
जो खड़ा होता है… उसका भाग्य भी खड़ा होता है।
जो सोता है… उसका भाग्य सो जाता है।
और जो चलता है… उसका भाग्य भी चलता है।

सूर्यवंश कथा · एपिसोड 22 / 84 · राजा हरिश्चंद्र (भाग 3 / 7)
In this episode: The prince who ran, and Indra's verses telling him not to go home.

📜 स्रोत: श्रीमद्भागवत 9.7 · ऐतरेय ब्राह्मण 7.15 (इंद्र के "चरैवेति" श्लोक)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:30 कथा का द्वार
0:57 पहला दृश्य: वन का एकांत
1:31 दूसरा दृश्य: पिता बीमार हैं
2:05 तीसरा दृश्य: एक ब्राह्मण रास्ता रोकता है
2:44 चौथा दृश्य: पहला श्लोक — बैठे का भाग्य
3:22 पाँचवाँ दृश्य: युग चलने में हैं
3:57 छठा दृश्य: शहद और सूर्य
4:44 सातवाँ दृश्य: छठा वर्ष
5:06 आठवाँ दृश्य: "इंद्र चलने वाले का मित्र है"
6:03 समाधान: चरैवेति आज
6:26 समापन

▶ अगला एपिसोड: E23 शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (287/500)
```
रोहित के छह वर्ष वन में: चलते रहो, Rohita's 6 Years in the Forest: 'Keep Walking', राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E23 शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
"जो बैठा है… उसका भाग्य भी बैठ जाता है। 🔱 रोहित के छह वर्ष वन में: चलते रहो
पूरी कथा: सूर्यवंश कथा · एपिसोड 22 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E23 · शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया

*Shunahshepha: The Boy Bought to Die in a Prince's Place* · राजा हरिश्चंद्र, भाग 4/7 · थंबनेल पर: **पिता ने बेचा** (English: SOLD BY HIS FATHER)

**YouTube title** (69/100)
```
शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया | सूर्यवंश कथा
```
**YouTube description**
```
एक बालक… यज्ञ के खंभे से बँधा था।
कोई उसे बाँधने को तैयार नहीं था। तो उसके पिता ने… सौ गायें और लेकर… उसे बाँधा।
कोई उसे मारने को तैयार नहीं था। तो उसके पिता ने… सौ गायें और लेकर… छुरी तेज़ करनी शुरू की।
और उस बालक ने… आँखें बंद कीं… और देवताओं को पुकारा।

सूर्यवंश कथा · एपिसोड 23 / 84 · राजा हरिश्चंद्र (भाग 4 / 7)
In this episode: The boy bought from Ajigarta, his prayers at the post, and how he became Devarata.

📜 स्रोत: श्रीमद्भागवत 9.7 (यज्ञ) · 9.16 (देवरात) · ऐतरेय ब्राह्मण 7.15-18 (शुनःशेप-आख्यान) · वाल्मीकि रामायण, बाल कांड (अलग संस्करण)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:24 कथा का द्वार
0:50 पहला दृश्य: तीन पुत्र, एक सौदा
1:38 दूसरा दृश्य: यज्ञ की तैयारी
2:09 तीसरा दृश्य: कोई बाँधने को तैयार नहीं
2:56 चौथा दृश्य: देवताओं को पुकार
3:31 पाँचवाँ दृश्य: एक-एक बंधन
4:14 छठा दृश्य: "तुम छुरी लेकर खड़े थे"
4:41 सातवाँ दृश्य: देवरात
5:32 आठवाँ दृश्य: शुनःशेप का पहला प्रश्न
6:30 समाधान: एक कथा, दो रामायण
7:00 समापन

▶ अगला एपिसोड: E24 दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (317/500)
```
शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया, Shunahshepha: The Boy Bought to Die in a Prince's Place, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E24 दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक बालक… यज्ञ के खंभे से बँधा था। 🔱 शुनःशेप: वह बालक जो दूसरे की जगह मरने के लिए खरीदा गया
पूरी कथा: सूर्यवंश कथा · एपिसोड 23 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E24 · दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया

*The Other Harishchandra, Part 1: He Gave Away His Kingdom* · राजा हरिश्चंद्र, भाग 5/7 · थंबनेल पर: **भागवत में नहीं** (English: NOT IN BHAGAVATA)

**YouTube title** (63/100)
```
दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया | सूर्यवंश कथा
```
**YouTube description**
```
एक राजा ने… एक वचन के लिए… अपना पूरा राज्य दान कर दिया।
फिर ऋषि ने कहा… "अब दक्षिणा दो।"
राजा के पास कुछ नहीं बचा था। न राज्य। न धन। न घर।
तो उसने अपनी पत्नी को बेचा। अपने पुत्र को बेचा।

सूर्यवंश कथा · एपिसोड 24 / 84 · राजा हरिश्चंद्र (भाग 5 / 7)
In this episode: The truth-test story most people know, and why it comes from a different Purana.

📜 स्रोत: मार्कंडेय पुराण, अध्याय 7-8 (हरिश्चंद्रोपाख्यान) · यह कथा भागवत में नहीं है
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:23 कथा का द्वार
0:51 पहला दृश्य: वन में रोती स्त्रियाँ
1:27 दूसरा दृश्य: एक क्रोध का क्षण
1:59 तीसरा दृश्य: "जो माँगें, वह दूँगा"
2:39 चौथा दृश्य: दक्षिणा
3:32 पाँचवाँ दृश्य: काशी
4:04 छठा दृश्य: पत्नी ने कहा, "मुझे बेच दीजिए"
4:46 सातवाँ दृश्य: और अभी भी कम था
5:10 आठवाँ दृश्य: काशी किसी राजा की क्यों नहीं?
6:04 समाधान: यह परीक्षा क्यों?
6:32 समापन

▶ अगला एपिसोड: E25 दूसरा हरिश्चंद्र, भाग 2: श्मशान
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (313/500)
```
दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया, The Other Harishchandra, Part 1: He Gave Away His Kingdom, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E25 दूसरा हरिश्चंद्र, भाग 2: श्मशान
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
एक राजा ने… एक वचन के लिए… अपना पूरा राज्य दान कर दिया। 🔱 दूसरा हरिश्चंद्र, भाग 1: जिसने राज्य दान कर दिया
पूरी कथा: सूर्यवंश कथा · एपिसोड 24 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E25 · दूसरा हरिश्चंद्र, भाग 2: श्मशान

*The Other Harishchandra, Part 2: The Cremation Ground* · राजा हरिश्चंद्र, भाग 6/7 · थंबनेल पर: **अपना ही पुत्र** (English: HIS OWN SON)

**YouTube title** (46/100)
```
दूसरा हरिश्चंद्र, भाग 2: श्मशान | सूर्यवंश कथा
```
**YouTube description**
```
आधी रात। श्मशान।
एक स्त्री आई… अपने मृत पुत्र को गोद में लिए। चिता के लिए।
और श्मशान के रखवाले ने कहा… "पहले कर दो।"
स्त्री ने उसकी ओर देखा। और पहचान लिया।

सूर्यवंश कथा · एपिसोड 25 / 84 · राजा हरिश्चंद्र (भाग 6 / 7)
In this episode: Kashi, the sale of his wife and son, Rohita's death, and the end of the test.

📜 स्रोत: मार्कंडेय पुराण, अध्याय 8 (हरिश्चंद्रोपाख्यान) · गांधी, "सत्य के प्रयोग" (आत्मकथा), भाग 1 · यह कथा भागवत में नहीं है
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:41 पहला दृश्य: स्वयं को बेचा
1:27 दूसरा दृश्य: श्मशान का रखवाला
2:04 तीसरा दृश्य: साँप
2:43 चौथा दृश्य: "कर दो"
3:14 पाँचवाँ दृश्य: फिर भी कर
4:15 छठा दृश्य: देवता प्रकट हुए
4:47 सातवाँ दृश्य: प्रजा के बिना नहीं
5:35 आठवाँ दृश्य: हरिश्चंद्र घाट
6:28 समाधान: एक बालक, जो रोया
7:08 समापन

▶ अगला एपिसोड: E26 दो ऋषि एक राजा के लिए पक्षी बनकर लड़े
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (292/500)
```
दूसरा हरिश्चंद्र, भाग 2: श्मशान, The Other Harishchandra, Part 2: The Cremation Ground, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E26 दो ऋषि एक राजा के लिए पक्षी बनकर लड़े
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
आधी रात। श्मशान। 🔱 दूसरा हरिश्चंद्र, भाग 2: श्मशान
पूरी कथा: सूर्यवंश कथा · एपिसोड 25 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```

### E26 · दो ऋषि एक राजा के लिए पक्षी बनकर लड़े

*Two Sages Fought as Birds Over 1 King* · राजा हरिश्चंद्र, भाग 7/7 · थंबनेल पर: **वर्षों का युद्ध** (English: YEARS OF WAR)

**YouTube title** (52/100)
```
दो ऋषि एक राजा के लिए पक्षी बनकर लड़े | सूर्यवंश कथा
```
**YouTube description**
```
दो ऋषि।
एक ने दूसरे को शाप दिया… "तुम बगुला बन जाओ।"
दूसरे ने उत्तर में शाप दिया… "और तुम आडी पक्षी।"
और फिर… दो विशाल पक्षी… आकाश में भिड़ गए। पर्वत हिले। समुद्र उफने। और यह युद्ध… वर्षों चला।

सूर्यवंश कथा · एपिसोड 26 / 84 · राजा हरिश्चंद्र (भाग 7 / 7)
In this episode: Vasishtha and Vishvamitra's years-long battle in bird form, and who started it.

📜 स्रोत: श्रीमद्भागवत 9.7 (युद्ध का उल्लेख) · मार्कंडेय पुराण, अध्याय 9 (आडी-बक युद्ध का विस्तार)
हर कथा के स्रोत स्क्रीन पर दिखाए गए हैं। जहाँ कथा लोक-परंपरा या बाद के ग्रंथों से है, वहाँ भी बताया गया है।

⏱ अध्याय
0:00 हुक
0:22 कथा का द्वार
0:44 पहला दृश्य: भागवत की एक पंक्ति
1:22 दूसरा दृश्य: जल से लौटे वसिष्ठ
2:05 तीसरा दृश्य: शाप
2:38 चौथा दृश्य: उत्तर में शाप
3:14 पाँचवाँ दृश्य: आकाश का युद्ध
3:58 छठा दृश्य: ब्रह्मा आए
4:30 सातवाँ दृश्य: एक झगड़ा, पूरी शृंखला में
5:27 आठवाँ दृश्य: "बक-वृत्ति"
6:23 समाधान
6:52 समापन

▶ अगला एपिसोड: E27 रोहित से बाहुक तक: सूर्यवंश ने अयोध्या कैसे खोई
▶ पूरी शृंखला (प्लेलिस्ट): [link]

वाचन: AI आवाज़ (ElevenLabs) · चित्र: AI से बनाए गए (Google) · पटकथा: स्रोत-ग्रंथों पर आधारित
Narration: AI voice (ElevenLabs) · Illustrations: AI-generated (Google) · Script: written from the cited texts

#सूर्यवंश #राजाहरिश्चंद्र #भागवतपुराण #Harishchandra #Suryavansh #हिंदूपौराणिककथा #IndianMythology #BhagavataPurana #पौराणिककथा #सनातनधर्म #HindiKahani #Mythology
```
**YouTube tags field** (282/500)
```
दो ऋषि एक राजा के लिए पक्षी बनकर लड़े, Two Sages Fought as Birds Over 1 King, राजा हरिश्चंद्र, Harishchandra, सूर्यवंश, Suryavansh, सूर्यवंश कथा, भागवत पुराण, Bhagavata Purana, Srimad Bhagavatam, हिंदू पौराणिक कथा, Hindu mythology, Ikshvaku dynasty, रामायण, Hindi story, पौराणिक कथा
```
**YouTube pinned comment**
```
आपके अनुसार, इस कथा में सबसे कठिन निर्णय किसका था? 👇
अगला एपिसोड: E27 रोहित से बाहुक तक: सूर्यवंश ने अयोध्या कैसे खोई
```
**YouTube Short** (optional: 30-60 s vertical clip of the hook, linked to the full episode)
```
दो ऋषि। 🔱 दो ऋषि एक राजा के लिए पक्षी बनकर लड़े
पूरी कथा: सूर्यवंश कथा · एपिसोड 26 (Related video में लिंक)
#Shorts #सूर्यवंश #राजाहरिश्चंद्र #पौराणिककथा
```
