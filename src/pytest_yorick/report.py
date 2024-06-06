import logging

from pytest_yorick.utils.yaml_func import dump_yaml

logger: logging.Logger = logging.getLogger(__name__)

try:
    from allure import attach, step, title, suite, sub_suite
    from allure import dynamic
    from allure import attachment_type

    yaml_type = attachment_type.YAML
except ImportError:
    """
    Avoid errors caused by the absence of Allure installation
    """


    class MockAttachmentType:
        YAML = None


    class dynamic:  # noqa

        @staticmethod
        def parent_suite(name):
            pass

        @staticmethod
        def suite(name):
            pass

        @staticmethod
        def sub_suite(name):
            pass

        @staticmethod
        def parameter(name, param):
            pass


    attachment_type = MockAttachmentType
    yaml_type = attachment_type.YAML


    def attach(*args, **kwargs) -> None:
        pass


    def mock_func(step_func):
        return step_func


    def step(name):
        return mock_func


def wrap_step(allure_name: str, partial):
    return step(allure_name)(partial)


def attach_yaml(payload: dict, name: str) -> None:
    dumped = dump_yaml(payload)
    return attach_text(dumped, name, yaml_type)


def attach_text(payload, name: str, attach_type=None) -> None:
    return attach(payload, name=name, attachment_type=attach_type)


def wrap_suite(suite_name: str):
    dynamic.parent_suite(suite_name)


def wrap_chapter(chapter_name: str):
    dynamic.suite(chapter_name)


def wrap_subchapter(subchapter_name: str):
    dynamic.sub_suite(subchapter_name)


def wrap_parameter(param):
    dynamic.parameter("param", param)
