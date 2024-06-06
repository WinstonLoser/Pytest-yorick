import os
from pathlib import Path
import pytest
from .addoption import add_parser_options, get_option_generic, add_ini_options, check_filter
from .file import YamlFile
from ..exceptions import CompileError
from ..utils.regexp_utils import regexp_compile, regexp_match

"""
The global param for pytest_ignore_collect func
"""
has_filter = False


def pytest_addoption(parser: pytest.Parser) -> None:
    add_parser_options(parser.addoption)
    add_ini_options(parser)


def pytest_configure(config: pytest.Config):
    """
    Try to get filters from config, set has_filter to True if filter gotten
    """
    if check_filter(config):
        global has_filter
        has_filter = True


def pytest_collect_file(parent, file_path: Path):
    """
    filter yaml files with config value
    """
    if not _filter_cases_by_pattern(parent.config, "suite", file_path):
        return None
    if not _filter_cases_by_pattern(parent.config, "chapter", file_path):
        return None
    if not _filter_cases_by_pattern(parent.config, "subchapter", file_path):
        return None
    if not _filter_cases_by_pattern(parent.config, "case", file_path):
        return None
    if file_path.suffix == ".yml":
        pattern = r"tc-\d+-[a-zA-Z0-9-]+\.yml$"
        compiled = regexp_compile(pattern)
        match_tavern_file = compiled.search
        if match_tavern_file(str(file_path)):
            return YamlFile.from_parent(parent, path=file_path)
    return None


def pytest_ignore_collect(collection_path: Path):
    """
    pytest will ignore .py files if the has_filter is True
    """
    if has_filter and collection_path.suffix == ".py":
        return True
    return False


def _filter_cases_by_pattern(config: pytest.Config, flag, path: os.PathLike) -> bool:
    """
    To filter the case by flags, matching with case path
    :param flag: flag can be suite, chapter, subchapter
    :return:
    """
    nodes = get_option_generic(config, flag, None)
    if isinstance(nodes, list) and nodes:
        for node in nodes:
            if flag == "suite":
                matched_file = _matched_suite(node)
            elif flag == "chapter":
                matched_file = _matched_chapter(node)
            elif flag == "subchapter":
                matched_file = _matched_subchapter(node)
            else:
                matched_file = _matched_case(node)
            if matched_file(str(path)):
                return True
        return False
    return True


def _matched_suite(suite: str):
    if regexp_match(r"^ts-\d+$", suite):
        pattern = fr"\\{suite}-\w*"
    elif regexp_match(r"^ts-\d+-.*$", suite):
        pattern = fr"\\{suite}"
    else:
        raise CompileError(f"Invalid --suite pattern: {suite}")
    compiled = _try_compile(pattern)
    return compiled.search


def _matched_chapter(chapter: str):
    if regexp_match(r"^ch-\d+$", chapter):
        pattern = fr"\\{chapter}-\w*"
    elif regexp_match(r"^ch-\d+-.*$", chapter):
        pattern = fr"\\{chapter}"
    else:
        raise CompileError(f"Invalid --chapter pattern: {chapter}")
    compiled = _try_compile(pattern)
    return compiled.search


def _matched_subchapter(subchapter: str):
    if regexp_match(r"^subch-\d+$", subchapter):
        pattern = fr"\\{subchapter}-\w*"
    elif regexp_match(r"^subch-\d+-.*$", subchapter):
        pattern = fr"\\{subchapter}"
    else:
        raise CompileError(f"Invalid --subchapter pattern: {subchapter}")
    compiled = _try_compile(pattern)
    return compiled.search


def _matched_case(case: str):
    if regexp_match(r"^tc-\d+$", case):
        pattern = fr"\\{case}-\w*"
    elif regexp_match(r"^tc-\d+-.*$", case):
        pattern = fr"\\{case}"
    else:
        raise CompileError(f"Invalid --case pattern: {case}")
    compiled = _try_compile(pattern)
    return compiled.search


def _try_compile(pattern):
    try:
        compiled = regexp_compile(pattern)
    except Exception as e:
        raise CompileError(f"Fail to compile filter pattern: {e}") from e
    return compiled
