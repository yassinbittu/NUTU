import re


class NameService:

    def __init__(self):

        self.yassin_variations = [
            "yassin",
            "yaseen",
            "yasin",
            "yasein",
            "yassine",
            "yaseen mohammed",
            "yasin mohammed",
            "yassin mohammed",
            "yaseen muhammad",
            "yasin muhammad",
            "yassin muhammad",
            "mohammed yassin",
            "mohammad yassin",
            "muhammad yassin",
            "mohammed yaseen",
            "mohammad yaseen",
            "muhammad yaseen",
        ]


    def normalize_yassin_name(
        self,
        message: str
    ) -> str:

        normalized_message = message

        # Longest phrases first
        variations = sorted(
            self.yassin_variations,
            key=len,
            reverse=True
        )

        for variation in variations:

            normalized_message = re.sub(
                rf"\b{re.escape(variation)}\b",
                "Mohammed Yassin",
                normalized_message,
                flags=re.IGNORECASE
            )

        return normalized_message


name_service = NameService()