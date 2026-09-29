import unittest
from unittest.mock import patch, mock_open
from argparse import Namespace
import json
import sys

import tasker

class TestTaskerApp(unittest.TestCase):

    def setUp(self):
        
        self.db = {}

        
        self.sample_db = {
            "1": {
                "description": "Learn Python",
                "status": "todo",
                "createdAt": "01-01-2023:12:00:00",
                "updatedAt": "01-01-2023:12:00:00"
            }
        }

    @patch('sys.stdout')
    def test_add(self, mock_stdout):
        args = Namespace(description="Buy groceries")

        
        tasker.add(args, self.db)

        
        self.assertIn("1", self.db)
        self.assertEqual(self.db["1"]["description"], "Buy groceries")
        self.assertEqual(self.db["1"]["status"], "todo")
        self.assertIn("createdAt", self.db["1"])

    @patch('sys.stdout')
    def test_update(self, mock_stdout):
        self.db = self.sample_db.copy()

      
        args = Namespace(id=1, description="Learn Advanced Python", status="in-progress")

        tasker.update(args, self.db)

        self.assertEqual(self.db["1"]["description"], "Learn Advanced Python")
        self.assertEqual(self.db["1"]["status"], "in-progress")

    def test_delete_existing_task(self):
        self.db = self.sample_db.copy()
        args = Namespace(id=1)

        tasker.delete(args, self.db)

       
        self.assertNotIn("1", self.db)
        self.assertEqual(len(self.db), 0)



    @patch('sys.exit', side_effect=SystemExit)
    def test_delete_non_existent_task(self, mock_exit):
        self.db = self.sample_db.copy()
        args = Namespace(id=99)

       
        tasker.delete(args, self.db)
        mock_exit.assert_called_with("Task with id:99 does not exist.")

    @patch('sys.stdout')
    def test_mark_in_progress(self, mock_stdout):
        self.db = self.sample_db.copy()
        
        args = Namespace(id=1, description="Learn Python", status="in-progress")

        tasker.mark_in_progress(args, self.db)
        self.assertEqual(self.db["1"]["status"], "in-progress")

    @patch('sys.stdout')
    def test_mark_done(self, mock_stdout):
        self.db = self.sample_db.copy()
        args = Namespace(id=1, description="Learn Python", status="done")

        tasker.mark_done(args, self.db)
        self.assertEqual(self.db["1"]["status"], "done")

    @patch('sys.stdout')
    def test_list_all_tasks(self, mock_stdout):
        self.db = self.sample_db.copy()
        args = Namespace(status=None)

        tasker.list_task(args, self.db)

        self.assertTrue(mock_stdout.write.called)

    @patch('sys.stdout')
    def test_list_tasks_by_status(self, mock_stdout):
        self.db = {
            "1": {"description": "Task 1", "status": "todo", "createdAt": "", "updatedAt": ""},
            "2": {"description": "Task 2", "status": "done", "createdAt": "", "updatedAt": ""}
        }
        args = Namespace(status="done")

        tasker.list_task(args, self.db)
        self.assertTrue(mock_stdout.write.called)

    def test_save(self):
        mocked_open = mock_open()
        with patch('builtins.open', mocked_open):
            tasker.save("dummy_path.json", self.sample_db)

          
            mocked_open.assert_called_once_with("dummy_path.json", "w")

            handle = mocked_open()
            written_content = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertIn("Learn Python", written_content)

    def test_load_existing_file(self):
        mock_file_content = json.dumps(self.sample_db)
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            loaded_db = tasker.load("dummy_path.json")
            self.assertEqual(loaded_db, self.sample_db)

    def test_load_non_existent_file(self):
       
        with patch('builtins.open', side_effect=FileNotFoundError):
            loaded_db = tasker.load("dummy_path.json")
            self.assertEqual(loaded_db, {})

if __name__ == '__main__':
    unittest.main()
