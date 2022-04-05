
### 使用 KOReader 阅读 EPUB
测试中发现 KOReader（2022.03版） 不支持使用多个 @font-face 定义相同名称的字体以实现类似字体合并的功能，
所以 html 中除了 h1-h6 等标题之外，使用了三个 class 属性标记字符，
其中 **cjk** 标记了汉字日文和全角符号等，
**lat** 标记了英文和半角符号等，
**tib** 标记了藏文。

**cjk** 繁体字体 NotoSerifCJKtc-Regular.otf，简体字体 NotoSerifCJKsc-Regular.otf

**lat** 使用字体 NotoSerif-Light.otf

**tib** NotoSerifTibetan-Regular.otf

**标题** 繁体字体 NotoSansCJKtc-Medium.otf 简体字体 NotoSansCJKsc-Medium.otf

[Noto CJK字体下载链接](https://github.com/googlefonts/noto-cjk)

[Noto 其它字体下载链接](https://github.com/googlefonts/noto-fonts)

