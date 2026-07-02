"""
BTC Trend Trader Professional v4
Persistence Tests
"""

import os
import tempfile
import unittest

from persistence.persistence_manager import PersistenceManager


class TestPersistenceManager(unittest.TestCase):

    def setUp(self):

        self.manager = PersistenceManager()

        self.test_data = {
            "balance": 10000,
            "equity": 10150,
            "positions": [],
        }

        self.temp_dir = tempfile.TemporaryDirectory()

        self.state_file = os.path.join(
            self.temp_dir.name,
            "state.json",
        )

        self.backup_file = os.path.join(
            self.temp_dir.name,
            "backup.json",
        )

        self.restore_file = os.path.join(
            self.temp_dir.name,
            "restore.json",
        )

    def tearDown(self):

        self.temp_dir.cleanup()

    def test_save(self):

        result = self.manager.save(
            self.test_data,
            self.state_file,
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.state_file))

    def test_load(self):

        self.manager.save(
            self.test_data,
            self.state_file,
        )

        data = self.manager.load(
            self.state_file,
        )

        self.assertEqual(
            data["balance"],
            10000,
        )

    def test_backup(self):

        self.manager.save(
            self.test_data,
            self.state_file,
        )

        result = self.manager.backup(
            self.state_file,
            self.backup_file,
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.backup_file))

    def test_recovery(self):

        self.manager.save(
            self.test_data,
            self.state_file,
        )

        self.manager.backup(
            self.state_file,
            self.backup_file,
        )

        result = self.manager.recover(
            self.backup_file,
            self.restore_file,
        )

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.restore_file))


if __name__ == "__main__":
    unittest.main()