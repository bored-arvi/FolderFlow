import unittest
from pathlib import Path
import shutil
from file_organizer import move_file, file_hash, generate_new_name

class TestDuplicateHandlingOnRoot(unittest.TestCase):
    ROOT_TEST_DIR = Path("C:/Users/aravi/FolderFlow/test folder")

    @classmethod
    def setUpClass(cls):
        # Clean up any previous test folder
        if cls.ROOT_TEST_DIR.exists():
            shutil.rmtree(cls.ROOT_TEST_DIR)
        cls.ROOT_TEST_DIR.mkdir(parents=True)

        # Original file
        (cls.ROOT_TEST_DIR / "file1.txt").write_text("Hello World")
        # Duplicate content
        (cls.ROOT_TEST_DIR / "file1_dup.txt").write_text("Hello World")
        # File with same name but different content
        (cls.ROOT_TEST_DIR / "file2.txt").write_text("Different Content")
        documents_dir = cls.ROOT_TEST_DIR / "Documents"
        documents_dir.mkdir()
        (documents_dir / "file2.txt").write_text("Existing Content")
        cls.documents_dir = documents_dir

    @classmethod
    def tearDownClass(cls):
        # Optional: Comment this out if you want to inspect files manually
        # shutil.rmtree(cls.ROOT_TEST_DIR)
        pass

    def test_duplicate_file_skipped(self):
        src = self.ROOT_TEST_DIR / "file1_dup.txt"
        dest = self.ROOT_TEST_DIR / "file1.txt"
        result = move_file(str(src), str(dest))
        self.assertFalse(result)

    def test_file_renamed_on_name_conflict(self):
        src = self.ROOT_TEST_DIR / "file2.txt"
        dest = self.documents_dir / "file2.txt"
        result = move_file(str(src), str(dest))
        self.assertTrue(result)
        renamed_files = list(self.documents_dir.glob("file2(*).txt"))
        self.assertTrue(len(renamed_files) > 0)

if __name__ == "__main__":
    unittest.main()
