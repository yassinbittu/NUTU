from groq import Groq

from app.config import settings
from app.prompts.nutu_prompt import (
    NUTU_SYSTEM_PROMPT,
    build_nutu_prompt
)


class LLMService:

    def __init__(self):

        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing from .env"
            )

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    # -------------------------------------------------
    # 1. NORMAL YASSIN QUESTIONS
    # RAG context + Groq
    # -------------------------------------------------

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        user_prompt = build_nutu_prompt(
            question=question,
            context=context
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": NUTU_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_tokens=500
        )

        return response.choices[0].message.content


    # -------------------------------------------------
    # 2. GREETINGS
    # Groq only - NO RAG
    # -------------------------------------------------

    def generate_greeting(
        self,
        message: str
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NUTU, the personal AI assistant "
                        "for Mohammed Yassin. "

                        "The user is greeting you. Respond naturally "
                        "and conversationally to the greeting. "

                        "Keep the response short, usually one or two "
                        "sentences. "

                        "Do not provide Yassin's professional summary, "
                        "education, skills, experience, projects, "
                        "certifications, location, or other information "
                        "unless the user specifically asks. "

                        "Do not turn a simple greeting into a long "
                        "introduction about Yassin. "

                        "You may briefly say you are NUTU when appropriate. "

                        "Match the user's greeting naturally. "
                        "For example, respond appropriately to Hi, Hello, "
                        "Namaste, Assalamualaikum, Good Morning, "
                        "Good Afternoon, or Good Evening."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.6,
            max_tokens=80
        )

        return response.choices[0].message.content


    # -------------------------------------------------
    # 3. FAREWELL
    # Groq only - NO RAG
    # -------------------------------------------------

    def generate_farewell(
        self,
        message: str
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NUTU, the personal AI assistant "
                        "for Mohammed Yassin. "

                        "The user is ending the conversation. "
                        "Respond naturally, warmly, and briefly, "
                        "like a real conversational assistant. "

                        "Do not redirect the user to ask about Yassin. "
                        "Do not provide Yassin's professional information. "
                        "Do not mention that you are designed only to "
                        "answer questions about Yassin. "

                        "Keep the response to one or two short sentences. "
                        "Vary your response naturally instead of using "
                        "the exact same goodbye every time. "

                        "Examples of the style: "
                        "'Bye! Take care and have a great day!' "
                        "'See you later! It was nice chatting with you.' "
                        "'Goodbye! Have a good one!'"
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=60
        )

        return response.choices[0].message.content


    # -------------------------------------------------
    # 4. UNRELATED QUESTIONS
    # Groq only - NO RAG
    # -------------------------------------------------

    def generate_redirect(
        self,
        message: str
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NUTU, the personal AI assistant "
                        "for Mohammed Yassin. "

                        "The user's message is unrelated to Yassin. "
                        "Do not answer the unrelated question. "

                        "Briefly and naturally explain that you are "
                        "here to help with information about Yassin. "

                        "Keep your response to one short sentence whenever "
                        "possible and never more than two short sentences. "

                        "Do not list Yassin's skills, projects, education, "
                        "experience, certifications, or other details. "

                        "Do not explain your internal limitations. "

                        "Do not mention RAG, context, vector databases, "
                        "embeddings, or internal systems. "

                        "Do not use the exact same wording every time."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.6,
            max_tokens=60
        )

        return response.choices[0].message.content


    # -------------------------------------------------
    # 5. GENERATE CONTACT EMAIL
    # Groq converts visitor message into professional email
    # -------------------------------------------------

    def generate_contact_email(
        self,
        visitor_email: str | None,
        visitor_message: str,
        contact_type: str | None = None,
        visitor_phone: str | None = None,
        current_draft: str | None = None,
        revision_request: str | None = None
    ) -> dict:

        type_note = ""

        if contact_type == "interview":
            type_note = (
                "The visitor is asking to schedule or discuss an "
                "interview with Yassin. "
            )
        elif contact_type == "resume_shortlisted":
            type_note = (
                "The visitor wants to share their resume or ask "
                "about being shortlisted for a role. "
            )
        elif contact_type == "user_details":
            type_note = (
                "The visitor is sending their details so Yassin "
                "can contact them. "
            )
        elif contact_type == "other":
            type_note = (
                "The visitor has another type of message for Yassin. "
            )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NUTU, Mohammed Yassin's personal "
                        "AI assistant. "

                        "A visitor wants to contact Yassin. "
                        "Convert the visitor's message into a concise, "
                        "professional email addressed to Yassin. "

                        "Use the visitor's own intention and tone, and "
                        "keep the message clear. "

                        "Do not invent company names, dates, job titles, "
                        "salary information, interview times, or other "
                        "details that the visitor did not provide. "

                        "If a contact type is provided, reflect it in the "
                        "subject line and body naturally. "

                        "When a current draft and revision request are "
                        "provided, revise the draft according to the "
                        "visitor's request while preserving accurate "
                        "contact details. "

                        "Return exactly this format:\n\n"

                        "SUBJECT: <email subject>\n"
                        "BODY:\n"
                        "<email body>\n\n"

                        "Include the visitor's contact email and, when "
                        "provided, phone number near the end of the email "
                        "so Yassin can reply to them."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Visitor email: {visitor_email or 'Not provided'}\n\n"
                        f"Visitor phone: {visitor_phone or 'Not provided'}\n\n"
                        f"Contact type: {contact_type or 'general'}\n\n"
                        f"Visitor message:\n{visitor_message}\n\n"
                        f"Current draft: {current_draft or 'None'}\n\n"
                        f"Revision request: {revision_request or 'None'}"
                    )
                }
            ],
            temperature=0.3,
            max_tokens=400
        )

        content = (
            response.choices[0]
            .message.content
            .strip()
        )

        # Default values in case Groq doesn't follow
        subject = "Message from a NUTU visitor"
        body = content

        if "SUBJECT:" in content and "BODY:" in content:

            subject_part, body_part = content.split(
                "BODY:",
                1
            )

            subject = (
                subject_part
                .replace("SUBJECT:", "")
                .strip()
            )

            body = body_part.strip()

        return {
            "subject": subject,
            "body": body
        }


# -------------------------------------------------
# CREATE ONE REUSABLE LLM SERVICE INSTANCE
# This must remain outside the class and at the bottom.
# -------------------------------------------------

llm_service = LLMService()
