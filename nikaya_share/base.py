import dataclasses


@dataclasses.dataclass
class Info:
    # xml-p5a 目录中 “N07/N07n0004.xml” 之 “4”,
    serial: int | None
    # 汉语名
    name: str
    # 巴利语名
    pali: str
    # 译者
    translators: tuple[str, ...]
    # 缩写
    abbr: str = None
    # 原作者
    authors: tuple[tuple, ...] = None
