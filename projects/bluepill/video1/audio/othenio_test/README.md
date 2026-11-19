# Othenio Abel pronunciation candidates (2026-11-12)

Voice George (JBFqnCBsd6RMkjVDRZzb), stability 0.75, similarity 0.75, style 0.05, speaker boost on, speed 1.0, mp3_44100_192, /with-timestamps.
previous_text: "During the Ice Age, dwarf elephants lived on islands across the Mediterranean." (no next_text). Script: gen_cands.py, raw data: results.json.
Template: `In 1914, the palaeontologist <NAME> thought there might be.`

| # | model | text sent for NAME | chars | name dur (s) | clip total (s) |
|---|---|---|---|---|---|
| 1 | eleven_multilingual_v2 | Othenio Abel (control) | 65 | 0.89 | 4.55 |
| 2 | eleven_multilingual_v2 | Oh-tay-nyo Ah-bel | 70 | 1.30 | 5.11 |
| 3 | eleven_multilingual_v2 | Otenyo Ahbel | 65 | 1.06 | 4.78 |
| 4 | eleven_multilingual_v2 | Oh-TAY-nee-oh AH-bull | 74 | 1.81 | 5.71 |
| 5 | eleven_multilingual_v2 | Ottaynio Abel | 66 | 0.85 | 4.46 |
| 6 | eleven_multilingual_v2 | Oh-teh-nee-oh Ah-bel | 73 | 1.35 | 5.16 |
| 7 | **eleven_turbo_v2_5 (different model; voice may differ slightly)** | `<phoneme alphabet="ipa" ph="oˈteːnjo">Othenio</phoneme> <phoneme alphabet="ipa" ph="ˈaːbl̩">Abel</phoneme>` | 159 | n/a (alignment collapsed the tag span to a point at 2.31s) | 3.53 |

Cand 7: API accepted the request, but the clip is ~1s shorter than the control, so the name may be clipped or skipped. Treat with suspicion.

## Where Othenio / Abel are spoken (beats.py -> voice.py chunks)
- beats.py line 71, ch3: "In 1914, the palaeontologist Othenio Abel thought there might be." -> chunk 6
- beats.py line 80, ch3: "Abel pictured a sailor, ..." -> chunk 6
- beats.py line 92, ch3: "Abel claimed that the philosopher Empedocles ..." -> chunk 8
- Not spoken (notes only): beats.py lines 21, 22, 82 (Abel in image notes / overlay codes).
- voice.py RESPELL table: ("Othenio", env OTHENIO_RESP, default "Oh-TAY-nee-oh") and ("Abel", env ABEL_RESP, default "AH-bel"), line 15; comment lines 12-14.

## Consistency
Chunk 8 (saved c08.json) was sent "Ah-bel" (the older respelling); chunk 6 was re-recorded with "AH-bel". Abel appears 2x in chunk 6, 1x in chunk 8. If the winner changes the Abel spelling, chunk 6 and chunk 8 must both be re-recorded to stay consistent. If only the Othenio part changes, re-record chunk 6 only (OTHENIO_RESP=... python3 voice.py gen 6 --force, VSPEED=1.0).
