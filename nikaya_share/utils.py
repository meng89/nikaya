from typing import NewType




import re
import copy
from datetime import datetime

import xl


Line = list[str | xl.Element]
Lines = list[Line]


def get_last_folder(data: dict):
    last_folder = None
    for _, v in data.items():
        if isinstance(v, dict):
            last_folder = v

    if last_folder is None:
        return data
    else:
        return get_last_folder(last_folder)


class AnalysisFailed(Exception):
    pass


def get_name(root, pattern):
    names = []
    for span in root.find_descendants("span"):
        if len(span.kids) > 0 and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            m = re.match(pattern, kid)
            if m:
                names.append(m)
    if len(names) != 1:
        open("get_name_debug.xml", "w").write(root.to_str())
        debug_print_es(root.find_descendants("span"))
        raise AnalysisFailed(names)
    return names[0]


def get_name2(root):
    names = []
    for span in root.find_descendants("span"):
        if len(span.kids) > 0 and span.attrs.get("style") == "font-size: 18pt" and isinstance(span.kids[0], str):
            kid = span.kids[0].strip()
            names.append(kid)
    if len(names) != 1:
        open("get_name_debug.xml", "w").write(root.to_str())
        debug_print_es(root.find_descendants("span"))
        raise AnalysisFailed(names)
    return names[0]


def debug_print_es(l):
    s = ""
    for x in l:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += x.to_str()
        else:
            raise Exception
    print(s)

                            # SN.1.1   1     1
def make_xml(source_page, sutta_nums, start, end, mtime, ctime, source_title, relevant, title_line, head, body, notes) -> xl.Xml:
    doc = xl.Element("doc")
    meta = doc.ekid("meta")

    source_page_e = meta.ekid("source_page")
    source_page_e.kids.append(source_page)

    sutta_nums_e = meta.ekid("sutta_nums")
    for type_, v in sutta_nums:
        e = sutta_nums_e.ekid("sutta_num")
        if type_ is not None:
            e.attrs["type"] = type_
        e.kids.append(v)


    start_e = meta.ekid("start")
    if start is not None:
        start_e.kids.append(start)

    end_e = meta.ekid("end")
    if end is not None:
        end_e.kids.append(end)

    source_title_e = meta.ekid("source_title")
    if source_title is not None:
        source_title_e.kids.extend(source_title)

    relevant_e = meta.ekid("relevant")
    if relevant is not None:
        relevant_e.kids.append(relevant)

    name_e = meta.ekid("title")
    if not isinstance(title_line, list):
        input(repr(title_line))
    name_e.kids.extend(title_line)

    mtime_e = meta.ekid("mtime")
    mtime_str = datetime.fromtimestamp(mtime).astimezone().strftime('%Y-%m-%d %H:%M:%S %z')
    mtime_e.kids.append(mtime_str)

    ctime_e = meta.ekid("ctime")
    if ctime:
        ctime_e.kids.append(ctime)

    if head:
        doc.kids.append(head)
    else:
        doc.ekid("head")
    doc.kids.append(body)
    doc.kids.append(notes)
    xml = xl.Xml(root=doc)
    return xml

WRITE_DONT_DO_TAGS = ["source_page", "sutta_num", "start", "end", "name", "mtime", "ctime", "relevant", "p", "note", "title", "source_title"]


def get_pin_name(body_lines):
    pin_list = []
    for line in body_lines:
        if len(line) == 1 and isinstance(line[0], str):
            kid = line[0].strip()
            if kid.endswith("品"):
                m = re.match(r"^(\d+\.)?(\S+)$", kid)
                pin_list.append(m.group(2))

    if pin_list:
        return pin_list[0]
    else:
        return None


def get_pin_name2(body_lines):
    pin_list = []
    for line in body_lines:
        if len(line) == 1 and isinstance(line[0], str):
            kid = line[0].strip()
            if kid.endswith("品"):
                m = re.match(r"^(\d+\.\S+)$", kid)
                pin_list.append(m.group(1))


    if len(pin_list) > 1:
        raise AnalysisFailed(pin_list)

    if pin_list:
        return pin_list[0]
    else:
        return None


Match = tuple[re.Match, int, Line]
Matchs = list[Match]

def match_line(lines: Lines, partterns: list[re.Pattern]) -> Matchs:
    matched_lines = []
    for index, line in enumerate(lines):
        txt = line_to_txt(line).strip()
        for parttern in partterns:
            m = re.match(parttern, txt)
            if m:
                matched_lines.append((m, index, line))
                break

    return matched_lines


def line_to_txt(line: Line):
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, xl.Element):
            s += line_to_txt(x.kids)
        else:
            raise Exception(x)

    return s


Suttas = list[tuple[Line, Lines, Lines]]
def split_sutta(body_lines, matches: Matchs) -> Suttas:
    sutta_lines_ = copy.deepcopy(matches)
    suttas = [] #[title_line, head_lines, ji_body_lines]

    _m, title_index, _title_line = sutta_lines_.pop(0)
    last_head_lines = body_lines[0: title_index]
    last_title_line = body_lines[title_index]

    last_title_index = title_index


    for _m, title_index, _title_line in sutta_lines_:
        title_line = body_lines[title_index]

        last_body_lines = body_lines[last_title_index +1: title_index]

        suttas.append(
            (last_title_line, last_head_lines, last_body_lines)
        )
        last_title_index = title_index

        last_head_lines = []
        last_title_line = title_line

    last_body_lines = body_lines[last_title_index +1:]
    suttas.append(
        (last_title_line, last_head_lines, last_body_lines)
    )

    return suttas


def strip_crlf(line: Line) -> Line:
    newline = copy.deepcopy(line)
    if isinstance(newline[0], str):
        newline[0] = newline[0].lstrip()
    if isinstance(newline[-1], str):
        newline[-1] = newline[-1].rstrip()
    return newline


def split_serial_title(line: Line) -> tuple[str, Line]:
    new_line = copy.deepcopy(line)
    new_line = strip_line(new_line)
    if isinstance(new_line[0], str):
        m = re.match(r"([\d-]+)\.(.*)$", new_line[0])
        if m:
            if m.group(2):
                new_line[0] = m.group(2)
            else:
                new_line.pop(0)

            return m.group(1), new_line

    raise Exception(new_line)


# xml need 1: toc title 没有其它经的引用，没有经号。
# 2: html 页面的 title，保留原有，包含其它经文的引用，包含注解。没有经号。
# 所以应该有一个


def split_title_txt(line: Line) -> tuple[str, str, str]:
    txt = line_to_txt(line)
    txt.strip()
    m = re.match(r"^([^一-龥]*)(.*?)([^一-龥]*)$", txt)
    return m.group(1), m.group(2), m.group(3)



def get_page_title(line: Line) -> Line:
    pass



def strip_line(line: Line):
    new_line = copy.deepcopy(line)
    if isinstance(new_line[0], str):
        new_line[0] = new_line[0].lstrip()
    if isinstance(new_line[-1], str):
        new_line[-1] = new_line[-1].rstrip()
    return new_line
