import xl
import epubpacker
from pyccc import book_public
import dopdf


_fl = (
    "1.巴利語經文與經號均依「台灣嘉義法雨道場流通的word版本」(緬甸版)。",

    "2.巴利語經文之譯詞，以水野弘元《巴利語辭典》(昭和50年版)為主，其他辭典或Ven.Bhikkhu Bodhi之英譯為輔，"
    "詞性、語態儘量維持與巴利語原文相同，並採「直譯」原則。譯文之「性、數、格、語態」儘量符合原文，「呼格」(稱呼；呼叫某人)以標點符號「！」表示。",

    "3.註解中作以比對的英譯，採用Ven.Bhikkhu Bodhi, Wisdom Publication, 2000年版譯本為主。",

    "4.《顯揚真義》(Sāratthappakāsinī, 核心義理的說明)為《相應部》的註釋書，"
    "《破斥猶豫》(Papañcasūdaṇī, 虛妄的破壞)為《中部》的註釋書，"
    "《吉祥悅意》(Sumaṅgalavilāsinī, 善吉祥的優美)為《長部》的註釋書，"
    "《滿足希求》(Manorathapūraṇī, 心願的充滿)為《增支部》的註釋書，"
    "《勝義光明》(paramatthajotikā, 最上義的說明)為《小部/經集》等的註釋書，"
    "《勝義燈》(paramatthadīpanī, 最上義的註釋)為《小部/長老偈》等的註釋書。",

    "5.前後相關或對比的詞就可能以「；」區隔強調，而不只限於句或段落。"
)


def write_fanli(epub: epubpacker.Epub, xc: book_public.XC):
    html = xl.Element("html", {"xmls": "http://www.w3.org/1999/xhtml",
                               "xml:lang": xc.xmlang,
                               "lang": xc.xmlang})
    head = xl.sub(html, "head")
    _title = xl.sub(head, "title", kids=["凡例"])
    body = xl.sub(html, "body")
    _h1 = xl.sub(body, "h1", kids=["凡例"])

    for one in _fl:
        p = xl.sub(body, "p", kids=[xc.c(one)])

    doc_path = "fanli.xhtml"
    htmlstr = xl.Xl(root=xl.pretty_insert(html, dont_do_tags=["p"])).to_str()
    epub.userfiles[doc_path] = htmlstr
    epub.spine.append(doc_path)
    epub.root_toc.append(epubpacker.Toc("凡例", doc_path))
