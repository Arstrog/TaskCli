import sys
import unittest
import tasker
import tempfile
import json
from pathlib import Path

class TestTasker(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def setUpClass(cls):

        cls.tmpdir = tempfile.mkdtemp(prefix="task_tests_")
        cls.data_dir = Path(cls.tmpdir)
        # cls.data_dir.mkdir(exist_ok=True)
        #happy path
        cls.task_path = cls.data_dir / "items_ok.json"
        data = {"1"}


    def tearDown(self) -> None:
        return super().tearDown()

    def setUp(self) -> None:
        return super().setUp()


    def test_add(self):
        pass

    def test_delete(self):
        pass

    def test_update(self):
        pass

    def test_list(self):
        pass

    def test_mark_in_progress(self):
        pass

    def test_mark_done(self):
        pass
