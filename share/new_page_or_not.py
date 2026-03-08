import math

import xl

from . import utils
from share import tag_str


"""
增支部前面的那些都是篇幅小的经，而且相关，如果每个这样的小经都是占用一个页面，翻页受累
长部这样的大篇幅经文，如果一个页面里一篇的经文的尾部连上后一篇经文的标题，看着难受
所以需要判断一个 obj 是否需要前后分页。所谓分页，在 PDF 中就是前后增加 \\page[yes]，在 EPUB 中就是增加一个新 xhtml

1. 如果 obj 是经的上一级，要前后分页
    判断一个 obj 的 sub 里是否有编号

2. 如果 obj 是经的一部分，不分页
    先判断 obj 这的 namegroups 里的前面是否有编号，而且这个编号是这个树里最深的编号

3. 如果 obj 是经，则还要看同级占用的页面大小。如果大部分都是小经，没必要分页，反之则分页
    先判断 obj 这的 namegroups 里是否有编号，而且这个编号是这个树里最深的编号
    先获取上级 obj，判断上级的所有子级

4. 无编号书籍的情况
     检查子级的类型是xml的数量是否有大于 1，如果大于 1 说明子级是经，接下来就按照 3 的判断方法。
"""


def merge_or_not(ngs, obj, ds_depth, max_hanzi_in_line=35, max_line_in_page=29):
    namegroups = ngs
    if ds_depth > 0:
        serial_count = 0
        on_serial = False

        for start, _end, _name in namegroups:
            if isinstance(start, int):
                serial_count += 1
                on_serial = True
            else:
                on_serial = False

        if serial_count < ds_depth:
            obj_type = "before_or_shesong"
            small_count, medium_count, large_count = count_docs_size(obj, max_hanzi_in_line, max_line_in_page)
            v = is_ratio_greater(small_count, large_count + medium_count, 1)
            return v

        elif serial_count == ds_depth:
            if on_serial:
                obj_type = "is_doc"
                return True
            else:
                obj_type = "after_doc"
                return True

        raise Exception(ngs)

    # 没有编号的书籍
    else:
        xml_count = 0
        list_count = 0
        for name, sub in obj:
            if isinstance(sub, list):
                list_count += 1
            else:
                xml_count += 1

        if xml_count > 1:
            obj_type = "is_doc"
            small_count, medium_count, large_count = count_docs_size(obj, max_hanzi_in_line, max_line_in_page)
            v = is_ratio_greater(small_count, large_count + medium_count, 1)
            return v

        elif xml_count == 1:
            return False

        else:
            return False


# 遍历 data 查找 serial 深度
def get_data_depth(data):
    max_depth = 0
    for namegroup, sub in data:
        (start, end, name) = namegroup
        if isinstance(start, int):
            sub_depth = 1
        else:
            sub_depth = 0
        if isinstance(sub, list):
            sub_sub_depth = get_data_depth(sub)
        else:
            sub_sub_depth = 0
        cur_depth = sub_depth + sub_sub_depth

        if cur_depth > max_depth:
            max_depth = cur_depth

        max_depth = max(sub_depth + sub_sub_depth, max_depth)
    return max_depth


# 获取 obj 的 namegroups
def get_keys(data, obj, keys=None):
    keys = keys or []
    for namegroup, sub in data:
        my_keys = keys + [namegroup]
        if sub is obj:
            return my_keys
        elif isinstance(sub, list):
            value = get_keys(sub, obj, my_keys)
            if value:
                return value
    return []


count_cache = []
def count_docs_size(parent_obj, max_hanzi_in_line, max_line_in_page):
    for (a, b, c), value in count_cache:
        if a is parent_obj and b == max_hanzi_in_line and c == max_line_in_page:
            return value
    value =  _count_docs_size(parent_obj, max_hanzi_in_line, max_line_in_page)
    count_cache.append(((parent_obj, max_hanzi_in_line, max_line_in_page), value))
    return value

def _count_docs_size(obj: list, max_hanzi_in_line, max_line_in_page):
    small_page_count = 0
    large_page_count = 0
    medium_page_count = 0

    for name, sub in obj:
        if isinstance(sub, xl.Element):
            line_count = count_xml_line(sub, max_hanzi_in_line)

        else:
            assert isinstance(sub, list)
            line_count = count_list_line(sub, max_hanzi_in_line)

        if line_count < max_line_in_page * 0.7:
            small_page_count += 1
        elif line_count > max_line_in_page:
            large_page_count += 1
        else:
            medium_page_count += 1
    return small_page_count, medium_page_count, large_page_count


def count_list_line(obj, max_hanzi_in_line):
    line_count = 3
    for _, sub in obj:
        if isinstance(sub, list):
            line_count += count_list_line(sub, max_hanzi_in_line)
        elif isinstance(sub, xl.Element):
            line_count += count_xml_line(sub, max_hanzi_in_line)
    return line_count


def count_xml_line(obj, max_hanzi_in_line):
    line_count = 3
    for sub in obj.kids:
        if sub.tag == "p":
            txt = utils.line_to_txt(sub.kids)
            cjk_count, other_count = tag_str.count(txt.strip())
            line_count += math.ceil((2 + cjk_count + other_count * 0.5) / max_hanzi_in_line)

        elif sub.tag == "j":
            line_count += len(sub.kids)

    return line_count


def is_ratio_greater(num1, num2, threshold):
    try:
        if num1 / num2 > threshold:
            return True
        else:
            return False
    except ZeroDivisionError:
        return True
