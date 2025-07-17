import os.path

import xl

import pyabo2.page_parsing

name_han = "優陀那" # 自说经
name_pali = "Udānapāḷi"
short = "Ud"
htmls = ["Ud/Ud{:0>2d}.htm".format(x) for x in range(1, 81)]


try:
    import user_config as config
except ImportError:
    import config as config


def trans_files():
    for x in pyabo2.page_parsing.read_pages(htmls):
        mtime, homage_line, head_lines, sutta_name_part, translator_part, agama_part, body, notes, pali_doc = x

        doc = xl.Element("doc")
        meta = doc.ekid("meta")
        doc.kids.append(body)
        doc.kids.append(notes)

        xml = xl.Xml(root=doc)
        data = xml.to_str(do_pretty=True, dont_do_tags=["p", "note"])
        open("1.xml", "w").write(data)



        print("mtime:", mtime)
        print()

        print("homage_line:", homage_line)
        print()

        print("sutta_name_part:", sutta_name_part)
        print()

        print("translator_part:", translator_part)
        print()

        print("agama_part:", agama_part)
        print()

        print("body_lines:", body)
        print()

        print("pali_doc:", pali_doc)
        print()


        break