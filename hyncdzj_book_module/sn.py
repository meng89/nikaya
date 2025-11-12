import re

import cn2an

from hyncdzj import base

info = base.Info(6, "相應部", ("通妙", "雲庵"), "SN")


# 原始 p5a 转换成的 simple, 调用此函数处理一下


def change_name_fun(name):
    m = re.match(r"(\S+篇)", name)
    if m:
        return m.group(1)
    else:
        return name


def change(data):
    xy_seril_map = []
    doc_seril_map = []

    data, _ = _change_name(data, 1, xy_seril_map, doc_seril_map)

    data = _change_j_name(xy_seril_map, data, doc_seril_map)

    return data


def _change_name(d, xy_index, xy_seril_map: list, j_seril_map: list):
    new_data = []
    #xy_index = None
    for name, obj in d:
        #print(repr(name))

        if name == "":
            new_name = name
        elif name.endswith("篇"):
            new_name = name
        else:
            m = re.match(r"^第[一二三四五六七八九十〇]+　(\S+)$", name)
            if m:
                new_name = m.group(1)
                if new_name.endswith("相應"):
                    xy_seril_map.append((obj, xy_index))
                    new_name = str(xy_index) + " " + new_name
                    xy_index += 1
                    print(xy_index)
            elif re.match("〔[一二三四五六七八九十〇～、]+〕", name):

                # '〔一〕瀑流'
                m = re.match(r"^〔([一二三四五六七八九十〇]+)〕　?(\S+)?$", name)
                if m:
                    #print(repr(m.group(1)), repr(m.group(2)))
                    start = end = cn2an.cn2an(m.group(1), "normal")
                    new_name = m.group(2) or ""
                    j_seril_map.append((obj, start, end))
                else:
                    # '〔二一〕第一\u3000依劍'
                    # '〔一六八〕第四、五、六\u3000欲念（四、五、六）'
                    # '〔一七四〕第廿二～廿四\u3000過去（四～六）'
                    # '〔三〕第三\u3000舍利弗——拘絺羅\u3000第一（住者）'
                    m = re.match(r"^〔([一二三四五六七八九十〇]+)〕"
                                 r"第[一二三四五六七八九十〇、～廿卅]+　?(.+)?$", name)
                    if m:
                        #print(repr(m.group(1)), repr(m.group(2)))
                        start = end = cn2an.cn2an(m.group(1), "normal")
                        new_name = m.group(2) or ""
                        j_seril_map.append((obj, start, end))
                    else:
                        #'〔七二～八〇〕第二～第十\u3000不知（之一）'
                        #'〔二五～二六〕第三～四\u3000無常（一～二）'
                        #'〔一一～二〇〕第十一\u3000布施利益（一）'
                        #'〔五六、五七〕第四、第五\u3000諸漏（一～二）'
                        m = re.match(r"^〔([一二三四五六七八九十〇]+)[～、]([一二三四五六七八九十〇]+)〕"
                                     r"[第一二三四五六七八九十〇～、]+　?(\S+)?$", name)
                                     # r"第[一二三四五六七八九十〇]+～第?[一二三四五六七八九十〇]+　?(\S+)?$", name)
                        if m:
                            start = cn2an.cn2an(m.group(1), "normal")
                            end = cn2an.cn2an(m.group(2), "normal")
                            new_name = m.group(3) or ""
                            j_seril_map.append((obj, start, end))
                        else:
                            if name == "〔三八～四三〕第八　父、第九　兄弟、第十　姊妹、第十一　子、第十二　女、第十三　妻":
                                start = 38
                                end = 43
                                new_name = "父、兄弟、姊妹、子、女、妻"
                                j_seril_map.append((obj, start, end))
                            else:
                                raise Exception(repr(name))
            else:
                if "〔" in name:
                    # print(repr(name))
                    pass
                new_name = name

        if isinstance(obj, list):
            new_obj, xy_index = _change_name(obj, xy_index, xy_seril_map, j_seril_map)
        else:
            new_obj = obj

        new_data.append((new_name, new_obj))

    return new_data, xy_index


def _change_j_name(xy_seril_map: list, d: list, j_seril_map: list):

    new_list = []
    for name, obj in d:
        result = _find_j_range(obj, j_seril_map)
        if result is not None:

            start, end = result
            xy_index = _find_xy_index(xy_seril_map, obj)
            new_name = "SN {}.{}".format(xy_index, start)
            if end != start:
                new_name = new_name + "～" + str(end)
            new_name += " " + name
            new_list.append((new_name, obj))
            print(new_name)
        else:
            new_list.append((name, obj))

        if isinstance(obj, list):
            _change_j_name(xy_seril_map, obj, j_seril_map)
            #todo

    return new_list


def _find_j_range(obj, j_seril_map):
    for j_obj, start, end in j_seril_map:
        if j_obj == obj:
            return start, end
    return None

def _find_xy_index(xy_seril_map, obj):
    for xy, index in xy_seril_map:
        if _is_contain(xy, obj):
            return index
    assert Exception

def _is_contain(obj: base.Folder, j: base.Folder):
    for name, x in obj:
        if x == j:
            return True
        elif isinstance(x, list):
            result = _is_contain(x, j)
            if result:
                return True
            else:
                continue
    return False


def change2(d: base.Folder):
    return add_range_to_name(d)

# 写入range
def add_range_to_name(d: base.Folder):
    return _add_range_to_name([], d)

def _add_range_to_name(branch: list, d: base.Folder):
    new_list = []
    for name, obj in d:
        if not isinstance(obj, base.Folder):
            new_list.append((name, obj))
            continue

        new_branch = branch.copy()
        new_branch.append(name)
        new_obj = _add_range_to_name(new_branch, obj)

        obj_type = _type(branch, name)
        if  obj_type == "PIAN":
            xy_serials = _get_xy_serials(obj)
            new_name = "{}({}～{})".format(name, min(xy_serials), max(xy_serials))
        elif obj_type == "PIN":
            jing_serials = _get_jing_serials(obj)
            new_name = "{}({}～{})".format(name, min(jing_serials), max(jing_serials))
        else:
            new_name = name

        new_list.append((new_name, new_obj))

    return new_list


def _type(branch, name):
    types = [_type2(s) for s in branch]
    my_type = _type2(name)

    if my_type == "PIAN" and "PIAN" not in types:
        return "PIAN"
    elif my_type == "XY" and "PIAN" in types and "XY" not in types:
        return "XY"
    elif my_type == "JING" and "PIAN" in types and "XY" in types and "JING" not in types:
        return "JING"
    elif my_type is None and "PIAN" in types and "XY" in types and "JING" not in types:
        return "PIN"
    elif my_type is None and "PIAN" in types and "XY" in types and "JING" in types:
        return "SUB"

def _type2(name):
    if name.endswith("篇"):
        return "PIAN"
    elif re.match(r"^\d+ \S+相應$", name):
        return "XY"
    elif re.match(r"^SN \d+", name):
        return "JING"
    else:
        return None

def _get_xy_serials(d: base.Folder):
    serials = []
    for name, obj in d:
        m = re.match(r"^(\d+) \S+相應$", name)
        if m:
            serials.append(int(m.group(1)))
        if isinstance(obj, base.Folder):
            serials.extend(_get_xy_serials(obj))
    return serials


def _get_jing_serials(d: base.Folder):
    serials = []
    for name, obj in d:
        m = re.match(r"^SN \d+\.(\d+)(?:～(\d+))?", name)
        if m:
            serials.append(int(m.group(1)))
            if m.group(2):
                serials.append(int(m.group(2)))
        if isinstance(obj, base.Folder):
            serials.extend(_get_jing_serials(obj))
    return serials


