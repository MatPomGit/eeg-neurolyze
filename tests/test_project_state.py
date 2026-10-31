"""Regression tests for the read-only scientific evidence index."""

from __future__ import annotations

import copy
import unittest

from tools.check_project_state import ROOT, read_state, validate_state


class ProjectStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = read_state()

    def test_repository_snapshot_is_valid(self) -> None:
        self.assertEqual(validate_state(self.state, ROOT), [])

    def test_missing_source_is_rejected(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][0]["source_paths"].append("not-a-real-source.py")
        self.assertTrue(any("missing file" in x for x in validate_state(bad, ROOT)))

    def test_no_repository_escape(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][0]["source_paths"] = ["../../private/key.pem"]
        self.assertTrue(any("escapes repository" in x for x in validate_state(bad, ROOT)))

    def test_planned_work_cannot_be_published_as_verified(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][3]["evidence_level"] = "DATASET_VALIDATED"
        self.assertTrue(any("planned feature" in x for x in validate_state(bad, ROOT)))

    def test_hardware_claim_requires_independent_provenance(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][2]["physical_qualification"] = True
        self.assertTrue(any("hardware qualification exceeds" in x
                            for x in validate_state(bad, ROOT)))

    def test_synthetic_scope_not_silently_widened(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][1]["synthetic_only"] = False
        self.assertTrue(any("real-data claim" in x for x in validate_state(bad, ROOT)))

    def test_missing_or_fabricated_ci_proof_is_rejected(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["milestones"][0]["verification"]["sha"] = "main"
        self.assertTrue(any("exact revision" in x for x in validate_state(bad, ROOT)))

    def test_no_fictitious_manuscript_path(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["publications"][0]["manuscript_path"] = "papers/unpublished.pdf"
        self.assertTrue(any("proposal cannot invent" in x
                            for x in validate_state(bad, ROOT)))

    def test_source_issue_coverage(self) -> None:
        bad = copy.deepcopy(self.state)
        bad["issue_references"].remove(21)
        self.assertTrue(any("missing source Issue" in x
                            for x in validate_state(bad, ROOT)))


if __name__ == "__main__":
    unittest.main()
