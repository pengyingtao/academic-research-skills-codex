from __future__ import annotations

import unittest

from collect_github import build_search_query
from collect_nvd import weakness_group
from collect_patents_bulk import compile_family_patterns, normalize_date
from common import load_queries
from screen_candidates import screen_supply


class PilotLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.q = load_queries()

    def test_patent_family_patterns_do_not_match_generic_ai_only(self) -> None:
        patterns = compile_family_patterns(self.q)
        text = "A machine learning model for generic industrial optimization"
        matched = [fam for fam, pat in patterns.items() if pat.search(text)]
        self.assertEqual(matched, [])

    def test_patent_family_pattern_specific(self) -> None:
        patterns = compile_family_patterns(self.q)
        text = "Transformer based vulnerability repair for secure code"
        matched = [fam for fam, pat in patterns.items() if pat.search(text)]
        self.assertIn("T02", matched)
        self.assertNotIn("T07", matched)

    def test_normalize_compact_patent_date(self) -> None:
        self.assertEqual(normalize_date("20240630"), "2024-06-30")

    def test_github_query_requires_ai_anchor_and_cutoff(self) -> None:
        q = build_search_query("threat hunting", "machine learning", "2026-06-30")
        self.assertIn('"threat hunting"', q)
        self.assertIn('"machine learning"', q)
        self.assertIn("created:<=2026-06-30", q)

    def test_supply_without_ai_anchor_is_rejected(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/repo",
            "title_or_name": "Threat intelligence platform",
            "text_evidence": "cyber threat intelligence IOC extraction and SOC workflow",
            "topics": [],
        }
        out = screen_supply(row, self.q)
        self.assertFalse(out["in_scope"])
        self.assertEqual(out["false_positive_type"], "NO_AI_SIGNAL")
        self.assertIsNone(out["primary_technology_id"])

    def test_ai_threat_intelligence_maps_to_t07(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/repo",
            "title_or_name": "LLM cyber threat intelligence",
            "text_evidence": "large language model for cyber threat intelligence and IOC extraction",
            "topics": [],
        }
        out = screen_supply(row, self.q)
        self.assertTrue(out["in_scope"])
        self.assertEqual(out["primary_technology_id"], "T07")

    def test_xai_is_recognized_as_ai_anchor(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/repo",
            "title_or_name": "Explainable secure code analysis",
            "text_evidence": "XAI and explainable AI for secure code review and software security analysis",
            "topics": [],
        }
        out = screen_supply(row, self.q)
        self.assertTrue(out["in_scope"])
        self.assertEqual(out["primary_technology_id"], "T15")

    def test_profile_repo_is_rejected(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "alice/alice",
            "title_or_name": "alice/alice",
            "text_evidence": "Cybersecurity professional. Professional experience in SOC and threat hunting. AI-powered projects listed below.",
            "topics": [],
            "artifact_type": "production_platform",
            "analysis_role": "ENGINEERING_SUPPLY",
        }
        out = screen_supply(row, self.q)
        self.assertFalse(out["in_scope"])
        self.assertEqual(out["false_positive_type"], "PERSONAL_PROFILE")

    def test_generic_workflow_catalog_is_rejected(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/catalog",
            "title_or_name": "Workflow catalog",
            "text_evidence": "AI-powered workflows catalog and reusable workflow templates including some security examples",
            "topics": [],
            "artifact_type": "paper_code",
            "analysis_role": "ENGINEERING_SUPPLY",
        }
        out = screen_supply(row, self.q)
        self.assertFalse(out["in_scope"])
        self.assertEqual(out["false_positive_type"], "AGGREGATOR_NOT_TOOL")

    def test_education_only_ai_cyber_lab_is_rejected(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/cyber-gym",
            "title_or_name": "Cybersecurity Gym",
            "text_evidence": "AI-powered certification training, exam questions, study material and learning lab for cybersecurity students",
            "topics": [],
            "artifact_type": "tool_framework",
            "analysis_role": "ENGINEERING_SUPPLY",
        }
        out = screen_supply(row, self.q)
        self.assertFalse(out["in_scope"])
        self.assertEqual(out["false_positive_type"], "EDUCATIONAL_ONLY")

    def test_security_of_ai_is_excluded(self) -> None:
        row = {
            "source_type": "open_source",
            "source_native_id": "org/repo",
            "title_or_name": "LLM jailbreak detection",
            "text_evidence": "large language model jailbreak detection for prompt injection defense",
            "topics": [],
        }
        out = screen_supply(row, self.q)
        self.assertFalse(out["in_scope"])
        self.assertEqual(out["false_positive_type"], "SECURITY_OF_AI")

    def test_cwe_group_mapping(self) -> None:
        groups = self.q["vulnerability_strata"]
        self.assertEqual(weakness_group(["CWE-787"], groups), "W01")
        self.assertEqual(weakness_group(["CWE-89"], groups), "W02")
        self.assertEqual(weakness_group(["CWE-99999"], groups), "W99")


if __name__ == "__main__":
    unittest.main()
