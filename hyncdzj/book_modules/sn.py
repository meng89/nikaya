import re

import cn2an

from nikaya_share import Info


info = Info(
    serial = 6,
    name = "相應部",
    pali = "Saṃyutta Nikāya",
    translators = ("通妙", "雲庵"),
    abbr = "SN",
)


# 原始 p5a 转换成的 simple, 调用此函数处理一下


def change_name_fun(name):
    m = re.match(r"(\S+篇)", name)
    if m:
        return m.group(1)
    else:
        return name


def change(raw_data):
    data, _xiangying_index = change2(raw_data, 0)
    return data


def change2(raw_data, xiangying_index):
    data = []
    for name, obj in raw_data:
        name_group, xiangying_index = name_to_group(name, xiangying_index)
        if isinstance(obj, list):
            sub_data, xiangying_index = change2(obj, xiangying_index)
        else:
            sub_data = obj
        data.append((name_group, sub_data))
    return data, xiangying_index


def name_to_group(name: str, xiangying_index):
    if name == "":
        return (None, None, None), xiangying_index

    if name.endswith("篇"):
        return (None, None, name), xiangying_index

    if name == "〔五一～五五〕第五十一～五十五　不現見（一～五）":
        return (None, None, "不現見"), xiangying_index
    if name == "第五十一　不現見（一）":
        return (51, 51, "不現見"), xiangying_index
    if name == "第五十二～五十四　不現見（二～四）":
        return(52, 54, "不現見"), xiangying_index
    if name == "第五十五　不現見（五）":
        return (55, 55, "不現見"), xiangying_index

    m = re.match(r"^第[一二三四五六七八九十〇]+　(\S+)$", name)
    if m:
        new_name = m.group(1)
        if new_name.endswith("相應"):
            xiangying_index += 1
            return (xiangying_index, xiangying_index, new_name), xiangying_index
        else:
            return (None, None, new_name), xiangying_index

    # '〔一〕瀑流'
    m = re.match(r"^〔([一二三四五六七八九十〇]+)〕　?(\S+)?$", name)
    if m:
        start = end = cn2an.cn2an(m.group(1), "normal")
        name = m.group(2)
        return (start, end, name), xiangying_index

    # '〔二一〕第一\u3000依劍'
    # '〔一六八〕第四、五、六\u3000欲念（四、五、六）'
    # '〔一七四〕第廿二～廿四\u3000過去（四～六）'
    # '〔三〕第三\u3000舍利弗——拘絺羅\u3000第一（住者）'
    m = re.match(r"^〔([一二三四五六七八九十〇]+)〕第[一二三四五六七八九十〇、～廿卅]+　?(.+)?$", name)
    if m:
        start = end = cn2an.cn2an(m.group(1), "normal")
        new_name = m.group(2)
        return (start, end, new_name), xiangying_index

    if name == "〔一三～二〇〕第三～第十　金環——地方之美人":
        return (None, None, "金環——地方之美人"), xiangying_index

    # 界蘊品 里
    if name == "〔一二～二〇〕第二～第十":
        return (None, None, None), xiangying_index

    #'〔七二～八〇〕第二～第十\u3000不知（之一）'
    #'〔二五～二六〕第三～四\u3000無常（一～二）'
    #'〔一一～二〇〕第十一\u3000布施利益（一）'
    #'〔五六、五七〕第四、第五\u3000諸漏（一～二）'
    m = re.match(r"^〔([一二三四五六七八九十〇]+)[～、]([一二三四五六七八九十〇]+)〕[第一二三四五六七八九十〇～、]+　?(\S+)?$", name)

    if m:
        start = cn2an.cn2an(m.group(1), "normal")
        end = cn2an.cn2an(m.group(2), "normal")
        new_name = m.group(3)
        return(start, end, new_name), xiangying_index

    if name == "〔三八～四三〕第八　父、第九　兄弟、第十　姊妹、第十一　子、第十二　女、第十三　妻":
        #start = 38
        #end = 43
        new_name = "父、兄弟、姊妹、子、女、妻"
        return (None, None, new_name), xiangying_index


    return (None, None, name), xiangying_index
