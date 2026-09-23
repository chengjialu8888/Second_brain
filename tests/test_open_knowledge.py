"""Regression checks for evidence boundaries and portable knowledge exchange."""

import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from knowledge import content_hash, freshness, pages, read_page, verification, window_status, write_page
from knowledge_bundle import catalog, export_bundle, validate_bundle
import workspace_compose


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "brain"
        self.root.mkdir()
        self.out = Path(self.temp.name) / "bundle"
        self.start = dt.date(2026, 8, 1)
        self.end = dt.date(2026, 8, 31)

    def page(self, name="concepts/demo.md", meta=None, body="\n# Demo\n\nEvidence.\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(write_page(meta if meta is not None else {
            "type": "concept", "title": "Demo", "description": "Short evidence summary.",
            "visibility": "public", "status": "active",
        }, body), encoding="utf-8")
        return path

    def test_capture_and_edit_dates_do_not_qualify_event(self):
        meta = {"captured_at": "2026-08-10", "updated": "2026-08-10"}
        self.assertEqual(window_status(meta, self.start, self.end), "unknown")

    def test_retrospective_vs_known_by(self):
        meta = {"event_date": "2026-08-20", "published_at": "2026-09-01"}
        self.assertEqual(window_status(meta, self.start, self.end), "inside")
        self.assertEqual(window_status(meta, self.start, self.end, "known-by", self.end), "after-cutoff")
        self.assertEqual(window_status(meta, self.start, self.end, "published"), "outside")

    def test_known_by_requires_publication(self):
        self.assertEqual(window_status({"event_date": "2026-08-20"}, self.start, self.end, "known-by", self.end), "unknown")

    def test_calendar_boundaries_and_invalid_date(self):
        for value in (self.start, self.end, "2026-08-31T23:59:00+08:00"):
            self.assertEqual(window_status({"event_date": value}, self.start, self.end), "inside")
        self.assertEqual(window_status({"event_date": "2026-08-99"}, self.start, self.end), "unknown")

    def test_content_change_invalidates_review(self):
        meta, body = read_page(self.page())
        meta["verified"] = [{"by": "human:reviewer", "at": "2026-08-22T10:00:00Z", "content_sha256": content_hash(meta, body)}]
        self.assertEqual(verification(meta, body), "human-reviewed")
        self.assertEqual(verification(meta, body + "Changed claim"), "needs-review")
        meta["event_date"] = "2026-08-22"
        self.assertEqual(verification(meta, body), "needs-review")

    def test_review_mapping_and_unbound_import(self):
        meta, body = read_page(self.page())
        meta["verified"] = {"by": "process:test", "at": "2026-08-22T00:00:00Z", "content_sha256": content_hash(meta, body)}
        self.assertEqual(verification(meta, body), "machine-confirmed")
        del meta["verified"]["content_sha256"]
        self.assertEqual(verification(meta, body), "needs-review")

    def test_freshness_is_separate_from_review(self):
        now = dt.datetime(2026, 9, 23, tzinfo=dt.timezone.utc)
        self.assertEqual(freshness({"stale_after": "2026-09-23T08:00:00+08:00"}, now), "stale")
        self.assertEqual(freshness({"stale_after": "2026-09-24T00:00:00Z"}, now), "fresh")
        self.assertEqual(freshness({"stale_after": "2026-09-24"}, now), "unknown")

    def test_catalog_does_not_inject_body(self):
        self.page(body="\n# Demo\n\nBODY-ONLY-DETAIL\n")
        result = catalog(self.root)
        self.assertIn("Short evidence summary", result)
        self.assertNotIn("BODY-ONLY-DETAIL", result)
        self.assertEqual(catalog(self.root, "BODY-ONLY-DETAIL"), "No matching metadata.")

    def test_discovery_excludes_generated_context(self):
        for folder in ("sources", "workspace", "templates", "inbox", ".hidden"):
            self.page(f"{folder}/secret.md")
        self.page()
        self.assertEqual(len(list(pages(self.root))), 1)
        self.assertEqual(len(list(pages(self.root, True))), 2)

    def test_export_preserves_unknown_fields_and_maps_status(self):
        path = self.page(meta={"type": "custom-type", "visibility": "public", "status": "paused", "knowledge_status": "stable", "custom": {"nested": 42}})
        before = path.read_bytes()
        export_bundle(self.root, ["concepts/demo.md"], self.out)
        meta, _ = read_page(self.out / "concepts/demo.md")
        self.assertEqual(meta["sb_status"], "paused")
        self.assertEqual(meta["status"], "stable")
        self.assertEqual(meta["custom"], {"nested": 42})
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(validate_bundle(self.out), [])

    def test_export_does_not_reuse_old_verification(self):
        self.page(meta={"type": "concept", "visibility": "public", "verified": {"by": "human:test", "at": "2026-08-01T00:00:00Z"}})
        export_bundle(self.root, ["concepts/demo.md"], self.out)
        meta, _ = read_page(self.out / "concepts/demo.md")
        self.assertNotIn("verified", meta)
        self.assertIn("sb_verification_history", meta)
        self.assertEqual(meta["status"], "draft")

    def test_export_selection_does_not_follow_links(self):
        self.page(body="\n# Demo\n\n[Private](../people/private.md)\n")
        self.page("people/private.md", {"type": "person"})
        export_bundle(self.root, ["concepts/demo.md"], self.out)
        self.assertFalse((self.out / "people/private.md").exists())
        self.assertEqual(json.loads((self.out / "manifest.json").read_text())["pages"], ["concepts/demo.md"])

    def test_export_requires_explicit_public(self):
        self.page(meta={"type": "concept"})
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["concepts/demo.md"], self.out)
        self.assertFalse(self.out.exists())

    def test_export_checks_all_pages_before_writing(self):
        self.page()
        self.page("concepts/private.md", {"type": "concept", "visibility": "private"})
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["concepts/demo.md", "concepts/private.md"], self.out)
        self.assertFalse(self.out.exists())

    def test_export_rejects_raw_sources_and_traversal(self):
        for name in ("sources/raw.md", "workspace/draft.md", "diary/day.md", "../escape.md", "/tmp/escape.md"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                export_bundle(self.root, [name], self.out)

    def test_export_rejects_symlink_escape(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("private", encoding="utf-8")
        (self.root / "escape.md").symlink_to(outside)
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["escape.md"], self.out)

    def test_export_cannot_alias_raw_sources_through_directory_symlink(self):
        self.page("sources/private.md")
        (self.root / "alias").symlink_to(self.root / "sources", target_is_directory=True)
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["alias/private.md"], self.out)

    def test_export_refuses_overwrite(self):
        self.page()
        export_bundle(self.root, ["concepts/demo.md"], self.out)
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["concepts/demo.md"], self.out)

    def test_export_rejects_wikilinks(self):
        self.page(body="\n# Demo\n[[other]]\n")
        with self.assertRaises(ValueError):
            export_bundle(self.root, ["concepts/demo.md"], self.out)

    def test_minimal_unknown_type_is_valid_okf(self):
        self.page(meta={"type": "unknown-custom-type"})
        self.assertEqual(validate_bundle(self.root), [])

    def test_validator_rejects_untyped_markdown(self):
        (self.root / "README.md").write_text("# Untyped\n", encoding="utf-8")
        self.assertTrue(validate_bundle(self.root))

    def test_invalid_yaml_reports_path(self):
        path = self.root / "bad.md"
        path.write_text("---\ntype: [invalid\n---\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "bad.md"):
            read_page(path)
        self.page()
        self.assertIn("Invalid frontmatter", catalog(self.root))
        self.assertIn("Short evidence summary", catalog(self.root))

    def test_workspace_does_not_use_filename_dates(self):
        self.page("concepts/2026-08-20-demo.md")
        with patch.object(workspace_compose, "BRAIN", self.root), patch.object(workspace_compose, "ROOT", self.root.parent):
            hits = workspace_compose.search("Demo", 1, self.start, self.end)
        self.assertEqual(hits[0].window_status, "unknown")

    def test_outside_high_score_does_not_crowd_out_inside(self):
        self.page("concepts/old.md", {"event_date": "2025-01-01"}, "Demo " * 100)
        self.page("concepts/current.md", {"event_date": "2026-08-20"}, "Demo")
        with patch.object(workspace_compose, "BRAIN", self.root), patch.object(workspace_compose, "ROOT", self.root.parent):
            hits = workspace_compose.search("Demo", 1, self.start, self.end)
        self.assertEqual([h.window_status for h in hits], ["inside", "outside"])

    def test_unknown_high_score_does_not_crowd_out_inside(self):
        self.page("concepts/undated.md", {}, "Demo " * 100)
        self.page("concepts/current.md", {"event_date": "2026-08-20"}, "Demo")
        with patch.object(workspace_compose, "BRAIN", self.root), patch.object(workspace_compose, "ROOT", self.root.parent):
            hits = workspace_compose.search("Demo", 1, self.start, self.end)
        self.assertEqual(hits[0].window_status, "inside")

    def test_quoted_query_produces_valid_yaml(self):
        script = Path(workspace_compose.__file__)
        out = Path(self.temp.name) / "workspace.md"
        result = subprocess.run([sys.executable, str(script), 'topic "quote": detail', "--output", str(out)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        meta, _ = read_page(out)
        self.assertEqual(meta["task"], 'topic "quote": detail')

    def test_strategy_cli_rejects_missing_or_reversed_window(self):
        script = Path(workspace_compose.__file__)
        for dates in ([], ["--from", "2026-09-01", "--to", "2026-08-01"]):
            result = subprocess.run([sys.executable, str(script), "demo", "--mode", "strategy-report", *dates], capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
