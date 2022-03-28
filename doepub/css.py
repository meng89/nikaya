from pyccc.book_public import TC, SC


sutta_css = """
p{margin: 0.3em;}
a{
    color: inherit;
}

.title{
    text-decoration: inherit;
}
"""
sutta_css_path = "_static/sutta.css"


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

_tc_font3 = """
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
    font-weight: 700;
}
"""


_sc_font3 = """
.cjk{
    font-family: "Noto Serif CJK SC";
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
    font-family: "Noto Sans CJK SC";
    font-weight: 700;
}
"""


font_css = {TC().enlang: _tc_font3,
            SC().enlang: _sc_font3}

font_path = {TC().enlang: "_static/tcfont.css",
             SC().enlang: "_static/scfont.css"}
