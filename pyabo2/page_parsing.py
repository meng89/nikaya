import os.path
import re
import bs4
import xl


try:
    import user_config as config
except ImportError:
    import config as config


def read_page(file_path, style=1):
    read_page_fun = _read_page1
    if style == 2:
        read_page_fun = _read_page2


    print("read_page:", file_path)
    full_path = os.path.join(config.DOWNLOAD_DIR, file_path)
    mtime = os.path.getmtime(full_path)
    data = open(full_path, "r").read()

    # todo report bug
    if file_path in ("AN/AN0437.htm", "AN/AN0993.htm"):
        data = data.replace("<aonMouseover", "<a onMouseover")

    soup = bs4.BeautifulSoup(data, 'html5lib')
    root = xl.parse(str(soup)).root

    result = [root, mtime] + read_page_fun(root)
    return result



def _read_page2(root):
    divs = root.find_descendants("div")
    div_nikaya = None
    div_pali = None
    div_comp = None

    for div in divs:
        if "class" in div.attrs.keys():
            if div.attrs["class"] == "nikaya":
                div_nikaya = div
            elif div.attrs["class"] == "pali":
                div_pali = div
            elif div.attrs["class"] == "comp":
                div_comp = div

    notes = take_comp(div_comp)
    body_lines =  kids_to_lines(div_nikaya.kids)
    return [body_lines, notes, div_nikaya]


def _read_page1(root):
    divs = root.find_descendants("div")
    div_nikaya = None
    div_pali = None
    div_comp = None

    for div in divs:
        if "class" in div.attrs.keys():
            if div.attrs["class"] == "nikaya":
                div_nikaya = div
            elif div.attrs["class"] == "pali":
                div_pali = div
            elif div.attrs["class"] == "comp":
                div_comp = div

    notes = take_comp(div_comp)

    homage_and_head_lines, sutta_name_part, translator_part, agama_part, body_lines = take_nikaya(div_nikaya)

    homage_line, _head_lines = _split_homage_and_head(homage_and_head_lines)
    head_lines = _head_lines

    body = lines_to_body(body_lines)
    return [homage_line, head_lines, sutta_name_part, translator_part, agama_part, body, notes, div_pali]


def take_comp(div_comp: xl.Element):
    notes = xl.Element("notes")
    for span in div_comp.find_descendants("span"):
        id_ = span.attrs.get("id")
        if id_ is not None:
            m = re.match(r"^note(\d+)$", id_)
            if m:
                note = xl.Element("note")
                note.attrs["id"] = m.group(1)
                note.kids.extend(span.kids)
                notes.kids.append(note)

    return notes


def kids_to_lines(kids: list) -> list:
    lines = []
    line = []
    for e in kids:
        if isinstance(e, xl.Element) and e.tag == "br":
            lines.append(line)
            line = []
        elif isinstance(e, xl.Comment):
            pass
        elif isinstance(e, str):
            if e.strip("\n") != "":
                line.append(e)
            else:
                pass
        elif isinstance(e, (str, xl.Element)):
            line.append(e)
        else:
            raise Exception((type(e), repr(e)))
            # line.append(e)
    if line:
        lines.append(line)

    return lines


def take_nikaya(div_nikaya):
    contents = div_nikaya.kids
    homage_and_head_oline = []
    homage_and_head_olines = []

    sutta_name_es = None
    body_lines = []

    while contents:
        e = contents.pop(0)
        if isinstance(e, xl.Element) and e.tag == "span" and e.attrs["class"] == "sutra_name":
            sutta_name_es = e.kids
            break
        elif isinstance(e, xl.Element) and e.tag == "br":
            homage_and_head_olines.append(homage_and_head_oline)
            homage_and_head_oline = []
        else:
            homage_and_head_oline.append(e)
    if homage_and_head_oline:
        homage_and_head_olines.append(homage_and_head_oline)

    homage_and_head_lines = htm_lines_to_xml_lines(homage_and_head_olines)
    # homage_and_head_lines = homage_and_head_olines

    e2 = contents.pop(0)
    assert isinstance(e2, str)
    translator_line = e2.strip()
    m = re.match(r"^(.+\(莊春江譯\))(.+)$", translator_line)
    if m:
        translator_part = m.group(1)
        agama_part = m.group(2)
    else:
        translator_part = translator_line
        agama_part = None
    # todo what?
    _br = contents.pop(0)
    assert (isinstance(_br, xl.Element) and _br.tag == "br")

    _new_contents = []
    for e in contents:
        if isinstance(e, xl.Element) and e.tag == "div" and e.attrs["style"] == "display: none":
            continue
        elif isinstance(e, xl.Element) and e.tag == "span" and e.attrs["class"] == "sutra_name" and e.kids[0] == "相應部12相應83-93經/學經等（中略）十一則":
            _new_contents.append(e.kids[0])
        else:
            _new_contents.append(e)

    contents = _new_contents

    for oline in kids_to_lines(contents):
        body_lines.append(htm_line_to_xml_line(oline))

    return homage_and_head_lines, sutta_name_es, translator_part, agama_part, body_lines


def _split_homage_and_head(lines):
    homage_line = None
    head_lines = []
    for line in lines:
        if line[0].startswith("對那位") and line[-1].endswith("禮敬"):
            homage_line = line
        else:
            head_lines.append(line)
    return homage_line, head_lines


def htm_lines_to_xml_lines(htm_lines: list):
    xml_lines = []
    for htm_line in htm_lines:
        xml_line = htm_line_to_xml_line(htm_line)
        xml_lines.append(xml_line)
    return xml_lines

def htm_line_to_xml_line(htm_line, funs=None):
    line = []
    for oe in htm_line:
        try:
            line.extend(_do_e(oe, funs or [do_str, do_global_note, do_local_note, do_a, do_styled_span, do_sutra_name_span]))
        except TypeError:
            raise Exception((type(oe), oe))
    return line


def print_line(line):
    l = ""
    for x in line:
        if isinstance(x, str):
            l += x
        elif isinstance(x, xl.Element):
            l += x.to_str()
    print("print_line:", l)


def _do_e(e, funs):
    for fun in funs:
        answer, x = fun(e=e)
        if answer:
            return x

    if isinstance(e, xl.Element):
        print(e.to_str())
    raise Exception((type(e), e))


def do_str(e):
    if isinstance(e, str):
        return True, [e.strip("\n")]
    else:
        return False, e


def do_global_note(e):
    if isinstance(e, xl.Element) and e.tag == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^note\(this,(\d+)\);$", e.attrs["onmouseover"])
        if m:
            twgn = xl.Element("gn") # text with global note
            twgn.attrs["id"] = m.group(1)
            twgn.kids.extend(e.kids)
            return True, [twgn]

    return False, e


def do_local_note(e):
    if isinstance(e, xl.Element) and e.tag == "a" and "onmouseover" in e.attrs.keys():
        m = re.match(r"^local\(this,(\d+)\);$", e.attrs["onmouseover"])
        if m:
            twln = xl.Element("ln") # text with local note
            twln.attrs["id"] = m.group(1)
            twln.kids.extend(e.kids)
            return True, [twln]

    return False, e


def do_a(e):
    if isinstance(e, xl.Element) and e.tag == "a":
        new_kids = htm_line_to_xml_line(e.kids)
        #e.kids.clear()
        e.kids = new_kids
        return True, [e]
    else:
        return False, e


def do_styled_span(e):
    if isinstance(e, xl.Element) and e.tag == "span" and e.attrs.get("style") == "color: #800000":
        new_kids = htm_line_to_xml_line(e.kids, [do_str, do_global_note, do_local_note, do_a, do_styled_span, do_br])
        e.kids = new_kids
        return True, [e]
    else:
        return False, e


def do_sutra_name_span(e):
    if isinstance(e, xl.Element) and e.tag == "span" and e.attrs.get("class") == "sutra_name":
        return True, [e]
    else:
        return False, e


def do_br(e):
    if isinstance(e, xl.Element) and e.tag == "br":
        return True, [e]
    else:
        return False, e


class NoteNotMatch(Exception):
    pass


class NoteNotFound(Exception):
    pass


def lines_to_body(lines):
    body = xl.Element("body")
    for line in lines:
        p = body.ekid("p")
        assert isinstance(line, list)
        p.kids.extend(line)
    return body


def lines_to_head(lines):
    head = xl.Element("head")
    for line in lines:
        p = head.ekid("p")
        assert isinstance(line, list)
        p.kids.extend(line)
    return head