# Picture rules (learned from the reviews of Episodes 1 and 2)

Every picture is drawn **once** (gemini-2.5-flash-image, about $0.04 each). There are no redraws, so
the description must be right the first time. These rules come from the 90 + 39 + 30 mistakes three
independent reviews found in Episodes 1-2. Follow all of them.

## The model's weak spots (write around them)

1. **Counting.** It cannot reliably draw exactly N people when N > 4 (it drew 8 and 9 sages for 7).
   If a number matters, show at most 3-4 clearly; for larger groups, frame them so the count can't be
   checked (a crowd, figures running out of frame, figures in shadow), and never write "seven" in
   the prompt in a way that invites counting. For 2-4 people, list each one with his position
   ("on the left ..., in the middle ..., on the right ...").
2. **Duplicated props.** It adds a second bow, crown or weapon. Always write "exactly one bow",
   say WHICH hand holds it or that it is slung on the back on a visible strap, and add "no other
   bow anywhere in the picture".
3. **Extra arms.** When a figure both holds something and folds hands, it adds a third arm. Give
   each hand one job: "his left hand holds ..., his right hand ...". Write "exactly two arms" for
   humans; for gods with four arms say "exactly four arms" and what each holds.
4. **Physical contact.** It cannot draw a rope tied to a specific point, a weapon touching a target
   or a hand placing something precisely. Avoid making the story depend on contact; show the moment
   before or after (the demon already falling, the rope already knotted and running in a straight
   line), and describe it as a clear spatial path.
5. **Beards and age drift.** A young man gets a beard unless told "clean-shaven, no beard, no
   moustache". Old men lose their grey beards unless told "long grey beard". Repeat the full
   character description in EVERY prompt where the character appears.
6. **Writing.** It writes fake letters on books, maps, banners, robes and corners, and sometimes a
   fake signature or logo. Always end with "no text, no letters, no writing, no signature". Books
   are palm-leaf pothi bundles tied with cord, never bound Western books. Maps show only drawn
   rivers, hills and forests.
7. **Modern things.** It adds asphalt roads, collared shirts, buttons, glass windows, Western crowns,
   dragons, gargoyles. Name the period item instead: "dusty earth track", "plain cotton dhoti and
   cloth wrap", "tall tiered Indian golden crown (mukut)", "carved stone jharokha window".
8. **Fire.** It adds stray fires and puts flames in people's laps. Say where the fire is and that
   it is "well in front of", "at a distance"; add "no other fires" when there should be none.
9. **Comic faces.** Gods and divine animals turn goofy (gaping mouths, bulging eyes, whiskers).
   Add "calm, dignified, serious face, mouth closed" and "not cartoonish, not comic".
10. **Cute animals.** Animals that are food, prey or offerings come out as cute pets. Show them
    wrapped, distant or as a symbol; never ask for a close-up of an animal that is eaten or killed.
11. **Blinks and subtle states.** It draws eyes open. Use a clearly closed eye, a clearly sleeping
    figure, etc., not "half-closed".

## Story rules

12. The picture must show **what is said while it is on screen**. A picture appears at its
    "starts at" words and stays until the next picture's words. Don't let one picture stay longer
    than about 20 seconds unless the narration stays on that same image the whole time; add a
    picture when the narration changes subject (a teaching, a moral, a different character).
13. Hold back what the narration hasn't revealed yet (no boat before "a boat came").
14. Iconography: Brahma = four faces on one head, three visible, elderly, white beard; Vishnu =
    blue, exactly four arms (conch, discus, mace, lotus); Shiva = blue skin, blue throat, matted
    locks, one small crescent moon, serpent at the neck, tiger skin; Indra = golden-skinned king of
    the gods with a thunderbolt (vajra), on the white elephant Airavata when riding; Shri Ram = blue
    skin, exactly one golden bow. Sages wear saffron or ochre, have long white or grey beards and
    hair tied in a top-knot.
15. Use the character sheet (characters.md) words exactly for every recurring character.

## Format

16. Each prompt is the [SCENE] part only; the style prefix is added automatically. Write it in
    English, 40-90 words, concrete and visual: who, where, doing what, light, mood.
17. The "starts at" column holds 2-6 Hindi words copied **exactly** from one narration piece, unique
    in the episode, at the point the picture should appear. The first picture starts at the first
    words of the episode.
