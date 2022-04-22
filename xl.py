# The MIT License

""" XML without mess """

from abc import abstractmethod
import copy


_xml_escape_table = [
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;')
]

_xml_attr_escape_table = _xml_escape_table + [
    ('"', '&quot;'),
    ("'", "&apos;")
]


def _unescape(text, table):
    _text = text
    nt = ""
    i = 0
    while i < len(text):
        unescaped = False
        for x, y in table:
            if text[i: i + len(y)] == y:
                nt += x
                i += len(y)
                unescaped = True
                break
        if not unescaped:
            nt += text[i]
            i += 1
    return nt


def _escape(text, table):
    nt = ""
    for c in text:
        escaped = False
        for x, y in table:
            if c == x:
                nt += y
                escaped = True
                break
        if not escaped:
            nt += c
    return nt


def clean_whitespaces(element):
    if not isinstance(element, Element):
        raise TypeError

    new_element = Element(tag=copy.deepcopy(element.tag),
                          attrs=copy.deepcopy(element.attrs))

    for child in element.kids:
        if isinstance(child, str):
            new_text = child.strip()
            if new_text:
                new_element.kids.append(new_text)
        elif isinstance(child, Element):
            new_element.kids.append(clean_whitespaces(child))

    return new_element


def _is_straight_line(element):
    if len(element.kids) == 0:
        return True

    if len(element.kids) == 1:
        if isinstance(element.kids[0], Element):
            return _is_straight_line(element.kids[0])
        else:
            return True

    elif len(element.kids) > 1:
        return False


def pretty_insert(element,
                  start_indent=0,
                  step=4,
                  insert_str=None,
                  dont_do_between_str=True,
                  dont_do_when_one_kid=True,
                  dont_do_tags=None):

    insert_str = insert_str or " "
    dont_do_tags = dont_do_tags or []
    new_e = Element(tag=copy.deepcopy(element.tag), attrs=copy.deepcopy(element.attrs))

    if (dont_do_when_one_kid and _is_straight_line(element)) or element.tag in dont_do_tags:
        for kid in element.kids:
            new_e.kids.append(copy.deepcopy(kid))

    elif element.kids:
        _indent_text = '\n' + insert_str * (start_indent + step)
        last_type = None
        for kid in element.kids:
            if isinstance(kid, str):
                if dont_do_between_str and last_type == str:
                    pass
                else:
                    new_e.kids.append(_indent_text)
                new_e.kids.append(kid)

            elif isinstance(kid, Element):
                new_e.kids.append(_indent_text)

                new_e.kids.append(pretty_insert(element=kid,
                                                start_indent=start_indent + step,
                                                step=step,
                                                insert_str=insert_str,
                                                dont_do_between_str=dont_do_between_str,
                                                dont_do_when_one_kid=dont_do_when_one_kid,
                                                dont_do_tags=dont_do_tags
                                                ))
            last_type = type(kid)

        new_e.kids.append('\n' + ' ' * start_indent)

    return new_e


class XLError(Exception):
    pass


class Xl(object):
    def __init__(self, prolog=None, doc_type=None, root=None):

        self.prolog = prolog or Prolog()
        self.doc_type = doc_type
        self.root = root

    def to_str(self):
        s = ''
        if self.prolog:
            s += self.prolog.to_str() + '\n'
        if self.doc_type:
            s += self.doc_type.to_str() + '\n'
        s += self.root.to_str()
        return s


class _Node(object):
    @abstractmethod
    def to_str(self):
        pass


class Prolog(_Node):
    def __init__(self, version=None, encoding=None, standalone=None):
        self.version = version or '1.0'
        self.encoding = encoding or 'UTF-8'
        self.standalone = standalone

    def to_str(self):
        if not (self.version or self.encoding or self.standalone):
            return ''

        s = '<?xml'
        if self.version:
            s += ' version="{}"'.format(self.version)
        if self.encoding:
            s += ' encoding="{}"'.format(self.encoding)
        if self.standalone is not None:
            s += ' standalone="'
            s += self.standalone.lower()
            s += '"'
        s += ' ?>'
        return s


class DocType(_Node):
    def __init__(self, doc_type_name, system_id, public_id):
        self.doc_type_name = doc_type_name
        self.system_id = system_id
        self.public_id = public_id

    def to_str(self):
        s = '<!DOCTYPE'
        s += ' {}'.format(self.doc_type_name)
        s += ' "{}"'.format(self.public_id)
        s += ' "{}"'.format(self.system_id)
        s += '>'
        return s


class InitError(Exception):
    pass


class Element(_Node):
    def __init__(self, tag=None, attrs=None, kids=None, fromstr=None):
        _Node.__init__(self)
        if bool(tag) == bool(fromstr) or (not tag and not fromstr):
            raise InitError()
        if tag:
            self.tag = tag
            self._attrs = dict(attrs) if attrs else {}
            self._kids = list(kids) if kids else []
        else:
            pass  # todo

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if not isinstance(value, str):
            raise ValueError
        self._tag = value

    @property
    def attrs(self):
        return self._attrs

    @property
    def kids(self):
        return self._kids

    def to_str(self):
        s = '<'
        s += self.tag

        _attrs_string_list = []
        for attr_name, attr_value in self.attrs.items():
            _attrs_string_list.append('{}="{}"'.format(attr_name, _escape(attr_value, _xml_attr_escape_table)))

        if _attrs_string_list:
            s += ' '
            s += ' '.join(_attrs_string_list)

        if self.kids:
            s += '>'
            for kid in self.kids:
                if isinstance(kid, Element):
                    s += kid.to_str()
                elif isinstance(kid, str):
                    s += _escape(kid, _xml_escape_table)
            s += '</{}>'.format(self.tag)

        else:
            s += ' />'

        return s

    def find_attr(self, attr):
        for _attr, value in self.attrs.items():
            if _attr == attr:
                return value

    def find_all(self, tag):
        es = []
        if self.tag == tag:
            es.append(self)
        for kid in self.kids:
            if isinstance(kid, Element):
                es.extend(kid.find_all(tag))
        return es

    def find_kids(self, tag):
        kids = []
        for kid in self.kids:
            if isinstance(kid, Element) and kid.tag == tag:
                kids.append(kid)
        return kids


def sub(element, tag, attrs=None, kids=None):
    sub_element = Element(tag, attrs, kids)
    element.kids.append(sub_element)
    return sub_element


def parse_prolog(text, i):
    prolog = Prolog()

    if text[i] != "<":
        raise ParseError
    i += 1
    i = ignore_blank(text, i)
    if text[i] != "?":
        raise ParseError
    i += 1
    i = ignore_blank(text, i)
    if text[i:i+3] != "xml":
        raise ParseError
    i += 3
    i = ignore_blank(text, i)

    while i < len(text) and text[i] not in "?>":
        key, value, i = read_attr(text, i)
        setattr(prolog, key.lower(), value)
        i = ignore_blank(text, i)

    i = ignore_blank(text, i)
    if text[i] != "?":
        raise ParseError
    i += 1
    i = ignore_blank(text, i)
    if text[i] != ">":
        raise ParseError
    i += 1
    return prolog, i


_blank = (" ", "\t", "\n", "\r")


def ignore_blank(text, i):
    while i < len(text):
        if text[i] not in _blank:
            return i
        else:
            i += 1
    return i


def read_tag(text, i):
    tag = ""
    while i < len(text) and text[i] not in " />":
        tag += text[i]
        i += 1
    return tag, i


def read_endtag(text, i):
    tag = ""
    while i < len(text) and text[i] not in " >":
        tag += text[i]
        i += 1
    return tag, i


def read_text(text, i):
    t = ""
    while i < len(text) and text[i] not in "<":
        t += text[i]
        i += 1
    return t, i


#  ↑↓←→↖↗↙↘
def parse_element(text, i):
    # <a id="1">xx<b/>yy</a>
    # ↑           ↑
    if text[i] != "<":
        raise ParseError

    i = ignore_blank(text, i + 1)
    tag, i = read_tag(text, i)
    e = Element(tag=tag)

    i = ignore_blank(text, i)
    while i < len(text) and text[i] not in "/>":
        # <a id="1">xx<b/>yy</a>
        #          ↖
        key, value, i = read_attr(text, i)
        e.attrs[key] = value
        i = ignore_blank(text, i)

    if text[i] == "/":
        # <a id="1">xx<b/>yy</a>
        #               ↑
        i += 1
        i = ignore_blank(text, i)
        if text[i] != ">":
            raise ParseError
        i += 1
        return e, i

    elif text[i] == ">":
        # <a id="1">xx<b/>yy</a>
        #          ↑
        i += 1

    while i < len(text):
        if text[i] == "<":
            # <a id="1">xx<b/>yy</a>
            #             ↑     ↑
            kid_e_i = i
            i += 1
            i = ignore_blank(text, i)
            if text[i] == "/":
                # <a id="1">xx<b/>yy</a>
                #                    ↑
                i += 1
                i = ignore_blank(text, i)

                # <a id="1">xx<b/>yy</a>
                #                     ↑
                end_tag, i = read_endtag(text, i)
                if tag != end_tag:
                    print(tag, end_tag)
                    raise ParseError
                i = ignore_blank(text, i)
                # <a id="1">xx<b/>yy</a>
                #                      ↑
                if text[i] != ">":
                    raise ParseError
                i += 1
                return e, i

            else:
                # <a id="1">xx<b/>yy</a>
                #             ↑
                kid, i = parse_element(text, kid_e_i)
                e.kids.append(kid)

        else:
            # <a id="1">xx<b/>yy</a>
            #           ↑     ↑
            string_e, i = read_text(text, i)
            e.kids.append(_unescape(string_e, _xml_escape_table))
    raise ParseError


def read_attr(text, i):

    key, border, i = read_till(text, i, "=")
    key = key.strip()
    i = ignore_blank(text, i)
    qmark = text[i]
    i += 1
    string_value, _, i = read_till(text, i, qmark)
    return key, _unescape(string_value, _xml_attr_escape_table), i


def parse_str(text):
    return _unescape(text, _xml_escape_table)


def parse(text: str):
    i = ignore_blank(text, 0)
    prolog, i = parse_prolog(text, i)
    i = ignore_blank(text, i)
    root, i = parse_element(text, i)
    xl = Xl(prolog, root=root)

    return xl


def read_till(text, bi, chars):
    xs = ""
    while bi < len(text):
        if text[bi] not in chars:
            xs += text[bi]
            bi += 1
        else:
            return xs, text[bi], bi + 1

    return xs, None, bi


class ParseError(Exception):
    pass
