class EvidenceBuilder:

    def build(self, findings):

        evidence = []

        for finding in findings:

            evidence.append({

                "title":
                    finding.title,

                "severity":
                    finding.severity,

                "impact":
                    finding.impact_score
            })

        return evidence

