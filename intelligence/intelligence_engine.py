from intelligence.root_cause_engine import RootCauseEngine
from intelligence.recommendation_engine import RecommendationEngine
from intelligence.executive_summary_generator import ExecutiveSummaryGenerator
from intelligence.playbook_generator import PlaybookGenerator
from analyzers.findings import deduplicate_findings, finding_to_dict

class IntelligenceEngine:
    def run(self, profile, analytics_result):
        findings_raw = analytics_result.get("findings", [])
        # Convert all Finding objects to dicts
        findings = [finding_to_dict(f) for f in findings_raw]
        # Deduplicate findings before analysis
        findings = deduplicate_findings(findings)

        root_causes = RootCauseEngine().analyze(findings)
        recommendations = RecommendationEngine().build(root_causes)
        playbooks = PlaybookGenerator().build(root_causes)

        summary = ExecutiveSummaryGenerator().generate(
            profile, root_causes, recommendations, findings
        )

        return {
            "root_causes": root_causes,
            "recommendations": recommendations,
            "summary": summary,
            "playbooks": playbooks,
        }

