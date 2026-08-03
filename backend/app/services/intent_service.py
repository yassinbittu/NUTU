from groq import Groq
import re

from app.config import settings


class IntentService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    # =================================================
    # LLM CLASSIFIER
    # =================================================
    # Decides:
    # yassin_question
    # contact_yassin
    # unrelated
    # =================================================

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

                        # -----------------------------
                        # YASSIN QUESTION
                        # -----------------------------

                        "yassin_question - if the user is asking about "
                        "Yassin, his skills, education, experience, "
                        "projects, certifications, background, career, "
                        "technologies, location, date of birth, "
                        "contact information, professional profile, "
                        "or anything related to him.\n\n"

                        # -----------------------------
                        # CONTACT YASSIN
                        # -----------------------------

                        "contact_yassin - if the user wants to contact, "
                        "message, email, recruit, hire, interview, "
                        "schedule a meeting with, send an opportunity to, "
                        "or personally communicate with Yassin.\n\n"

                        "Examples of contact_yassin:\n"
                        "'I want to contact Yassin'\n"
                        "'Can you send Yassin an email?'\n"
                        "'I want to send him a message'\n"
                        "'I have a job opportunity for Yassin'\n"
                        "'I want to hire Yassin'\n"
                        "'Can Yassin contact me?'\n"
                        "'Tell Yassin to contact me'\n"
                        "'I would like to interview him'\n"
                        "'I want to schedule an interview with Yassin'\n"
                        "'I like his profile and want to talk to him'\n"
                        "'We have an opportunity for him'\n"
                        "'Can I connect with Yassin?'\n\n"

                        # -----------------------------
                        # UNRELATED
                        # -----------------------------

                        "unrelated - if the user is asking about something "
                        "not related to Yassin.\n\n"

                        # -----------------------------
                        # IMPORTANT RULES
                        # -----------------------------

                        "Pronouns such as he, him, and his should refer "
                        "to Yassin when the message appears to be "
                        "about Yassin.\n\n"

                        "If someone expresses interest in Yassin and wants "
                        "to communicate with him, classify it as "
                        "contact_yassin, not yassin_question.\n\n"

                        "If someone only asks for Yassin's email address "
                        "or phone number, classify it as "
                        "yassin_question.\n\n"

                        "If someone asks NUTU to send Yassin a message "
                        "or help them contact Yassin, classify it as "
                        "contact_yassin.\n\n"

                        "Return ONLY one of these exact values:\n"
                        "yassin_question\n"
                        "contact_yassin\n"
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

        if intent == "contact_yassin":
            return "contact_yassin"

        return "unrelated"


    # =================================================
    # MAIN INTENT DETECTOR
    # =================================================

    def detect_intent(
        self,
        message: str
    ) -> str:

        message = message.lower().strip()


        # -------------------------------------------------
        # 1. RESUME REQUEST
        # -------------------------------------------------

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


        # -------------------------------------------------
        # 2. FAREWELL DETECTION
        # -------------------------------------------------

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


        # -------------------------------------------------
        # 3. GREETING DETECTION
        # -------------------------------------------------

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


        # -------------------------------------------------
        # 4. GREETING + ANOTHER MESSAGE
        # -------------------------------------------------

        if has_greeting:

            remaining_message = message

            # Remove greeting phrases
            for greeting in greeting_words:

                remaining_message = re.sub(
                    rf"\b{re.escape(greeting)}\b",
                    "",
                    remaining_message
                )


            # Remove NUTU
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


            # Only greeting
            if not remaining_message:
                return "greeting"


            # Greeting + actual message
            return self.classify_with_llm(
                remaining_message
            )


        # -------------------------------------------------
        # 5. NORMAL MESSAGE
        # -------------------------------------------------

        return self.classify_with_llm(
            message
        )


# =====================================================
# REUSABLE SERVICE INSTANCE
# =====================================================

intent_service = IntentService()