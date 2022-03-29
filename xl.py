# The MIT License

""" XML without mess """

from abc import abstractmethod
import copy


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
    def __init__(self, header=None, doc_type=None, root=None):

        self.header = header or Header()
        self.doc_type = doc_type
        self.root = root

    def to_str(self):
        s = ''
        if self.header:
            s += self.header.to_str() + '\n'
        if self.doc_type:
            s += self.doc_type.to_str() + '\n'
        s += self.root.to_str()
        return s


class _Node(object):
    @abstractmethod
    def to_str(self):
        pass


class Header(_Node):
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
            s += ' standalone="{}"'.format('yes' if self.standalone else 'no')
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
        if (tag and fromstr) or (not tag or not fromstr):
            raise InitError()
        if tag:
            self.tag = tag
            self._attrs = dict(attrs) if attrs else {}
            self._kids = list(kids) if kids else []
        else:


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
            _attrs_string_list.append('{}="{}"'.format(attr_name, attr_value))

        if _attrs_string_list:
            s += ' '
            s += ' '.join(_attrs_string_list)

        if self.kids:
            s += '>'
            for kid in self.kids:
                if isinstance(kid, Element):
                    s += kid.to_str()
                elif isinstance(kid, str):
                    s += _escape(kid)
            s += '</{}>'.format(self.tag)

        else:
            s += ' />'

        return s

    def find_attr(self, attr):
        for _attr, value in self.attrs.items():
            if _attr == attr:
                return value

    def find_kids(self, tag):
        kids = []
        for kid in self.kids:
            if isinstance(kid, Element) and kid.tag == tag:
                kids.append(kid)
        return kids


def _escape(string):
    s = ''
    for char in string:
        if char == '&':
            s += '&amp;'
        elif char == '<':
            s += '&lt;'
        elif char == '>':
            s += '&gt;'
        else:
            s += str(char)
    return s


def sub(element, tag, attrs=None, kids=None):
    sub_element = Element(tag, attrs, kids)
    element.kids.append(sub_element)
    return sub_element

def parse_element(xmlstr):

def parse(xmlstr):
    pass
    #todo
