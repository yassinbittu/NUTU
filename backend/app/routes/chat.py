from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import rag_service
from app.services.llm_service import llm_service
from app.services.intent_service import intent_service
from app.services.name_service import name_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


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


    # -------------------------------------------------
    # 1. EMPTY MESSAGE
    # -------------------------------------------------

    if not message:

        return ChatResponse(
            answer="Please enter a question.",
            type="text"
        )


    # -------------------------------------------------
    # 2. NORMALIZE YASSIN'S NAME
    # Yaseen / Yasin / Yassine etc. -> Mohammed Yassin
    # -------------------------------------------------

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


    # -------------------------------------------------
    # 3. DETECT INTENT
    # IMPORTANT: use normalized message
    # -------------------------------------------------

    intent = intent_service.detect_intent(
        normalized_message
    )

    print(
        f"Detected intent: {intent}"
    )

    


    # -------------------------------------------------
    # 4. GREETING
    # Groq only - NO RAG
    # -------------------------------------------------

    if intent == "greeting":

        answer = llm_service.generate_greeting(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="greeting"
        )


    # -------------------------------------------------
    # 5. FAREWELL
    # Groq only - NO RAG
    # -------------------------------------------------

    if intent == "farewell":

        answer = llm_service.generate_farewell(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="farewell"
        )


    # -------------------------------------------------
    # 6. RESUME REQUEST
    # Direct PDF - NO RAG / NO Groq
    # -------------------------------------------------

    if intent == "resume":

        return ChatResponse(
            answer=(
                "Sure! You can view or download "
                "Yassin Mohammed's resume below."
            ),
            type="resume",
            action={
                "type": "resume",
                "label": "View Resume",
                "url": (
                    "/static/resume/"
                    "Yassin_Mohammed_Resume.pdf"
                )
            }
        )


    # -------------------------------------------------
    # 6. UNRELATED QUESTION
    # Short Groq redirect - NO RAG
    # -------------------------------------------------

    if intent == "unrelated":

        answer = llm_service.generate_redirect(
            message=normalized_message
        )

        return ChatResponse(
            answer=answer,
            type="redirect"
        )


    # -------------------------------------------------
    # 7. QUESTION ABOUT YASSIN
    # RAG -> ChromaDB -> Groq
    # -------------------------------------------------

    if intent == "yassin_question":

        # IMPORTANT:
        # Search using normalized message
        results = rag_service.search(
            query=normalized_message,
            top_k=4
        )


        # Combine retrieved chunks
        context = "\n\n---\n\n".join(
            result["text"]
            for result in results
        )


        # Generate natural answer
        # IMPORTANT:
        # Send normalized question to Groq
        answer = llm_service.generate_answer(
            question=normalized_message,
            context=context
        )


        return ChatResponse(
            answer=answer,
            type="text"
        )


    # -------------------------------------------------
    # 8. FALLBACK
    # -------------------------------------------------

    return ChatResponse(
        answer=(
            "I'm here to help you learn about Yassin."
        ),
        type="text"
    )