# Taiping Yulan demonstration corpus

These 1,000 XML files were downloaded from the numbered volume pages of
[Wikisource's 太平御覽](https://zh.wikisource.org/wiki/太平御覽) and converted
with `scripts/download_taiping_yulan.py`.

The files use the workshop's deliberately simple TEI structure: one `<p>` per
source entry, with book titles between `《` and `》` represented as `<title>`.
Wikisource navigation, links, and editorial templates/notes are omitted. This
is suitable for demonstrating corpus-scale counting, not for producing a
scholarly critical edition.
