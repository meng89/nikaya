import re


def analyse_head_lines(lines):  # public
    # 根本五十則篇
    # 1.根本法門品

    info = {}
    for line in lines[:-1]:

        # '(1)有偈篇' SN.1.1
        m = re.match('^\((\d)\)(\S+篇)$', line)
        if m:
            info['pian_no'] = m.group(1)
            info['pian_title'] = m.group(2)
            continue

        m = re.match('^(\S+篇)$', line)
        if m:
            info['pian_title'] = m.group(1)
            continue

        m = re.match('^(\d+)\.?(\S+品)$', line)
        if m:
            info['pin_no'] = m.group(1)
            info['pin_title'] = m.group(2)
            continue

        # 长部 二、大品
        m = re.match('^\S+、(\S+品)$', line)
        if m:
            info['pin_title'] = m.group(1)

        m = re.match('\d+[\./](?:\(\d+\))?\.?(.+相應)$', line)
        if m:
            info['xiangying_title'] = m.group(1)
            continue

    # 相应部
    m = re.match('^ *相+應部?(\d+)相應 ?第?(\d+(?:\-\d+)?)經(?:/(.+?經.*?))?\((?:\S+?)相應/(?:\S+?)篇/(?:\S+?)\)', lines[-1])
    if m:
        info['xiangying_no'] = m.group(1)
        info['sutra_title'] = m.group(3)

    m = re.match('^相應部(48)相應 (83)-(114)經$', lines[-1])
    if m:
        info['xiangying_no'] = m.group(1)
        info['sutra_title'] = ''

    # 中部：
    # 中部1經/根本法門經(根本法門品[1])(莊春江譯)
    # 中部24經接力車經(譬喻品[3])(莊春江譯)
    m = re.match('^\S+?(\d+)經/?(\S+經)\((\S+品)\[(\d+)\]\)\(莊春江譯\)$', lines[-1])
    if m:
        info['sutra_title'] = m.group(2)
        info['pin_title'] = m.group(3)
        info['pin_no'] = m.group(4)

    # 长部
    # 長部14經/譬喻大經(大品[第二])(莊春江譯)
    m = re.match('^長部(\d+)經/(\S+經)\((\S+品)\[\S+\]\)\(莊春江譯\)$', lines[-1])
    if m:
        info['sutra_title'] = m.group(2)
        info['pin_title'] = m.group(3)

    # 增支部
    # 增支部1集1經(莊春江譯)
    # 增支部6集35經/明的一部分經(莊春江譯)
    m = re.match('^增支部(\d+)集(\d+(?:\-\d+)?)經(?:/?(\S+經(\S+)?|))\(莊春江譯\)$', lines[-1])
    if m:
        info['ji_no'] = m.group(1)
        info['sutra_title'] = m.group(3)
    return info


def split_chinese_lines(chinese):
    lines = chinese.strip().splitlines()

    head_lines = []
    main_lines = []

    is_sutra_name_line_passed = False

    for line in lines:
        if is_sutra_name_line_passed:
            main_lines.append(line)
        else:
            head_lines.append(line)
            if re.search('\(莊春江譯\)', line):
                is_sutra_name_line_passed = True

            elif re.match('相應部48相應 83-114經', line):
                is_sutra_name_line_passed = True

    return head_lines, main_lines
