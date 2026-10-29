"""Guard Goodwu HDR capability utilities against upstream quality model refactors."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "lib/models/common/video/base_quality.dart"
PART = ROOT / "lib/models/common/video/video_quality.dart"
CONSUMERS = (
    ROOT / "lib/utils/codec_capability.dart",
    ROOT / "lib/utils/hdr_source_hint.dart",
)


class QualityPartImports(unittest.TestCase):
    def test_base_library_owns_video_quality_type(self):
        self.assertIn("part 'video_quality.dart';", BASE.read_text())
        self.assertIn("part of 'base_quality.dart';", PART.read_text())
        for file in CONSUMERS:
            body = file.read_text()
            self.assertIn("models/common/video/base_quality.dart", body, file.name)
            self.assertNotIn("import 'package:PiliPlus/models/common/video/video_quality.dart'", body, file.name)


if __name__ == "__main__":
    unittest.main()
