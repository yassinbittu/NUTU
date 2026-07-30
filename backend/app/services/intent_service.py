from groq import Groq
import re

from app.config import settings


class IntentService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    # -------------------------------------------------
    # LLM CLASSIFIER
    # Decides: yassin_question OR unrelated
    # -------------------------------------------------

    def classify_with_llm(
        self,
        message: str
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intent classifier for NUTU, "
                        "a personal AI assistant about Mohammed Yassin. "

                        "Classify the user's message into exactly ONE "
                        "of these categories:\n\n"

                        "yassin_question - if the user is asking about "
                        "Yassin, his skills, education, experience, "
                        "projects, certifications, background, career, "
                        "technologies, or anything related to him.\n\n"

                        "unrelated - if the user is asking about something "
                        "not related to Yassin.\n\n"

                        "Pronouns such as he, him, and his should refer "
                        "to Yassin when the question appears to be about "
                        "his professional information.\n\n"

                        "Return ONLY one of these:\n"
                        "yassin_question\n"
                        "unrelated"
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0,
            max_tokens=10
        )

        intent = (
            response.choices[0]
            .message.content
            .strip()
            .lower()
        )

        if intent == "yassin_question":
            return "yassin_question"

        return "unrelated"


    # -------------------------------------------------
    # MAIN INTENT DETECTOR
    # -------------------------------------------------

    def detect_intent(
        self,
        message: str
    ) -> str:

        message = message.lower().strip()


        # --------------------------------
        # 1. Resume request
        # --------------------------------

        resume_words = [
            "resume",
            "cv",
            "curriculum vitae"
        ]

        if any(
            word in message
            for word in resume_words
        ):
            return "resume"


        # --------------------------------
        # 2. Farewell detection
        # --------------------------------

        farewell_words = [
            "bye",
            "bye bye",
            "goodbye",
            "good bye",
            "see you",
            "see you later",
            "take care",
            "catch you later"
        ]

        has_farewell = any(
            re.search(
                rf"\b{re.escape(farewell)}\b",
                message
            )
            for farewell in farewell_words
        )

        if has_farewell:
            return "farewell"


        # --------------------------------
        # 3. Greeting detection
        # --------------------------------

        greeting_words = [
            "hi",
            "hii",
            "hiii",
            "hello",
            "hey",
            "namaste",
            "assalamualaikum",
            "assalamu alaikum",
            "salam",
            "good morning",
            "good afternoon",
            "good evening",
            "good evng"
        ]

        has_greeting = any(
            re.search(
                rf"\b{re.escape(greeting)}\b",
                message
            )
            for greeting in greeting_words
        )


        # --------------------------------
        # 4. Greeting + another message
        # --------------------------------

        if has_greeting:

            remaining_message = message

            # Remove greeting phrases
            for greeting in greeting_words:

                remaining_message = re.sub(
                    rf"\b{re.escape(greeting)}\b",
                    "",
                    remaining_message
                )

            # Remove the word NUTU
            remaining_message = re.sub(
                r"\bnutu\b",
                "",
                remaining_message
            )

            # Remove punctuation
            remaining_message = re.sub(
                r"[^\w\s]",
                " ",
                remaining_message
            )

            # Remove extra spaces
            remaining_message = re.sub(
                r"\s+",
                " ",
                remaining_message
            ).strip()


            # Only greeting was provided
            if not remaining_message:
                return "greeting"


            # Greeting + actual question/message
            return self.classify_with_llm(
                remaining_message
            )


        # --------------------------------
        # 5. Normal message
        # --------------------------------

        return self.classify_with_llm(
            message
        )


intent_service = IntentService()