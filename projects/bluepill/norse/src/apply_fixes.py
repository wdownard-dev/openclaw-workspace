import re
P='/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src/'
lines=open(P+'beats.txt').read().split('\n')
# (old text key) -> dict(text=, shot=, trace=)
F={
"and every one of them is doomed.":dict(text="and all of it will burn.",trace="Voluspa 45-57 (the destruction); Gylf 4 and 51 ('burn all the world') V"),
"The gods know it,":dict(text="Odin knows it,",trace="(ours) framing; basis Voluspa 28-30 (Odin consults the seeress)"),
"because they have heard their own ending.":dict(text="because a seeress told him his own ending.",trace="Voluspa 1, 28-30 V"),
"Odin gave an eye for wisdom,":dict(trace="Voluspa 28-29 V; Gylf 15 V"),
"The end comes anyway,":dict(trace="Voluspa 45-57 V"),
"His skull becomes the sky, held up by four dwarfs.":dict(trace="Grimnismal 40 (skull as sky) V; Gylf 8 (four dwarfs, East, West, North, South) V"),
"Not bad for a day's work.":dict(text="Not bad for three brothers.",trace="(ours) dry beat; the three brothers are Gylf 6-8"),
"Along the shore they find two fallen trees.":dict(trace="Gylf 9 V (the two trees); Voluspa 17 has 'two without fate' and no trees"),
"At the well of the giant Mimir, Odin trades one eye for a drink.":dict(text="At the well of Mimir, Odin trades one eye for a drink.",trace="Voluspa 28-29 V; Gylf 15 V (Mimir keeps the well; Brodeur does not call him a giant)"),
"That is why Odin has one eye, a wide hat, and a lot of secrets.":dict(trace="(ours) one eye Voluspa 29 and Gylf 15 V; wide hat = Odin's name Sidhottr 'With Broad Hat', Grimnismal 48 V; 'a lot of secrets' is our joke"),
"So the gods send to the dwarfs, who weave a ribbon called Gleipnir.":dict(text="So the gods send to the dwarfs, who make a cord called Gleipnir.",trace="Gylf 34 V (Brodeur: 'fetter named Gleipnir', 'soft and smooth as a silken ribbon'; Skirnir is sent)"),
"It is made of six things: a cat's footstep, a woman's beard,":dict(text="It is made of six things: the sound of a cat's step, a woman's beard,",shot="close: the dwarfs' hands dropping a few faint curved sound-lines for a cat's soft step, then a curl of beard, into a pot",trace="Gylf 34 V (noise a cat makes in foot-fall; beard of a woman)"),
"a mountain's roots, a bear's sinews, a fish's breath, and a bird's spit.":dict(trace="Gylf 34 V (Brodeur: roots of a rock; Bellows note on Voluspa 39 quotes 'roots of mountains')"),
"Thor is the god of thunder, with a red beard and a hammer named Mjolnir.":dict(text="Thor is the god of thunder, strongest of them all, with a hammer named Mjolnir.",trace="Gylf 21 V (strongest of all gods and men; Mjollnir). 'God of thunder' is the standard description, not a word in Gylf 21. Red beard not in Brodeur or Bellows: visual design only, never narrated"),
"The gods beg Hel to give him back.":dict(text="Odin's son rides to Hel, and begs her to give him back.",shot="medium, dusk: a lone hooded rider on a grey horse at a black stone gate, Hel's split-faced figure beyond it",trace="Gylf 49 V (Hermod, Odin's son, rides to Hel; he is not named in the narration)"),
"The sons of Muspell":None,
"Fire giants ride from the south, led by Surt, with a flaming sword.":dict(text="The sons of Muspell ride from the south, led by Surt, with a flaming sword.",trace="Gylf 51 V; Voluspa 52 V (Brodeur: 'Sons of Muspell'; they are not called giants)"),
"The wolf goes for Odin and swallows him whole.":dict(text="The wolf goes for Odin and swallows him.",trace="Gylf 51 V ('The Wolf shall swallow Odin')"),
"Odin's son Vidar puts one boot on the wolf's jaw,":dict(trace="Gylf 51 V (Vidar sets one foot on the lower jaw)"),
"and tears it apart.":dict(text="and tears the wolf's throat apart.",trace="Gylf 51 V (Prose Edda: tears the gullet asunder; Voluspa 54 has a sword to the heart, not used)"),
"Then Surt flings fire across every world.":dict(text="Then Surt flings fire across the earth.",trace="Gylf 51 V ('burn all the world'); Voluspa 52, 57 V"),
"The mistletoe goes straight through Baldr, and he falls dead.":dict(trace="Gylf 49 V; Voluspa 32-33 V"),
"None of this was written down by the people who first told it.":dict(text="None of this was written down when the poems were first made.",trace="(ours) basis: Bellows, Voluspa introductory note ('two hundred years between its composition and its first being committed to writing') V; Bellows general introduction (collections written by the 12th century)"),
"For centuries it was spoken, from memory, on long winter nights.":dict(text="For generations it was recited from memory by poets.",trace="(ours) basis: Bellows (as above); 'winter nights' dropped, no source"),
"The poems survive in one great book, the Codex Regius, from about twelve seventy.":dict(text="Most of the poems survive in one great book, the Codex Regius, from about twelve seventy.",trace="Codex Regius (GKS 2365 4to), 1270s (Wikipedia, Codex Regius; sole source for most of its poems) V; Bellows intro: other poems survive elsewhere (AM 748, Hauksbok)"),
"It was written in Iceland, by Christians, about gods nobody worshipped anymore.":dict(trace="(ours) Iceland legally Christian in 1000 (Wikipedia, Christianization of Iceland) V; Bellows intro: Regius is a copy made about a hundred years after the 12th-century collections"),
"Around twelve twenty, a chieftain named Snorri Sturluson wrote a handbook for poets.":dict(text="Around twelve twenty, an Icelandic chieftain named Snorri Sturluson put together a handbook for poets.",trace="Prose Edda c. 1220 (Wikipedia, Prose Edda: 'to some extent written, or at least compiled, by Snorri c. 1220'); Brodeur intro: a book for apprentice poets V"),
"Snorri was a Christian too,":dict(trace="(ours) basis: Brodeur intro (Snorri's address to beginners: the tales are 'neither to be believed nor to be tampered with'); Prologue opens with the Christian creation V"),
"and he begins by saying the gods were once men from Asia.":dict(text="and his book opens with Adam and Eve, then says the gods were once men from Asia.",trace="Prose Edda Prologue (Brodeur p. 1-9: Adam and Eve, then the Aesir as men of Asia, from Troy) V; Brodeur intro: many scholars consider the Prologue spurious"),
"He was killed in twelve forty-one, on the orders of a Norwegian king.":dict(trace="Brodeur intro (Gizurr Thorvaldsson, 1241, 'at the express order of the King', Hakon Hakonarson) V; Wikipedia, Snorri: 23 Sept 1241, Reykholt, killed in the cellar"),
}
del F["The sons of Muspell"]
# traces for Gylf 47 -> 48 handled by beat texts below
FISHING=["One day he sets out to find the serpent,","disguised as a young man.","He comes to a giant named Hymir,","who does not think the stranger will be much use on a boat.","Thor takes the head of the biggest ox on the farm for bait.","They row out, and Hymir says they are far enough,","but Thor says row further.","Hymir grows pale.","Thor ties the ox head to a hook,","and throws it into the deep,","and the serpent bites.","Thor pulls so hard his feet go through the bottom of the boat,","and he braces himself on the sea floor."]
out=[];state_fix=0;used=set()
for l in lines:
    if l.startswith('@S ') and l[3:].startswith("Hel's gate; dusk; 3 present: Hel, Odin, Thor"):
        l="@S Hel's gate; dusk; 2 present: Hel, a hooded rider (Hermod, Odin's son, unnamed); the rider pleads"; state_fix+=1
    elif '||' in l:
        p=[x.strip() for x in l.split('||')]
        k=p[0]
        if k in F:
            d=F[k]; used.add(k)
            p[0]=d.get('text',p[0]); p[1]=d.get('shot',p[1]); p[2]=d.get('trace',p[2])
        if k in FISHING:
            used.add('F:'+k)
            p[2]=p[2].replace('Gylf 47','Gylf 48') if 'Gylf 47' in p[2] else p[2]
        l=' || '.join(p)
    out.append(l)
open(P+'beats2.txt','w').write('\n'.join(out))
print('fixes used',len([u for u in used if not u.startswith('F:')]),'of',len(F),'fishing',len([u for u in used if u.startswith('F:')]),'of',len(FISHING),'state',state_fix)
print([k for k in F if k not in used])
