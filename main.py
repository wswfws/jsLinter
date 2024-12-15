"""
Тут всё будет переписано
"""

import argparse
import json
import logging
import os
import sys

import esprima
from yaml import load as load_yaml, FullLoader

from checkers.correct_naming import check_for_correct_naming
from checkers.empty_lines import check_for_empty_lines
from checkers.missing_semicolons import check_for_missing_semicolons
from checkers.spaces_style import check_spaces_style
from config import CONFIG_PATH, CONFIG_ENCODING
from self_types.js_code import JsCode, JsCodeError, JsCodeWarning


class SimpleJSLinter:
    """
    Class for linting JavaScript code and reporting errors and warnings.

    Attributes:
        js_code (JsCode): The JavaScript code object to be linted.
        errors (list[JsCodeError]): List to store linting errors.
        warnings (list[JsCodeWarning]): List to store linting warnings.
    """

    def __init__(self, js_code: JsCode):
        self.js_code = js_code
        self.errors: list[JsCodeError] = []
        self.warnings: list[JsCodeWarning] = []

    def lint(self, **kwargs):
        """
        Lints the JavaScript code for errors.

        Args:
            **kwargs: Keyword arguments to specify which specific checks to run.
                      Pass 'missing_semicolons=True' to check for missing semicolons.
                      Pass 'empty_lines=True' to checking empty lines.
                      Pass 'all=True' to run all available checks.
        """

        checkers = kwargs.get('checkers', {})

        try:
            check_all = checkers.get("all", False)
            if check_all or checkers.get("missing_semicolons"):
                self.warnings.extend(check_for_missing_semicolons(self.js_code))
            if check_all or checkers.get("empty_lines"):
                self.warnings.extend(check_for_empty_lines(
                    self.js_code,
                    kwargs.get("max-code-line-without-empty-lines", 9)
                ))
            if check_all or checkers.get("spaces_style"):
                self.warnings.extend(check_spaces_style(
                    self.js_code,
                    kwargs.get("spaces-style", {})
                ))
            if check_all or checkers.get("correct_naming"):
                self.warnings.extend(check_for_correct_naming(
                    self.js_code,
                    kwargs.get("naming-patterns", {})
                ))
        except esprima.Error as e:
            print(f"Parsing error: {e.message}")

    def report(self):
        """Reports the linting errors and warnings found in the JavaScript code."""
        if not self.errors and not self.warnings:
            print("No linting errors found!")
        else:
            for error in self.errors:
                print(error)
            for warning in self.warnings:
                print(warning)


def parse_arguments(args: str):
    parser = argparse.ArgumentParser(description="JavaScript Linter")
    parser.add_argument('--files', nargs='+', help="Paths to JavaScript files to lint")
    parser.add_argument('--directories', nargs='+', help="Directories containing JavaScript files to lint")
    parser.add_argument('--config', type=str, default=CONFIG_PATH,
                        help=f"Path to the configuration file (default: {CONFIG_PATH})")
    return parser.parse_args(args)


def get_files_from_directories(directories):
    js_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.js'):
                    js_files.append(os.path.join(root, file))
    return js_files


logger = logging.getLogger(__name__)


def main():
    args = parse_arguments(sys.argv[1:])

    if not args.files and not args.directories:
        logger.error("No files or directories specified, type -h to see usage")
        return

    try:
        with open(args.config, 'r', encoding=CONFIG_ENCODING) as f:
            config = load_yaml(f, Loader=FullLoader)

        files_to_lint = args.files or []

        if args.directories:
            files_to_lint.extend(get_files_from_directories(args.directories))

        for file_path in files_to_lint:
            try:
                with open(file_path, 'r', encoding=CONFIG_ENCODING) as f:
                    code = JsCode(f.read(), file_path)

                linter = SimpleJSLinter(code)
                linter.lint(**config)
                linter.report()

            except FileNotFoundError as e:
                logger.error(f"File not found: {file_path}")
            except Exception as e:
                logger.error(f"Error linting file {file_path}: {e}")

    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

"""
python ./main.py --directories ./
python ./main.py --files .\\test2.js .\\test1.js
"""
