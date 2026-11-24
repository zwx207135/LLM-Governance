import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from experiments.package_c_handoff import verify_archive


class HandoffPackageTests(unittest.TestCase):
    def test_archive_manifest_detects_modified_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "handoff.zip"
            manifest = {"stage": "test", "files": {"file.txt": hashlib.sha256(b"correct").hexdigest()}}
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("file.txt", b"wrong")
                archive.writestr("C_RELEASE_MANIFEST.json", json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify_archive(path)

    def test_archive_manifest_covers_all_payload_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "handoff.zip"
            manifest = {"stage": "test", "files": {"file.txt": hashlib.sha256(b"correct").hexdigest()}}
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("file.txt", b"correct")
                archive.writestr("C_RELEASE_MANIFEST.json", json.dumps(manifest))
            self.assertEqual(verify_archive(path)["verified_files"], 1)


if __name__ == "__main__":
    unittest.main()
