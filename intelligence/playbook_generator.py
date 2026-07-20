from intelligence.playbook_library import (
    PLAYBOOKS
)

class PlaybookGenerator:

    def build(
        self,
        root_causes
    ):

        output = []

        for cause in root_causes:

            playbook = PLAYBOOKS.get(
                cause.id
            )

            if not playbook:
                continue

            output.append(
                {
                    "title":
                        cause.title,

                    "severity":
                        cause.severity,

                    "playbook":
                        playbook
                }
            )

        return output

