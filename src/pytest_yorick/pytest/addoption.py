import pytest
from pathlib import Path
from typing import List, Optional, TypeVar, Union


def add_parser_options(parser_addoption) -> None:
    parser_addoption(
        '--suite',
        help="One or more suites to include in every test: ts-01 ts-02",
        nargs="+",
    )
    parser_addoption(
        '--chapter',
        help="One or more chapters to include in every test: ch-01 ch-02",
        nargs="+",
    )
    parser_addoption(
        '--subchapter',
        help="One or more subchapter to include in every test: subch-01 subch-02",
        nargs="+",
    )
    parser_addoption(
        '--case',
        help="One or more case to include in every test: tc-01 tc-02",
        nargs="+",
    )
    parser_addoption(
        "--clean-allure",
        action="store_true",
        default=False,
        help="Clean allure results directory before running tests"
    )

def add_ini_options(parser: pytest.Parser) -> None:
    parser.addini(
        'suite',
        help="One or more suites to include in every test: ts-01 ts-02",
        type="linelist",
        default=[],
    )
    parser.addini(
        'chapter',
        help="One or more chapters to include in every test: ch-01 ch-02",
        type="linelist",
        default=[],
    )
    parser.addini(
        'subchapter',
        help="One or more subchapter to include in every test: subch-01 subch-02",
        type="linelist",
        default=[],
    )
    parser.addini(
        'case',
        help="One or more case to include in every test: tc-01 tc-02",
        type="linelist",
        default=[],
    )


T = TypeVar("T", bound=Optional[Union[str, List, List[Path], List[str], bool]])


def get_option_generic(
        pytest_config: pytest.Config,
        flag: str,
        default: T,
) -> T:
    """Get a configuration option or return the default

    Priority order is cmdline, then ini, then default"""
    cli_flag = flag.replace("-", "_")
    ini_flag = flag

    # Lowest priority
    use = default

    # Middle priority
    if pytest_config.getini(ini_flag) is not None:
        use = pytest_config.getini(ini_flag)

    # Top priority
    if pytest_config.getoption(cli_flag) is not None:
        use = pytest_config.getoption(cli_flag)

    return use


def check_filter(pytest_config: pytest.Config) -> bool:
    if pytest_config.getoption("suite"):
        return True
    elif pytest_config.getoption("chapter"):
        return True
    elif pytest_config.getoption("subchapter"):
        return True
    elif pytest_config.getoption("case"):
        return True
    return False
