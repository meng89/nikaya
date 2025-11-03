#!/usr/bin/env python3
import os
import tempfile
import subprocess
import uuid
import datetime
import re
import opencc

import config

import epubpacker

from hyncdzj import base

import xl
import load_from_p5a

import book_module

def trans_sc(s: str) -> str:
    c = opencc.OpenCC("t2s.json")
    return c.convert(s)


def load_book_from_dir(m):
    book = load_from_p5a.load_book_by_module(m)
    return book


def cover_to_sc(src, dst):
    for file in os.listdir(src):
        path = os.path.join(src, file)
        dst_path = os.path.join(dst, trans_sc(file))

        if os.path.isfile(path) and file.lower().endswith(".xml"):
            f = open(path, "r")
            xml_str = f.read()
            f.close()
            f = open(dst_path, "w")
            f.write(trans_sc(xml_str))
            f.close()

        elif os.path.isdir(path):
            os.makedirs(dst_path)
            cover_to_sc(path, dst_path)


def create_identifier(s):
    return uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/meng89/ncdzj" + s)


def write_epub(path, book, module, title, lang):
    _dir = os.path.split(path)[0]
    os.makedirs(_dir, exist_ok=True)
    epub = epubpacker.Epub()
    identifier_string = "元亨寺南傳大藏經" + module.info.name + lang
    if lang == "zh-Hans":
        identifier_string = trans_sc(identifier_string)

    epub.meta.identifier = identifier_string
    epub.meta.titles = [title]
    epub.meta.creators = module.info.translators
    epub.meta.languages.append(lang)
    epub.meta.date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%SZ")

    epub_notes = EpubNotes()
    write_epub_tree(book, epub_notes, epub, [], epub.mark, 0, 0, module, lang)
    for name, xml_str in epub_notes.pages(lang):
        epub.userfiles[name] = xml_str
        epub.spine.append(name)

    shuoming_filename = "电子书制作说明.xhtml"
    shuoming_path = os.path.join(config.PROJECT_ROOT, shuoming_filename)
    epub.userfiles[shuoming_filename] = open(shuoming_path).read()
    epub.mark.kids.append(epubpacker.Mark("电子书制作说明", shuoming_filename))
    epub.spine.append(shuoming_filename)

    epub.write(path)


def create_page(lang, title):
    html = xl.Element(
        "html",
        {
            "xmlns:epub": "http://www.idpf.org/2007/ops",
            "xmlns": "http://www.w3.org/1999/xhtml",
            "xml:lang": lang,
            "lang": lang
        }
    )
    head = html.ekid("head")
    head.ekid("title", kids=[title or "-"])
    html.ekid("body")
    return html


def write_epub_tree(d: base.Dir, epub_notes, epub, no_href_marks, parent_mark, mark_level, doc_count, module, lang):
    for name, obj in d.list:
        mark = epubpacker.Mark(name)
        parent_mark.kids.append(mark)

        if isinstance(obj, base.Doc):
            doc_count += 1
            doc_path = str(doc_count) + ".xhtml"
            html = write_doc(name, obj, lang, doc_path, epub_notes, mark, mark_level)
            htmlstr = xl.Xml(root=html).to_str(do_pretty=True, dont_do_tags=["title", "p", "h1", "h2", "h3", "h4", "h4", "h5", "h6",
                                                                             "a", "sen", "aside"])

            epub.userfiles[doc_path] = htmlstr
            epub.spine.append(doc_path)
            mark.href = doc_path
            for _mark in no_href_marks:
                _mark.href = doc_path
            no_href_marks = []

        elif isinstance(obj, base.Dir):
            no_href_marks.append(mark)
            doc_count, no_href_marks = write_epub_tree(obj, epub_notes, epub, no_href_marks, mark, mark_level + 1, doc_count, module, lang)

    return doc_count, no_href_marks


def write_doc(name, doc: base.Doc, lang, doc_path, epub_notes, parent_mark, mark_level):
    html = create_page(lang, name)
    body = html.find_kids("body")[0]
    es, note_count = trans_machine_to_epub_es(doc.body.kids, epub_notes, 0)
    epub_es = _make_doc_marks(es, doc_path, parent_mark, mark_level, 0)
    body.kids.extend(epub_es)
    return html

def _make_doc_marks(es, doc_path, parent_mark, mark_level, doc_mark_count):
    new_es = []
    marks = {}
    for e in es:
        if not isinstance(e, xl.Element) or e.tag not in ("h1", "h2", "h3", "h4", "h5", "h6",    "h7", "h8", "h9"):
            new_es.append(e)
            continue

        m = re.match(r"^h(\d)$", e.tag)
        assert m
        new_h_level = int(m.group(1)) + mark_level
        new_h = xl.Element("h{}".format(new_h_level), e.attrs, e.kids)
        new_es.append(new_h)
        id_ = _make_doc_mark_id(doc_mark_count)
        doc_mark_count += 1
        new_h.attrs["id"] = id_
        mark = epubpacker.Mark(new_h.kids[0], "{}#{}".format(doc_path, id_))
        marks[new_h_level] = mark

        parent_level = new_h_level - 1

        if parent_level in marks.keys():
            _parent_mark = marks[parent_level]
        else:
            _parent_mark = parent_mark

        _parent_mark.kids.append(mark)

    return new_es


def _make_doc_mark_id(doc_mark_count):
    return "id_sub_mark_{}".format(doc_mark_count)


def trans_machine_to_epub_es(es, epub_notes, note_count):
    note_count = note_count
    new_es = []
    for e in es:
        _es, note_count = trans_machine_to_epub_e(e, epub_notes, note_count)
        new_es.extend(_es)
    return new_es, note_count


def trans_machine_to_epub_e(e, epub_notes, note_count):
    for fun in [fun_ewn, fun_j, fun_list, fun_everything]:
        result = fun(e, epub_notes, note_count)
        if result is not None:
            return result
        else:
            continue

    raise Exception


def fun_ewn(e: xl.Element, epub_notes, note_count, ):
    if not isinstance(e, xl.Element) or e.tag != "ewn":
        return None

    href = epub_notes.add_note(e.kids[1].kids)
    note_count += 1
    a = e.ekid("a", {"epub:type": "noteref", "href" : href})
    a.kids.extend(e.kids[0].kids)
    if not a.kids:
        a.attrs["class"] = "notext"
        a.kids.append(str(note_count))
    return [a], note_count


def fun_j(e: xl.Element, epub_notes, note_count):
    if not isinstance(e, xl.Element) or e.tag != "j":
        return None

    div_j = xl.Element("div", {"class": "ji"})
    for term in e.kids:
        if term.tag == "p":
            div_j.ekid("div", {"class": "person"}, kids=term.kids)
        elif term.tag == "s":
            div_s = div_j.ekid("div", {"class": "sentence"})
            es, note_count = trans_machine_to_epub_es(term.kids, epub_notes, note_count)
            div_s.kids.extend(es)
    return [div_j], note_count

def fun_list(e: xl.Element, epub_notes, note_count):
    if not isinstance(e, xl.Element) or e.tag != "list":
        return None

    div_list = xl.Element("div", {"class": "list"})
    for term in e.kids:
        assert term.tag == "item"
        div_item = div_list.ekid("div", {"class": "item"})
        es, note_count = trans_machine_to_epub_es(term.kids, epub_notes, note_count)
        div_item.kids.extend(es)
    return [div_list], note_count



def fun_everything(e, epub_notes, note_count):
    note_count = note_count
    if isinstance(e, xl.Element):
        new_e = xl.Element(e.tag, e.attrs)
        new_es, note_count = trans_machine_to_epub_es(e.kids, epub_notes, note_count)
        new_e.kids.extend(new_es)
        return [new_e], note_count
    else:
        return [e], note_count


class EpubNotes:
    def __init__(self):
        self._pages = []

    def add_note(self, es):
        match len(self._pages):
            case 0:
                page = []
                self._pages.append(page)
            case _:
                page = self._pages[-1]

        if len(page) == 100:
            page = []
            self._pages.append(page)

        page_index = self._pages.index(page)
        page.append(es)
        note_index = page.index(es)

        return "note_page{}.xhtml#note{}".format(page_index + 1, note_index + 1)

    def pages(self, lang):
        _pages = []
        for page_index, page in enumerate(self._pages):
            _page_html = create_page(lang, "Note {}".format(page_index + 1))
            _body = _page_html.find_kids("body")[0]
            _section = _body.ekid("section", {"epub:type": "endnotes", "role": "doc-endnotes"})
            ol = _section.ekid("ol")
            for note_index, note_es in enumerate(page):
                li = ol.ekid("li", {"id": "note{}".format(note_index + 1)})
                #p = li.ekid("p")
                #p.kids.extend(note_es)
                li.kids.extend(note_es)
            _pages.append(
                (
                    "note_page{}.xhtml".format(page_index + 1),
                    _page_html.to_str(do_pretty=True, dont_do_tags=["title", "link", "script", "p", "li"])
                    )
            )
        return _pages


# 短小的合并之类操作应该修改dir对象来完成

def check_epub(epub_path):
    stdout_file_path = "{}_{}".format(epub_path, "stdout")
    stdout_file = open(stdout_file_path, "w")
    stderr_file_path = "{}_{}".format(epub_path, "stderr")
    stderr_file = open(stderr_file_path, "w")

    def _run():
        nonlocal check_result
        compile_cmd = "java -jar {} {} -q".format(config.EPUBCHECK, epub_path)
        cwd = os.path.split(epub_path)[0]
        # print("运行:", compile_cmd, end=" ", flush=True)
        print("检查", os.path.split(epub_path)[1], ": ", end="", flush=True)
        p = subprocess.Popen(compile_cmd, cwd=cwd, shell=True, stdout=stdout_file, stderr=stderr_file)
        p.communicate()

        if p.returncode != 0:
            return False
        else:
            return True

    check_result = _run()
    if check_result:
        print("Passed")
    else:
        print("Failed")

    if os.path.getsize(stdout_file_path) == 0:
        os.remove(stdout_file_path)
    if os.path.getsize(stderr_file_path) == 0:
        os.remove(stderr_file_path)

    return check_result


def main():
    # zh-Hans: 简体中文
    # zh-Hant: 传统中文
    td = tempfile.TemporaryDirectory(prefix="ncdzj_")

    for category, ms in book_module.categories:
        a = None
        for m in ms:
            if hasattr(m, "get_book"):
                book = m.get_book()
            else:
                book = load_book_from_dir(m)
            if hasattr(m, "change2"):
                book = m.change2(book)

            title = "漢譯南傳大藏經·{}·{}".format(category, m.info.name)

            path = os.path.join(td.name, "漢譯南傳大藏經", category, "元_{}_繁.epub".format(m.info.name))
            write_epub(path, book, m, title, "zh-Hant")
            check_epub(path)

            ################################################################################################################

            book = book.trans_2_sc()
            title = trans_sc(title)
            path = os.path.join(td.name, "汉译南传大藏经", trans_sc(category), trans_sc("元_{}_简.epub".format(m.info.name)))
            write_epub(path, book, m, title, "zh-Hans")
            check_epub(path)


    input("Press any key to exit:")


if __name__ == '__main__':
    main()
