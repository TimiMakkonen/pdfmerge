# PDF merge

[![GitHub License](https://img.shields.io/github/license/TimiMakkonen/pdfmerge)](/LICENSE)
![GitHub Latest Release Tag](https://img.shields.io/github/v/tag/TimiMakkonen/pdfmerge)

Python script for merging PDFs on the command line.

## Table of contents

* [How to use](#how-to-use)
* [Version history](#version-history)
* [Fixes and features left to consider/implement](#fixes-and-features-left-to-considerimplement)

## How to use

```console
usage: pdfmerge.py [-h] [-o OUTFILE] inputfiles [inputfiles ...]

positional arguments:
  inputfiles            input PDF files to merge

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file of PDF merge, default='merged.pdf'
```

## Version history

### Version DEVELOP

* Fixed substantial bug which caused an error when trying to save merged
  pdf in the current directory.
* Added default value information of 'OUTFILE' to help message.
* Modified docstrings.
* Added shebang.
* Linted using default pylint.

### Version 0.1.0

* Script should work as expected.
* Expected usage manually tested.
* Edge cases related to file path names not guaranteed to work, but most
  likely will.

## Fixes and features left to consider/implement

* Add tests.
