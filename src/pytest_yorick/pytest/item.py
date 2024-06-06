import pytest
from _pytest.nodes import Node
import pathlib
from pytest_yorick.exceptions import BadSchemaError
from pytest_yorick.report import wrap_suite, wrap_chapter, wrap_subchapter
from pytest_yorick.runner import run_test
from pytest_yorick.utils.regexp_utils import regexp_search


class YamlItem(pytest.Item):
    """
    yamlItem class of all yaml test items.
    """
    def __init__(self, *, spec, **kwargs):
        super().__init__(**kwargs)
        self.spec = spec

    def runtest(self):
        """
        runtest will set hierarchy for beautiful allure report suites before running
        :return:
        """
        self._set_hierarchy()
        run_test(self.path, self.spec)

    def repr_failure(self, excinfo):  # noqa
        """Called when self.runtest() raises an exception."""
        return super().repr_failure(excinfo)

    def repr_failure(self, excinfo):  # noqa
        if isinstance(excinfo.value, BadSchemaError):
            return f"BadSchemaError: {excinfo.value}"
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.path, 0, f"case: {self.name}"

    @classmethod
    def yamlitem_from_parent(cls, name, parent: Node, spec, path: pathlib.Path):
        return cls.from_parent(parent, name=name, spec=spec, path=path)

    def add_markers(self, marks):
        for m in marks:
            if m.name == "usefixtures":
                pass
            self.add_marker(m)

    def _set_hierarchy(self):
        """
        refactor the structure in allure report
        :return:
        """
        suite = self._set_parent_suite()
        chapter = self._set_suite()
        subchapter = self._set_sub_suite()
        if suite:
            wrap_suite(suite)
        if chapter:
            wrap_chapter(chapter)
        if subchapter:
            wrap_subchapter(subchapter)

    def _set_parent_suite(self):
        pattern = r"ts-\d+-[\w-]+"
        match = regexp_search(pattern, str(self.path))
        if match:
            return match.group(0)
        return None

    def _set_suite(self):
        pattern = r"ch-\d+-[\w-]+"
        match = regexp_search(pattern, str(self.path))
        if match:
            return match.group(0)
        return None

    def _set_sub_suite(self):
        pattern = r"subch-\d+-[\w-]+"
        match = regexp_search(pattern, str(self.path))
        if match:
            return match.group(0)
        return None
