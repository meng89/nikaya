from pyabo.book_public import TC, SC


public = """

.title a {
    color: inherit;
    text-decoration: inherit;
}

body.sutta p {
    margin: 0.3em;
}

.tail_number {
    font-size: small;
}

a.noteref {
    color: inherit;
    text-decoration: none;
    border-bottom: 0.05em dashed;
}

body.note ol {
    list-style: none;
}


a.suttaref_inbook {
    text-decoration: inherit;
    border-bottom:  dashed #ccc;
    color:#c00;
}
"""

public_path = "_css/public.css"


_font = """
.cjk {
    font-family: "Noto Serif CJK TC";
    font-weight: 400;
}

.lat {
    font-family: "Noto Serif";
    font-weight: 300;
}

.tib {
    font-family: "Noto Serif Tibetan";
    font-weight: 400;
}

.title {
    font-family: "Noto Sans CJK TC";
    font-weight: 600;
}

.subtitle {
    font-family: "Noto Serif CJK TC";
    font-weight: 700;
}

.tail_number {
    font-family: "Noto Serif";
    font-weight: 300;
}

body.notice {
    font-family: "Noto Serif CJK TC";
    font-weight: 400;
}

"""


font_css = {TC().enlang: _font,
            SC().enlang: _font.replace("CJK TC", "CJK SC")}


font_path = {TC().enlang: "_css/tcfont.css",
             SC().enlang: "_css/scfont.css"}
