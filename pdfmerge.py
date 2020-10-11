#!/usr/bin/env python3
"""Python script for merging PDFs on the command line.

Usage:
    pdfmerge.py [-h] [-o OUTFILE] inputfiles [inputfiles ...]

License:
    MIT License

    Copyright (c) 2020 Timi Makkonen

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import argparse
import os

# noinspection PyPackageRequirements
import fitz  # used for reading and writing PDF files
from pathvalidate.argparse import validate_filepath_arg

MAX_NUM_OF_RENAME_ATTEMPTS = 20
DEFAULT_MERGE_OUTPUT_FILE_NAME = "merged.pdf"


class TooManyRenameAttemptsError(Exception):
    """Error that occurs if trying to rename a file too many times."""

    def __init__(self, num_of_rename_attempts, file_name) -> None:
        super().__init__(
            f"maximum number of renaming attempts ({num_of_rename_attempts}) for '{file_name}' "
            "has been exceeded.")
        self.num_of_rename_attempts = num_of_rename_attempts
        self.file_name = file_name


def merge_pdfs(outfile, pdf_files):
    """Merges given PDF files into one PDF file.

    :param pdf_files: PDF files to merge
    :param outfile: Merged PDF file
    """

    result_pdf = fitz.Document()

    # reads pdf files
    for pdf_file in pdf_files:
        with fitz.Document(pdf_file) as pdf_doc:
            result_pdf.insertPDF(pdf_doc)

    # creates directories needed to write the outfile (if needed)
    # os.path.normpath() used to turn "" (empty string) directory path to "."
    # manually checking for "" and turning into "." would also work
    # https://bugs.python.org/issue33968
    os.makedirs(os.path.normpath(os.path.dirname(outfile)), exist_ok=True)

    result_pdf.save(outfile)


def rename_file_if_necessary(file, default_file_name, max_num_of_rename_attempts):
    """Tries to rename a file if necessary.

    If given a directory file, appends 'default_file_name' to it.
    If given a file name that already exists, tries concatenate a number to it,
    up to 'max_num_of_rename_attempts' times.

    :param file: File path/name to modify
    :param default_file_name: Default file name to append to path if 'file' argument is a directory
    :param max_num_of_rename_attempts: Maximum number of rename attempts before raising an error
    :return: Renamed file
    :raises: TooManyRenameAttemptsError: If trying to rename file too many times
    """

    # if file is a directory, append default_file_name to path
    if os.path.basename(file) == '':
        file += default_file_name

    file = concat_num_to_file_name_if_necessary(file, max_num_of_rename_attempts)

    return file


def concat_num_to_file_name_if_necessary(file, max_num_of_rename_attempts):
    """Concatenates file name with a number if a file with same name already exists.

    :param file: File path/name to modify if the path/name already exists
    :param max_num_of_rename_attempts: Maximum number of rename attempts before raising an error
    :return: Renamed file path/name
    :raises: TooManyRenameAttemptsError: If trying to rename file too many times
    """

    renamed_file = file
    if os.path.exists(renamed_file):
        file_dirname, file_basename = os.path.split(renamed_file)
        file_basename_first_part, *file_basename_rest_parts = file_basename.split('.')
        num_of_rename_attempts = 0
        while os.path.exists(renamed_file):
            num_of_rename_attempts += 1

            if num_of_rename_attempts > max_num_of_rename_attempts:
                raise TooManyRenameAttemptsError(max_num_of_rename_attempts, file)

            renamed_file = os.path.join(file_dirname,
                                        '.'.join([file_basename_first_part + str(
                                            num_of_rename_attempts)] + file_basename_rest_parts))

    return renamed_file


def parse_arguments():
    """Parses command line arguments using argparse.ArgumentParser().

    :return: Parsed arguments
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("inputfiles", nargs='+', type=validate_filepath_arg,
                        help="input PDF files to merge")
    parser.add_argument("-o", "--outfile", type=validate_filepath_arg,
                        help="output file of PDF merge (default: %(default)s)\n"
                             "When directory (with ending slash, eg. 'my_dir/')\n"
                             "is given as an argument, default named output is\n"
                             "created in the given directory\n"
                             "(eg. 'my_dir/default_file_name').",
                        default=DEFAULT_MERGE_OUTPUT_FILE_NAME)

    return parser.parse_args()


def print_argument_details(argparse_args):
    """Prints given arguments in pretty format.

    :param argparse_args: Parsed arguments
    """

    print("inputfiles:")
    for arg in argparse_args.inputfiles:
        print(f"\t{arg}")

    print(f"outfile: {argparse_args.outfile}")


if __name__ == '__main__':
    args = parse_arguments()
    print_argument_details(args)

    try:
        renamed_outfile = rename_file_if_necessary(args.outfile, DEFAULT_MERGE_OUTPUT_FILE_NAME,
                                                   MAX_NUM_OF_RENAME_ATTEMPTS)

        merge_pdfs(outfile=renamed_outfile, pdf_files=args.inputfiles)
    except TooManyRenameAttemptsError as error:
        print(f"error: {error}")
