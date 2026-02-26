import re
import os
import string
import subprocess
import shutil
from datetime import datetime

import xl

import config
from . import epub, ebook_utils
import nikaya_share
from nikaya_share import new_page_or_not
import abo.ebook_utils


MAIN = "main.tex"
SUTTAS = "suttas.tex"

layouts = {
    "normal": {
        "cover_size": (2126, 2835),
        "max_hanzi_in_line": 35,
        "max_line_in_page": 29,
    },

    "A4": {
        "cover_size": (2480, 3508),
        "max_hanzi_in_line": 40,
        "max_line_in_page": 43,
    },

    "xperia10v": {
        "cover_size": (1080, 2520),
        "max_hanzi_in_line": 29,
        "max_line_in_page": 15,
    },

    "ipad9th": {
        "cover_size": (1620, 2160),
        "max_hanzi_in_line": 29,
        "max_line_in_page": 15,
    },

    "kobo_forma": {
        "cover_size": (1440, 1920),
        "max_hanzi_in_line": 27,
        "max_line_in_page": 25,

    },
}

fonts = {
    "song": "rm",
    "kai": "cg",
    "hei": "ss"
}

"""
\\setuphead[part][style=\\tfd\\bf\\ss]
\\setuphead[title][style=\\tfc\\bf\\ss]
\\setuphead[subject][style=\\tfb\\bf\\ss]
\\setuphead[subsubject][style=\\tfa\\bf\\ss]
\\setuphead[subsubsubject][style=\\tf\\bf\\ss]
\\setuphead[subsubsubsubject][style=\\tfx\\bf\\ss]
\\setuphead[subsubsubsubsubject][style=\\tfxx\\bf\\ss]
\\setuphead[subsubsubsubsubsubject][style=\\tfxx\\bf\\ss]
\\setuphead[subsubsubsubsubsubsubject][style=\\tfxx\\bf\\ss]
"""





class TexHead:
    heads = ["part", "title", "subject", "subsubject", "subsubsubject", "subsubsubsubject", "subsubsubsubsubject", "subsubsubsubsubsubject", "subsubsubsubsubsubsubject"]
    font_sizes = ["tfd", "tfc", "tfb", "tfa", "tf", "tfx", "tfxx", "tfxx", "tfxx"]
    def __init__(self, catalog_depth):
        self.catalog_depth = catalog_depth

    def _get_size(self, i):
        try:
            return "\\" + TexHead.font_sizes[i - self.catalog_depth]
        except IndexError:
            return "\\" + TexHead.font_sizes[0]

    def setuphead(self):
        s = ""
        for count, head in enumerate(TexHead.heads):
            s += "\\setuphead[" + head + "][style=" + self._get_size(count) + "\\bf\\ss]\n"
        return s

    def startsec(self, depth, title, bookmark, toctext, lang, sc_key=None, abo_key=None):
        sec = TexHead.heads[depth]
        font_size = self._get_size(depth)
        s = ""
        s += "\\startalignment[center]\n"
        s += "{\\darkred\n"
        s += "\\setuphead[" + sec + "][before={\\testpage[4]\\blank[1*halfline]"

        if sc_key:
            s += "\\goto{" + font_size + " \\ss \\bf " + sc_key + "}[url(https://suttacentral.net/" + sc_key + ")]\\kern 0.5em"
        else:
            s += "\\strut"  # 若不添加，上面的居中命令就无效了，我也不知道为什么

        s += "}]\n"

        s += "\\start" + sec + "[\n"
        s += "    title={{{}}},\n".format(title or "")
        s += "    bookmark={{{}}},\n".format(bookmark)
        s += "    list={" + (sc_key + " " if sc_key is not None else "") + toctext + "},]\n"

        if abo_key:
            s += "\\goto{(莊春江" + lang.c("譯") + ")}[url(https://suttacentral.net/" + abo_key + ")]\n"

        s += "}\n"

        s += "\\stopalignment\n"

        s += "\\blank[1*halfline]\n\n"

        return s

    @staticmethod
    def stop(depth):
        return "\\stop{}\n\n".format(TexHead.heads[depth])

def writetolist(f, ngs):
    s = ""
    for index, (_, _, name) in enumerate(ngs):
        s = "\\writetolist[" + TexHead.heads[index] + "]{}{" + name + "}\n"
    f.write(s)


def build_epub_one_book(type_, cover_dir, full_path, data_infos, lang, layout, font, tag):
    data3, translators = epub.make_tree_data(type_, data_infos, lang)
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    shutil.copytree(config.TEX_DIR, work_dir)

    os.makedirs(out_dir, exist_ok=True)

    w, h = layouts[layout]["cover_size"]
    if type_ is nikaya_share.HYNCDZJ:
        _write_hyncdzj_homage(work_dir, lang)
        _write_readme(epub.README_HYNCDZJ, work_dir, lang)
        book_info = nikaya_share.Info(name="漢譯南傳大藏經", pali="Tipiṭaka", translators=tuple(translators))
        cover_image_path = ebook_utils.make_cover_image(cover_dir, book_info, lang, tag, w, h, onebook=True)
        write_main_tex(work_dir, book_info, lang, layout, font, "hyncdzj_homage.tex", cover_image_path)
    else:
        _write_abo_homage(work_dir, lang)
        _write_readme(epub.README_ABO, work_dir, lang)
        book_info = nikaya_share.Info(name="漢譯藏經", pali="Sutta Piṭaka", translators=tuple(translators))
        cover_image_path =  abo.ebook_utils.make_cover_image(cover_dir, book_info, lang, w, h, onebook=True)
        write_main_tex(work_dir, book_info, lang, layout, font, "abo_homage.tex", cover_image_path)
    write_fontstex(work_dir, lang)

    f = open(os.path.join(work_dir, SUTTAS), "w")
    for prev_ngs, info, data in data3:
        ds_depth = new_page_or_not.get_data_depth(data)
        nh_ngs = prev_ngs + [(None, None, lang.c(info.name))]
        writetolist(f, nh_ngs)
        root_depth = len(nh_ngs) -1
        texhead = TexHead(root_depth)
        write_tree2(type_, info, texhead, ds_depth, f, [], data, 0, lang, False, layouts[layout]["max_hanzi_in_line"], layouts[layout]["max_line_in_page"])

    complie_pdf(work_dir, out_dir, layout, full_path)


def build_pdf(type_, cover_dir, full_path, data, info, lang, layout, font, tag):
    work_dir = full_path + "_work"
    out_dir = full_path + "_out"
    shutil.copytree(config.TEX_DIR, work_dir)

    os.makedirs(out_dir, exist_ok=True)

    w, h = layouts[layout]["cover_size"]
    if type_ is nikaya_share.HYNCDZJ:
        _write_hyncdzj_homage(work_dir, lang)
        _write_readme(epub.README_HYNCDZJ, work_dir, lang)
        cover_image_path = ebook_utils.make_cover_image(cover_dir, info, lang, tag, w, h, onebook=True)
        write_main_tex(work_dir, info, lang, layout, font, "hyncdzj_homage.tex", cover_image_path)
    else:
        _write_abo_homage(work_dir, lang)
        _write_readme(epub.README_ABO, work_dir, lang)
        cover_image_path =  abo.ebook_utils.make_cover_image(cover_dir, info, lang, w, h, onebook=True)
        write_main_tex(work_dir, info, lang, layout, font, "abo_homage.tex", cover_image_path)
    write_fontstex(work_dir, lang)

    texhead = TexHead(0)
    ds_depth = new_page_or_not.get_data_depth(data)
    f = open(os.path.join(work_dir, SUTTAS), "w")
    f.write(texhead.setuphead())
    #for _, obj in data:
    #    write_tree(-1, data, f, info, obj, lang, layouts[layout]["max_hanzi_in_line"], layouts[layout]["max_line_in_page"])
    write_tree2(type_, info, texhead, ds_depth, f, [], data, 0, lang, False, layouts[layout]["max_hanzi_in_line"], layouts[layout]["max_line_in_page"])
    f.close()

    complie_pdf(work_dir, out_dir, layout, full_path)


def complie_pdf(work_dir, out_dir, layout, full_path):
    my_env = os.environ.copy()
    if os.name == "posix":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ":" + my_env["PATH"]
    elif os.name == "nt":
        my_env["PATH"] = os.path.expanduser(config.CONTEXT_BIN_PATH) + ";" + my_env["PATH"]
    mode_list = [layout]
    if config.DEBUG:
        mode_list.append("debug")
    modes = ",".join(mode_list)
    compile_cmd = """context --path="{}" "{}"/"{}" --mode={}""".format(work_dir, work_dir, MAIN, modes)

    stdout_file = open(os.path.join(out_dir, "cmd_stdout"), "w", encoding="utf-8")
    stderr_file = open(os.path.join(out_dir, "cmd_stderr"), "w", encoding="utf-8")

    def _run():
        #print("运行:", compile_cmd, end=" ", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=out_dir, shell=True, env=my_env,
                             stdout=stdout_file, stderr=stderr_file)
        p.communicate()

        if p.returncode != 0:
            pass
            #input("出错")
        else:
            #print("完成")
            shutil.copy(os.path.join(out_dir, "main.pdf"), full_path)
            if not config.DEBUG:
                shutil.rmtree(work_dir)
                shutil.rmtree(out_dir)
        return p.returncode

    _run()
    print("here")

    stdout_file.close()
    stderr_file.close()


def write_tree2(type_, info, texhead, ds_depth, f, ngs, obj, depth, lang, parent_merge_or_not, max_hanzi_in_line, max_line_in_page):
    if parent_merge_or_not:
        merge_or_not = True
    else:
        if len(ngs) == 0:
            merge_or_not = False
        else:
            merge_or_not = new_page_or_not.merge_or_not(ngs, obj, ds_depth)

    for ng, sub in obj:
        sub_ngs = ngs + [ng]
        _, _, _, mark_name, title_range, title_name = epub.make_mark_and_heading(info, sub_ngs, sub, 1)
        start_str = texhead.startsec(depth, title_name, mark_name, title_name, lang, title_range)
        f.write(start_str)

        if isinstance(sub, xl.Element):
            write_doc(f, sub, lang)
        else:
            assert isinstance(sub, list)
            write_tree2(type_, info, texhead, ds_depth, f, sub_ngs, sub, depth + 1, lang, merge_or_not, max_hanzi_in_line, max_line_in_page)

        f.write(texhead.stop(depth))

    if not merge_or_not:
        f.write("\\page[yes]\n")



def write_tree(level_offset, book_data, f, info, obj, lang, max_hanzi_in_line, max_line_in_page):

    new_page = new_page_or_not.new_page_or_not_smart(book_data, obj, max_hanzi_in_line, max_line_in_page)

    namegroups = new_page_or_not.get_keys(book_data, obj, [])
    #print("hh:",namegroups, new_page)

    depth = len(namegroups)
    if depth > 9:
        print("depth too long", namegroups)
        exit()

    _, _, _, mark_name, title_range, title_name = epub.make_mark_and_heading(info, namegroups, obj, 1)

    if title_range is not None:
        sc_key = title_range
        # title = "\\goto{{{}}}[url(https://suttacentral.net/{})]".format(title_range, title_range) + " " + title_name
    else:
        sc_key = None
        # title = title_name

    f.write(startsec(lang, depth, title_name, mark_name, title_name, sc_key))

    if isinstance(obj, xl.Element):
        write_doc(f, obj, lang)
    else:
        assert isinstance(obj, list)
        for _, sub in obj:
            write_tree(level_offset, book_data, f, info, sub, lang, max_hanzi_in_line, max_line_in_page)

    f.write(stopsec(depth))
    if new_page:
        f.write("\\page[yes]\n")


def write_doc(f, doc, lang):
    for e in doc.kids:
        if isinstance(e, xl.Element) and re.match(r"^n\d+$", e.tag):
            break

        elif isinstance(e, xl.Element) and e.tag == "sub":
            #todo
            pass

        elif isinstance(e, xl.Element) and e.tag.startswith("sub"):
            #todo
            pass

        else:
            f.write(xml_to_tex([e], doc, lang))


def write_fontstex(work_dir, lang):
    type_name = "type-imp-myfonts-" + lang.en + ".tex"

    f = open(os.path.join(work_dir, type_name), "r+", encoding="utf-8")
    fonttex = f.read()

    replace_map = {}
    for fontname in re.findall("file:(.*(?:ttf|otf|ttc))", fonttex):
        realfontpath = findfile(config.FONTS_DIRS, os.path.basename(fontname))
        if os.name == "nt":
            realfontpath = ntrelpath(realfontpath, work_dir)
        replace_map[fontname] = realfontpath

    for fontname, realfontpath in replace_map.items():
        fonttex = fonttex.replace(fontname, realfontpath.replace("\\", "/"))

    f.seek(0)
    f.truncate()
    f.write(fonttex)
    f.close()

def findfile(font_dirs, name):
    for font_dir in font_dirs:
        for relpath, dirs, files in os.walk(font_dir):
            if name in files:
                full_path = os.path.join(font_dir, relpath, name)
                return os.path.normpath(os.path.abspath(full_path))
    raise FileNotFoundError(name)

def ntrelpath(path1, path2):
    import ntpath
    try:
        path = ntpath.relpath(path1, ntpath.dirname(path2))
    except ValueError:
        path = path1
    return path


def write_main_tex(work_dir, info, lang, layout, font, homage, cover_image):
    f = open(os.path.join(work_dir, MAIN), "r+", encoding='utf-8')
    main_t = f.read()

    date = datetime.today().strftime('%Y-%m-%d')
    main = string.Template(main_t).substitute(
        font_type="type-imp-myfonts-sc" if isinstance(lang, ebook_utils.SC) else "type-imp-myfonts-tc",
        layout=layout+".tex",
        font=fonts[font],
        title=info.name,
        author="、".join(info.translators) + lang.c("譯"),
        keyword=lang.c("上座部佛教、南傳佛教、") + info.name,
        date=date,
        mulu=lang.c("目錄"),
        homage=homage,
        cover_image=cover_image,
    )
    f.seek(0)
    f.truncate()
    f.write(main)
    f.close()


def _write_hyncdzj_homage(work_dir, lang):
    f = open(os.path.join(work_dir, "hyncdzj_homage.tex"), "r+", encoding="utf-8")
    homage_t = f.read()
    homeage = string.Template(homage_t).substitute(
        title = lang.c("禮敬偈"),
        line1 = lang.c("歸命彼世尊"),
        line2 = lang.c("應供等覺者")
    )
    f.seek(0)
    f.truncate()
    f.write(homeage)
    f.close()

def _write_abo_homage(work_dir, lang):
    f = open(os.path.join(work_dir, "abo_homage.tex"), "r+", encoding="utf-8")
    homage_t = f.read()
    homeage = string.Template(homage_t).substitute(
        title = lang.c("禮敬世尊"),
        line = lang.c("對那位世尊、阿羅漢、遍正覺者禮敬"),
    )
    f.seek(0)
    f.truncate()
    f.write(homeage)
    f.close()


def _write_readme(readme, work_dir, lang):
    f = open(os.path.join(work_dir, "readme.tex"), "w", encoding="utf-8")
    f.write(startsec(lang, 1, "说明", "说明", "说明"))
    for line in readme:
        f.write(xml_to_tex(line, None, nikaya_share.Lang()))
        f.write("\n\\blank\n")

    if config.DEBUG:
        f.write("\\page[yes]\n")
        lines = [
            "Pāḷi: Sammā-diṭṭhi, Sammā-saṅkappa, Sammā-vācā, Sammā-kammanta, Sammā-ājīva, Sammā-vāyāma, Sammā-sati, Sammā-samādhi",
            "EN: right view, right resolve, right speech, right conduct, right livelihood, right effort, right mindfulness, and right samadhi",
            "SC: 正见、正思维、正语、正业、正命、正精进、正念、正定",
            "TC: 正見、正思維、正語、正業、正命、正精進、正念、正定",
        ]
        for font in "rm", "ss", "cg":
            for style in "", "it", "bf":
                f.write("{")

                f.write("\\" + font + " ")
                if style:
                    f.write("\\" + style + " ")
                f.write(font + " " + style + " :\\par\n")

                for line in lines:
                    f.write(line)
                    f.write("\\par\n")
                f.write("}")
                f.write("\n\\blank\n")

    f.write("\\page\n")
    f.write(stopsec(1))


_map = {
    1: ("part", "\\tfd " ),
    2: ("title", "\\tfc "),
    3: ("subject", "\\tfb " ),
    4: ("subsubject", "\\tfa "),
    5: ("subsubsubject", "\\tf "),
    6: ("subsubsubsubject", "\\tfx "),
    7: ("subsubsubsubsubject", "\\tfxx "),
    8: ("subsubsubsubsubsubject", "\\tfxx "),
    9: ("subsubsubsubsubsubsubject", "\\tfxx "),
    10: ("subsubsubsubsubsubsubsubject", "\\tfxx "),
    11: ("subsubsubsubsubsubsubsubject", "\\tfxx "),
}

def startsec(lang, depth, title, bookmark, toctext, sc_key=None, abo_key=None):
    # Ugly hack to Title

    sec = _map[depth][0]
    font_size = _map[depth][1]
    s = ""
    s += "\\startalignment[center]\n"
    s += "{\\darkred\n"
    s += "\\setuphead[" + sec + "][before={\\testpage[4]\\blank[1*halfline]"

    if sc_key:
        s += "\\goto{" + font_size + "\\ss \\bf " + sc_key + "}[url(https://suttacentral.net/"+ sc_key + ")]\\kern 0.5em"
    else:
        s += "\\strut" # 若不添加，上面的居中命令就无效了，我也不知道为什么

    s += "}]\n"

    s += "\\start" + sec + "[\n"
    s += "    title={{{}}},\n".format(title or "")
    s += "    bookmark={{{}}},\n".format(bookmark)
    s += "    list={" + (sc_key + " " if sc_key is not None else "") + toctext + "},]\n"

    if abo_key:
        s += "\\goto{(莊春江" + lang.c("譯") + ")}[url(https://suttacentral.net/" + abo_key + ")]\n"

    s += "}\n"

    s += "\\stopalignment\n"

    s += "\\blank[1*halfline]\n\n"

    return s

def stopsec(depth):
    #return ""
    return "\\stop{}\n\n".format(_map[depth][0])


def xml_to_tex(es, doc, lang):
    s = ""
    for e in es:
        if isinstance(e, str):
            _s = e
            _s = _s.replace("{", "\\{").replace("}", "\\}").replace("[", "\\[").replace("]", "\\]").replace("#", "\\#")
            s += _s

        elif isinstance(e, xl.Element):
            m_t = re.match(r"^t(\d+)$", e.tag)
            m_n = re.match(r"^n\d+$", e.tag)
            if m_t:
                if e.kids:
                    assert (len(e.kids) == 1 and isinstance(e.kids[0], str))
                    text = e.kids[0]
                    s += text
                n_kids = epub.get_note_by_key(doc, m_t.group(1))
                _note = es_to_text(n_kids)

                s += "\\zhfootnote{" + _note + "}"
                #s += "\\high{{\\tfxx \\PDFhighlight[原始注解][{{{}}}]{{{}}}}}".format(_note, text or "㊟")
                #s += "\\high{\\tfxx \\PDFhighlight[原始注解][{" + _note + "}]{" + (text or "㊟") + "}}"

            elif m_t and False:
                text = None
                if e.kids:
                    assert (len(e.kids) == 1 and isinstance(e.kids[0], str))
                    text = e.kids[0]
                n_kids = epub.get_note_by_key(doc, m_t.group(1))
                _note = es_to_text(n_kids)
                #s += "\\high{{\\tfxx \\PDFhighlight[原始注解][{{{}}}]{{{}}}}}".format(_note, text or "㊟")
                s += "\\high{\\tfxx \\PDFhighlight[原始注解][{" + _note + "}]{" + (text or "㊟") + "}}"

            elif e.tag == "p":
                s += xml_to_tex(e.kids, doc, lang)
                s += "\n\n"

            elif e.tag == "j":
                s += "\\startalignment[middle]\n"
                s += "\\startlines\n"
                for index, p in enumerate(e.kids):
                    s += "\\strut "
                    kids, delete_head, delete_tail = xxx(p.kids)
                    lltp_str = ""
                    if index == 0:
                        if "a" in e.attrs.keys():
                            lltp_str = e.attrs["a"]
                        else:
                            lltp_str = ""

                    if delete_head:
                        lltp_str += "「"

                    if lltp_str:
                        s += "\\dontleavehmode\\llap{{{}}}".format(lltp_str)
                    s += xml_to_tex(kids, doc, lang)
                    if delete_tail:
                        s += "\\rlap{{{}}}".format("」")
                    s += "\n"
                s += "\\stoplines\n"
                s += "\\stopalignment\n"

            elif m_n:
                pass

            elif e.tag == "a":
                s += "\\goto{" + xml_to_tex(e.kids, doc, lang) + "}[url(" + e.attrs["href"] + ")]"

            elif e.tag == "list":
                s += "\\startalignment[middle]\n"
                s += "\\startlines\n"
                for item in e.kids:
                    s += xml_to_tex(item.kids, doc, lang)
                    s += "\n\n"
                s += "\\stoplines\n"
                s += "\\stopalignment\n"

            else:
                raise Exception("Unknown element type: {}".format(repr(e.to_str())))
        else:
            raise Exception("Unknown element type: {}".format(repr(e.to_str())))

    return s


def es_to_text(es):
    s = ""
    for x in es:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += es_to_text(x.kids)
        else:
            raise Exception(x)
    return s


def xxx(p_kids):
    kids = []
    delete_head = False
    for index, e in enumerate(p_kids):
        if index == 0 and isinstance(e, str) and e[0] == "「":
            delete_head = True
            kids.append(e[1:])
        else:
            kids.append(e)

    if isinstance(kids[-1], str) and kids[-1][-1] == "」":
        kids[-1] = kids[-1][:-1]
        delete_tail = True
    else:
        delete_tail = False

    return  kids, delete_head, delete_tail
