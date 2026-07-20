from pathlib import Path


class ProfileLoader:

    @staticmethod
    def load(path):

        return Path(path).read_text(
            encoding="utf-8",
            errors="ignore"
        )

    @staticmethod
    def load_uploaded_file(uploaded_file):

        return uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

