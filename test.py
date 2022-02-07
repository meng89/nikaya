#!/usr/bin/env python3
from pybtex.database import BibliographyData, Entry

bib_data = BibliographyData(
        {
            "misc": Entry("1123", [
                ("note", "\\sfsf{xxxbbb}")
            ])
        }
    )
print(bib_data.to_string("bibtex"))
