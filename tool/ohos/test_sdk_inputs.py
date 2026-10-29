"""Ensure reviewed SDK patches still match the current application checkout.

This fast, read-only preflight detects upstream patch-script changes before
fetching the OHOS SDK or scheduling expensive native jobs.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
TOOL = Path(__file__).with_name("prepare_sdk.py")
SPEC = importlib.util.spec_from_file_location("ohos_sdk_prepare_inputs", TOOL)
prepare_sdk = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_sdk)


class SDKInputsTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(prepare_sdk.MANIFEST_PATH.read_text())

    def test_current_checkout_matches_every_reviewed_patch_input(self):
        patches = prepare_sdk.patch_inputs(ROOT, self.manifest)
        self.assertEqual(len(patches), len(self.manifest["patches"]))
        self.assertTrue(all(path.is_file() for path in patches))

    def test_changed_upstream_patch_driver_is_rejected(self):
        bad = dict(self.manifest, upstream_patch_driver_sha256="0" * 64)
        with self.assertRaisesRegex(prepare_sdk.PreparationError, "compatibility review"):
            prepare_sdk.patch_inputs(ROOT, bad)


if __name__ == "__main__":
    unittest.main()
