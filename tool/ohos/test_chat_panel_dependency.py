"""Check the pinned OHOS chat panel constructor matches the App dependency lock."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]


class ChatPanelDependencyContract(unittest.TestCase):
    def test_ohos_recipe_matches_current_chat_bottom_container_lock(self):
        recipe = json.loads((ROOT / "tool/ohos/dependencies.json").read_text())
        lock = (ROOT / "pubspec.lock").read_text()
        match = re.search(
            r"(?ms)^  chat_bottom_container:\n"
            r"(?:(?!^  [A-Za-z_][A-Za-z_0-9]*:).)*?"
            r"^      resolved-ref: ([0-9a-f]{40})$",
            lock,
        )
        self.assertIsNotNone(match, "Current App lock lacks chat_bottom_container Git SHA")
        selected = recipe["repositories"]["chat_bottom_container"]["git"]["ref"]
        self.assertEqual(selected, match.group(1),
                         "Upstream chat panel constructor API differs from OHOS compatibility dependency")

    def test_new_panel_constructor_args_preserved_in_upstream_app(self):
        source = (ROOT / "lib/pages/common/publish/common_publish_page.dart").read_text()
        self.assertIn("currentPanelType:", source)
        self.assertIn("data:", source)


if __name__ == "__main__":
    unittest.main()
