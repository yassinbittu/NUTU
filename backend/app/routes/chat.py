import traceback

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import rag_service
from app.services.llm_service import llm_service
from app.services.intent_service import intent_service
from app.services.name_service import name_service
from app.services.contact_service import contact_service
from app.services.email_service import email_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


CONTACT_TYPE_OPTIONS = [
    {"label": "Interview", "message": "interview"},
    {"label": "Resume shortlisted", "message": "resume shortlisted"},
    {"label": "Share my details", "message": "user details"},
    {"label": "Other", "message": "other"},
]


MESSAGE_SUGGESTIONS = {
    "interview": [
        "I would like to schedule an interview with you. Please let me know your availability.",
        "We are interested in discussing a software engineering opportunity with you.",
    ],
    "resume_shortlisted": [
        "Your resume has been shortlisted. Please share a convenient time to discuss the next steps.",
        "We would like to move forward with your application and discuss the role with you.",
    ],
    "user_details": [
        "I would like to share my details and discuss a potential opportunity with you.",
        "Please contact me to discuss how we can connect further.",
    ],
    "other": [
        "I would like to connect with you to discuss an opportunity.",
        "I have a message for you and would appreciate the chance to speak.",
    ],
}


# -------------------------------------------------
# REQUEST MODEL
# -------------------------------------------------

class ChatRequest(BaseModel):
    message: str


# -------------------------------------------------
# RESPONSE MODEL
# -------------------------------------------------

class ChatResponse(BaseModel):
    answer: str
    type: str = "text"
    action: dict | None = None


# -------------------------------------------------
# CHAT ENDPOINT
# -------------------------------------------------

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    # Original user message
    message = request.message.strip()


    # =================================================
    # 1. EMPTY MESSAGE
    # =================================================

    if not message:

        return ChatResponse(
            answer="Please enter a question.",
            type="text"
        )


    # =================================================
    # 2. ACTIVE CONTACT WORKFLOW
    # IMPORTANT:
    # Check this BEFORE normal intent detection.
    # =================================================


    # -------------------------------------------------
    # WAITING FOR VISITOR CONTACT DETAILS
    # -------------------------------------------------

    if contact_service.state == "waiting_for_email":

        visitor_email, visitor_phone = contact_service.extract_contact_details(message)

        if not visitor_email and not visitor_phone:

            return ChatResponse(
                answer=(
                    "Please enter a valid email address or phone number "
                    "so Yassin knows how to contact you."
                ),
                type="contact",
                action={
                    "type": "request_contact_email"
                }
            )


        contact_service.save_email(visitor_email, visitor_phone)


        print(
            "Contact details:",
            contact_service.visitor_email or contact_service.visitor_phone
        )


        return ChatResponse(
            answer=(
                "Thank you! What kind of message should I send to Yassin? "
                "Please choose one of these options: interview, "
                "resume shortlisted, user details, or other."
            ),
            type="contact",
            action={
                "type": "request_contact_type",
                "options": CONTACT_TYPE_OPTIONS
            }
        )


    # -------------------------------------------------
    # WAITING FOR CONTACT TYPE
    # -------------------------------------------------

    if contact_service.state == "waiting_for_contact_type":

        contact_type = contact_service.parse_contact_type(message)

        if not contact_type:

            return ChatResponse(
                answer=(
                    "Please tell me what type of message this is for Yassin. "
                    "Choose interview, resume shortlisted, user details, or other."
                ),
                type="contact",
                action={
                "type": "request_contact_type",
                "options": CONTACT_TYPE_OPTIONS
                }
            )


        contact_service.save_contact_type(contact_type)


        return ChatResponse(
            answer=(
                "Great. Now please provide a few details for the message "
                "so Yassin can reply to you appropriately."
            ),
            type="contact",
            action={
                "type": "request_contact_message",
                "suggestions": [
                    {"label": suggestion, "message": suggestion}
                    for suggestion in MESSAGE_SUGGESTIONS[contact_type]
                ]
            }
        )


    # -------------------------------------------------
    # WAITING FOR VISITOR MESSAGE
    # -------------------------------------------------

    if contact_service.state == "waiting_for_message":

        if len(message) < 3:

            return ChatResponse(
                answer=(
                    "Please provide a little more information "
                    "about what you'd like to discuss with Yassin."
                ),
                type="contact",
                action={
                    "type": "request_contact_message"
                }
            )


        contact_service.save_message(message)


        print(
            "Contact message:",
            contact_service.visitor_message
        )

        email_data = llm_service.generate_contact_email(
            visitor_email=contact_service.visitor_email,
            visitor_message=contact_service.visitor_message,
            contact_type=contact_service.contact_type,
            visitor_phone=contact_service.visitor_phone
        )

        contact_service.save_generated_email(
            subject=email_data["subject"],
            body=email_data["body"]
        )


        return ChatResponse(
            answer=(
                "I have drafted an email to Yassin at iamyassin25@gmail.com. "
                "Please review the subject and message below, then reply "
                "yes to confirm sending or no to cancel. You can also "
                "tell me what you would like to change.\n\n"
                f"Subject: {contact_service.email_subject}\n\n"
                f"{contact_service.email_body}"
            ),
            type="contact",
            action={
                "type": "request_contact_confirmation",
                "subject": contact_service.email_subject,
                "body": contact_service.email_body,
                "options": [
                    {"label": "Yes — send", "message": "yes", "variant": "primary"},
                    {"label": "No — cancel", "message": "no", "variant": "secondary"},
                ]
            }
        )


    # -------------------------------------------------
    # WAITING FOR CONFIRMATION
    # -------------------------------------------------

    if contact_service.state == "waiting_for_confirmation":

        if contact_service.is_confirmation(message):

            try:
                email_service.send_email(
                    subject=contact_service.email_subject,
                    body=contact_service.email_body,
                    visitor_email=contact_service.visitor_email,
                    recipient_email="iamyassin25@gmail.com"
                )

                answer = (
                    "Your email has been sent to Yassin at "
                    "iamyassin25@gmail.com. Thank you!"
                )
            except Exception as exc:

                traceback.print_exc()

                

                print("Email send failure:", str(exc))

                answer = (
                    "I was not able to send the email right now. "
                    "Please try again later."
                )
                

            contact_service.reset()

            return ChatResponse(
                answer=answer,
                type="contact"
            )


        if contact_service.is_cancellation(message):

            contact_service.reset()

            return ChatResponse(
                answer=(
                    "No problem. I have canceled the contact request. "
                    "If you want, I can help you start again."
                ),
                type="contact"
            )


        email_data = llm_service.generate_contact_email(
            visitor_email=contact_service.visitor_email,
            visitor_message=contact_service.visitor_message,
            contact_type=contact_service.contact_type,
            visitor_phone=contact_service.visitor_phone,
            current_draft=(
                f"Subject: {contact_service.email_subject}\n\n"
                f"{contact_service.email_body}"
            ),
            revision_request=message
        )

        contact_service.save_generated_email(
            subject=email_data["subject"],
            body=email_data["body"]
        )

        return ChatResponse(
            answer=(
                "I've updated the draft. Please review it and reply yes "
                "to send or no to cancel.\n\n"
                f"Subject: {contact_service.email_subject}\n\n"
                f"{contact_service.email_body}"
            ),
            type="contact",
            action={
                "type": "request_contact_confirmation",
                "subject": contact_service.email_subject,
                "body": contact_service.email_body,
                "options": [
                    {"label": "Yes — send", "message": "yes", "variant": "primary"},
                    {"label": "No — cancel", "message": "no", "variant": "secondary"},
                ]
            }
        )


    # =================================================
    # 3. NORMALIZE YASSIN'S NAME
    # Yaseen / Yasin / Yassine etc.
    # -> Mohammed Yassin
    # =================================================

    normalized_message = (
        name_service.normalize_yassin_name(
            message
        )
    )


    print(
        "Original message:",
        message
    )

    print(
        "Normalized message:",
        normalized_message
    )


    # =================================================
    # 4. DETECT INTENT
    # =================================================

    intent = intent_service.detect_intent(
        normalized_message
    )


    print(
        f"Detected intent: {intent}"
    )


    # =================================================
    # 5. GREETING
    # Groq only - NO RAG
    # =================================================

    if intent == "greeting":

        answer = llm_service.generate_greeting(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="greeting"
        )


    # =================================================
    # 6. FAREWELL
    # Groq only - NO RAG
    # =================================================

    if intent == "farewell":

        answer = llm_service.generate_farewell(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="farewell"
        )


    # =================================================
    # 7. RESUME REQUEST
    # Direct PDF - NO RAG / NO Groq
    # =================================================

    if intent == "resume":

        return ChatResponse(
            answer=(
                "Sure! You can view or download "
                "Yassin Mohammed's resume below. "
                "If you'd like, I can also help you contact Yassin "
                "at iamyassin25@gmail.com."
            ),
            type="resume",
            action={
                "type": "resume",
                "label": "View Resume",
                "suggestions": [
                    {
                        "label": "I want to contact Yassin",
                        "message": "I want to contact Yassin"
                    }
                ],
                "url": (
                    "/static/resume/"
                    "Yassin_Mohammed_Resume.pdf"
                )
            }
        )


    # =================================================
    # 8. CONTACT YASSIN
    # Start contact workflow
    # =================================================

    if intent == "contact_yassin":

        # IMPORTANT:
        # Start contact conversation state
        contact_service.start_contact()


        return ChatResponse(
            answer=(
                "Absolutely! I can help you get in touch with Yassin. "
                "Please provide your email address or phone number so "
                "Yassin knows how to contact you."
            ),
            type="contact",
            action={
                "type": "request_contact_email"
            }
        )


    # =================================================
    # 9. UNRELATED QUESTION
    # Groq redirect - NO RAG
    # =================================================

    if intent == "unrelated":

        answer = llm_service.generate_redirect(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="redirect"
        )


    # =================================================
    # 10. QUESTION ABOUT YASSIN
    # RAG -> ChromaDB -> Groq
    # =================================================

    if intent == "yassin_question":

        # ---------------------------------------------
        # Search knowledge base
        # ---------------------------------------------

        results = rag_service.search(
            query=normalized_message,
            top_k=4
        )


        # ---------------------------------------------
        # Combine retrieved chunks
        # ---------------------------------------------

        context = "\n\n---\n\n".join(
            result["text"]
            for result in results
        )


        # ---------------------------------------------
        # Generate natural answer
        # ---------------------------------------------

        answer = llm_service.generate_answer(
            question=normalized_message,
            context=context
        )


        return ChatResponse(
            answer=answer,
            type="text"
        )


    # =================================================
    # 11. FALLBACK
    # =================================================

    return ChatResponse(
        answer=(
            "I'm here to help you learn about Yassin."
        ),
        type="text"
    )
