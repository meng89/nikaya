from pyabo.book_public import TC, SC


_css1 = """
/* koreader 只支持部分 CSS 功能
*/
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
}

body.note ol {
    list-style: none;
}

a.suttaref_inbook {
    color: inherit;
}

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
    font-family: "Noto Serif Light Italic";
    font-weight: 300;
}

body.notice {
    font-family: "Noto Serif CJK TC";
    font-weight: 400;
}

"""

_css2 = """

@font-face {
    font-family: MySerif;
    src: local('Noto Serif CJK TC Light');
    unicode-range: U+4E00-U+9FFF, U+3400-U+4DBF, U+2B740–U+2B81F;
}
@font-face {
    font-family: MySerif;
    src: local('Noto Serif Tibetan Light');
    unicode-range: U+0F00-U+0FFF;
}
@font-face {
    font-family: MySerif;
    src: local('Noto Serif Light');
}
@font-face {
    font-family: MySerifItalic;
    src: local('Noto Serif Light Italic');
}

@font-face {
    font-family: MySerifBold;
    src: local('Noto Serif CJK TC SemiBold');
    unicode-range: U+4E00-U+9FFF, U+3400-U+4DBF, U+2B740–U+2B81F;
}

@font-face {
    font-family: MySansMedium;
    src: local('Noto Sans CJK TC Medium');
}

@font-face {
    font-family: MySansMedium;
    src: local('Noto Sans Medium');
}


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
    border-bottom: 0.08em dashed;
}

body.note ol {
    list-style: none;
}


a.suttaref_inbook {
    text-decoration: inherit;
    border-bottom:  dashed #ccc;
    color:#c00;
}

body{
    font-family: MySerif;
}

.title{
    font-family: MySansMedium;
}

.subtitle {
    font-family: MySerifBold;
}

.tail_number {
    font-family: MySerifItalic;
}

"""


css1 = {TC().enlang: _css1,
        SC().enlang: _css1.replace("CJK TC", "CJK SC")}

css1_path = "_css/css1.css"


css2 = {TC().enlang: _css2,
        SC().enlang: _css2.replace("CJK TC", "CJK SC")}

css2_path = "_css/css2.css"
