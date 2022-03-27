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
_tc_font2 = """
@font-face {
  font-family: "MySerif";
  src: local("Noto Serif");
}
@font-face {
  font-family: "MySerif";
  src: local("Noto Serif CJK TC");
  unicode-range: U+0-2FF;
}
@font-face {
  font-family: "MySerif";
  src: local("Noto Serif Tibetan");
  unicode-range: U+0F00-U+0FFF;
}

@font-face {
  font-family: "MySans";
  src: local("Noto Sans");
}
@font-face {
  font-family: "MySans";
  src: local("Noto Sans CJK TC");
  unicode-range: U+0-2FF;
}

p{
    font-family: "MySerif";
    font-weight: 400;
}
.title{
    font-family: "MySans";
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


font_css = {TC().enlang: _tc_font2,
            SC().enlang: _sc_font}

font_path = {TC().enlang: "_static/tcfont.css",
             SC().enlang: "_static/scfont.css"}
