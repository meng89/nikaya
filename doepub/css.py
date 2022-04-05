from pyccc.book_public import TC, SC


public = """
body.sutta p{
    margin: 0.3em;
}

body.sutta a,
body.homage a{
    color: inherit;
}

body.note ol{
    list-style:none;
}

.title{
    text-decoration: inherit;
}
"""

public_path = "_css/public.css"


_font = """
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


font_css = {TC().enlang: _font,
            SC().enlang: _font.replace("CJK TC", "CJK SC")}


font_path = {TC().enlang: "_css/tcfont.css",
             SC().enlang: "_css/scfont.css"}
