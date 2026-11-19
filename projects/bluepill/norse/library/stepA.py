from common import *
d="Odin: tall old man, a BLACK EYE PATCH over one eye with a thin black strap across the head, ONE small dot eye on the other side, wide-brimmed blue-grey hat, long grey beard to the belly, dark blue cloak pinned at the throat."
ref="Match only the drawing style, line weight and shading of the attached reference image; change the character entirely (different face, hat, beard, clothes, colours). "
wp('odin_turn_ref',P(ref+TURN,d))
wp('odin_turn_noref',P(TURN,d))
