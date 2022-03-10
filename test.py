#!/usr/bin/env python3

from pyccc.lang_convert import convert2sc
s = """

對那位世尊、阿羅漢、遍正覺者禮敬
相應部
(1)有偈篇
1.諸天相應
1.蘆葦品
相應部1相應1經/暴流之渡過經(諸天相應/有偈篇/祇夜)(莊春江譯)
　　被我這麼聽聞：
　　有一次，世尊住在舍衛城祇樹林給孤獨園。那時，在夜已深時，容色絕佳的某位天神使整個祇樹林發光後，去見世尊。抵達後，向世尊問訊，接著在一旁站立。在一旁站立的那位天神對世尊說這個：
　　「親愛的先生！你怎樣渡過暴流呢？」
　　「朋友！我無住立、無用力地渡過暴流。」
　　「親愛的先生！那麼，依怎樣的方式你無住立、無用力地渡過暴流呢？」
　　「朋友！當我住立時，那時，我沈沒；朋友！當我用力時，那時，我被飄走，朋友！這樣，我無住立、無用力地渡過暴流。」
　　「終於我確實看見，般涅槃的婆羅門：
　　　無住立、無用力地，已度脫世間中的執著。」
　　那位天神說這個，大師是認可者。那時，那位天神[心想]：「大師對我是認可者。」向世尊問訊，然後作右繞，接著就在那裡消失了。 

"""

s = """　　「終於我確實看見，般涅槃的婆羅門：
　　　無住立、無用力地，已度脫世間中的執著。」"""

print(repr(s))
print(repr(convert2sc(s)))

