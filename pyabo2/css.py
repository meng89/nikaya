from pyabo.book_public import TC, SC


_css1 = """
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


h1, h2, h3, h4, h5, h6, h7, .sutta_title {
    font-family: "Noto Sans CJK TC";
    font-weight: 600;
    color: inherit;
}
.sutta_nums {
/*
    font-family: "Noto Serif";
    font-size: 0.8em;
*/
}
.sutta_num_sc, .sutta_num_abo {
    color: inherit;
    text-decoration: none;
}
.sutta_name {
    color: inherit;
    text-decoration: none;
}


a.noteref {
    color: inherit;
    text-decoration-style: dotted;
    text-underline-offset: 0.2rem;
}

body.note ol {
    list-style: none;
}

a.suttaref_inbook {
    color: inherit;
}


body.cover {
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center;     /* 垂直居中 */
    height: 100vh;           /* 确保body高度填满整个视口 */
    margin: 0;               /* 移除默认margin */
}
body.cover   img {
    max-width: 100%;         /* 图片最大不超过父容器宽度 */
    max-height: 100%;        /* 图片最大不超过父容器高度 */
}


body.homage {
    display: flex; /* 将body设置为弹性容器 */
    align-items: center; /* 使子元素在垂直方向上居中 */
    min-height: 100vh; /* 让body占据整个视口高度，确保垂直居中有效 */
    justify-content: center; /* 水平居中 */
}


"""

css1 = {
    TC().enlang: _css1,
    SC().enlang: _css1.replace("CJK TC", "CJK SC")
}

css1_path = "_css/css1.css"
