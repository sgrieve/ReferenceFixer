# -*- coding: utf-8 -*-
'''
Written to convert in text citations such as:

(Smith et al., 2016)
Smith et al. (2016)
Smith and Jones (2016)
(Smith and Jones, 2016)
Jones (2016)
(Jones, 2016)

To latex format, eg \citep{smith_title_2016} by scraping a given bibtex file for
the corrext information. Needed to traslate a word manuscript into latex.

The code cannot discriminate between 2 papers by the same author in the same
year, eg Smith (2012a; 2012b) so will write the latex command as
\citep{smith_???_2016} making it easy to manually edit these. Does not perform
any tests that references are within the bibtex file and will fail if a
reference cannot be found.

Will fail on names with spaces in them and names with non letter characters
that are not inside parentheses. Surnames with lower case first letters will
cause problems for citations which are not within parentheses.

This works for my specific use case with little failure and might help someone
else in the future.

SWDG - May 2016
'''
import re
import sys


def ProcessBibtex(filename):
    '''
    Build a dictionary of bibtex citation titles, keyed with the tuple
    (Author, Year)
    '''
    with open(filename, 'r') as f:
        raw_refs = f.readlines()

    Refs = []
    RefDict = {}

    for r in raw_refs:
        if '@article{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())
        elif '@inproceedings{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())
        elif '@incollection{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())
        elif '@book{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())
        elif '@misc{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())
        elif '@techreport{' in r:
            Refs.append(r.split('{')[1].split('}')[0].strip())

    for R in Refs:
        split = R.split('_')
        RefDict[(split[0], split[2].strip(','))] = split[1]

    return RefDict


def ReadCiteP(unformatted, references):
    '''
    Given a the contents of an unformatted bracketed citation, find all the
    references and replace them with valid latex in text citations.

    '''
    outputlist = []

    for i in unformatted:
        name = re.match('^.+?(?=,|(\set al)|(\sand\s))', i).group(0)
        year = re.search('\d\d\d\d[a-z]?', i).group(0)

        if len(year) == 4:
            outputlist.append(name + '_' + references[name, year] + '_' + year)

        else:
            outputlist.append(name + '_???_' + year)

    return '\citep{' + ', '.join(outputlist) + '}'


def ProcessCitep(bibDict, text):
    '''
    Given a string of unformatted text, find all the references in brackets and
    replace them with valid latex citations.
    '''
    #  http://stackoverflow.com/a/16826935/1627162
    author = "(?:[A-Z][A-Za-z'`-]+)"
    etal = "(?:et al.?)"
    additional = "(?:,? (?:(?:and |& )?" + author + "|" + etal + "))"
    year_num = "(?:18|19|20)[0-9][0-9][a-z]?"
    year = "(?:, *" + year_num + "| *\(" + year_num + "\))"
    regex = "(" + author + additional + "*" + year + ")"

    refs = re.findall('\(([^\d].*?\d\d\d\d[a-z]?)\)', text)

    replaceList = []

    for r in refs:
        matches = re.findall(regex, r)
        matches = [m.lower() for m in matches]
        replaceList.append(ReadCiteP(matches, bibDict))

    for i in range(len(replaceList)):
        text = re.sub('\(([^\d].*?\d\d\d\d[a-z]?)\)', replaceList[i],
                      text, count=1)
    return text


def ProcessCiteT(text, references):
    '''
    Given a string of unformatted text, find all the in text references and
    replace them with valid latex in text citations.
    '''
    # (\w+ et al. \(\d\d\d\d[a-z]?\))  gets et al. citet refs
    # (\w+ and \w+ \(\d\d\d\d[a-z]?\))   gets X and Y citet refs
    # ([A-z][a-z]+\s\(\d\d\d\d[a-z]?\))' inline citations, fails on jr. and o'

    citationRE = re.compile('(\w+\set\sal.\s\(\d\d\d\d[a-z]?\))|(\w+\sand\s\w+'
                            '\s\(\d\d\d\d[a-z]?\))|([A-z][a-z]+\s\(\d\d\d\d'
                            '[a-z]?\))')
    cites = re.findall(citationRE, text)
    outputlist = []
    for c in cites:
        citation = ''.join(c).lower()

        name = citation.split(' ')[0]
        year = re.search('\d\d\d\d[a-z]?', citation).group(0)

        if len(year) == 4:
            outputlist.append('\citet{' + name + '_' +
                              references[name, year] + '_' + year + '}')

        else:
            outputlist.append('\citet{' + name + '_???_' + year + '}')

    for i in range(len(outputlist)):
        text = re.sub(citationRE, outputlist[i],
                      text, count=1)
    return text


def LoadInput(input):
    '''
    Load the input file as a string.
    '''
    with open(input, 'r') as f:
        return f.read().strip()


def WriteOutput(output, text):
    '''
    Write the edited string to the output file.
    '''
    with open(output, 'w') as f:
        f.write(text)


def Run(bibFile, input, output):
    '''
    Wrapper to process references.
    '''

    text = LoadInput(input)
    bibDict = ProcessBibtex(bibFile)
    newtext = ProcessCitep(bibDict, text)

    OutputToWrite = ProcessCiteT(newtext, bibDict)
    WriteOutput(output, OutputToWrite)

    print '\nDone.\n'

if __name__ == "__main__":
    if len(sys.argv) == 4:
        Run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        sys.exit('\n{} needs 3 arguments:\n\n'
                 '[1] The name of the bibtex file\n'
                 '[2] The name of the input text file\n'
                 '[3] The output filename\n'.format(sys.argv[0]))
