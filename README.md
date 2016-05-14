# Reference Fixer

Written to convert in text citations such as:

* (Smith et al., 2016)
* Smith et al. (2016)
* Smith and Jones (2016)
* (Smith and Jones, 2016)
* Jones (2016)
* (Jones, 2016)

To latex format, eg `\citep{smith_title_2016}` by scraping a given bibtex file for
the corrext information. Needed to traslate a word manuscript into latex.

The code cannot discriminate between 2 papers by the same author in the same
year, eg `Smith (2012a; 2012b)` so will write the latex command as
`\citep{smith_???_2016}` making it easy to manually edit these. Does not perform
any tests that references are within the bibtex file and will fail if a
reference cannot be found.

Will fail on names with spaces in them and names with non letter characters
that are not inside parentheses. Surnames with lower case first letters will
cause problems for citations which are not within parentheses.

This works for my specific use case with little failure and might help someone
else in the future.

SWDG - May 2016
