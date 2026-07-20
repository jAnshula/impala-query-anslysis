from intelligence.recommendation import Recommendation

from intelligence.recommendation_library import (
    RECOMMENDATIONS
)

class RecommendationEngine:

    def build(self, root_causes):

        recommendations = []

        seen = set()

        for cause in root_causes:

            for rec_id in cause.recommendation_ids:

                if rec_id in seen:
                    continue

                seen.add(rec_id)

                rec = RECOMMENDATIONS.get(rec_id)

                if not rec:
                    continue

                recommendations.append(

                    Recommendation(
                        id=rec_id,
                        title=rec["title"],
                        description=rec["description"],
                        priority="HIGH"
                    )
                )

        return recommendations

