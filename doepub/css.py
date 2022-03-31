from pyccc.book_public import TC, SC


public = """
body.sutta p{
    margin: 0.3em;
}

body.sutta a{
    color: inherit;
}

body .title{
    text-decoration: inherit;
}
"""

public_path = "_css/public.css"


_tc_font = """
p{
    font-family: "Noto Serif CJK TC", "Noto Serif", "Noto Serif Tibetan";
    font-weight: 500;
}
.title{
    font-family: "Noto Sans CJK TC";
    font-weight: 700;
}
"""

_sc_font = """
p{
    font-family: "Noto Serif", "Noto Serif CJK SC", "Noto Serif Tibetan";
    font-weight: 500;
}

.title{
    font-family: "Noto Sans CJK SC";
    font-weight: 700;
}
"""


_tc_font2 = """
@font-face {
    font-family: MySerif;
    src: local('Noto Serif CJK TC');
    /* unicode-range: U+4E00-U+9FFF, U+3400-U+4DBF, U+2B740–U+2B81F; */
}

@font-face {
    font-family: MySerif;
    src: local('Noto Serif Tibetan');
    /* unicode-range: U+0F00-U+0FFF; */
}

@font-face {
    font-family: MySerif;
    src: local('Noto Serif');
}



@font-face {
    font-family: MySans;
    src: local('Noto Sans CJK TC');
}
@font-face {
    font-family: MySans;
    src: local('Noto Sans');
}


body{
    font-family: MySerif;
    font-weight: 400;
}
.title{
    font-family: MySans;
}

"""

_sc_font2 = """
@font-face {
    font-family: MySerif;
    src: local('Noto Serif CJK SC');
    /* unicode-range: U+4E00-U+9FFF, U+3400-U+4DBF, U+2B740–U+2B81F; */
}

@font-face {
    font-family: MySerif;
    src: local('Noto Serif Tibetan');
    /* unicode-range: U+0F00-U+0FFF; */
}

@font-face {
    font-family: MySerif;
    src: local('Noto Serif');
}



@font-face {
    font-family: MySans;
    src: local('Noto Sans CJK SC');
}
@font-face {
    font-family: MySans;
    src: local('Noto Sans');
}


body{
    font-family: MySerif;
}
.title{
    font-family: MySans;
}

"""

_font3 = """
.cjk{
    font-family: "Noto Serif CJK TC";
    font-weight: 400;
}

.lat{
    font-family: "Noto Serif";
    font-weight: 300;
}

.tib{
    font-family: "Noto Serif Tibetan";
    font-weight: 400;
}

.title{
    font-family: "Noto Sans CJK TC";
    font-weight: 500;
}

body.notice{
    font-family: "Noto Serif CJK TC";
    font-weight: 400;
}

"""


font_css = {TC().enlang: _font3,
            SC().enlang: _font3.replace("CJK TC", "CJK SC")}


font_path = {TC().enlang: "_css/tcfont.css",
             SC().enlang: "_css/scfont.css"}
