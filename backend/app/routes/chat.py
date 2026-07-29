from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import rag_service
from app.services.llm_service import llm_service
from app.services.intent_service import intent_service


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
    # 2. DETECT INTENT
    # -------------------------------------------------

    intent = intent_service.detect_intent(
        message
    )

    print(f"Detected intent: {intent}")


    # -------------------------------------------------
    # 3. GREETING
    # Groq only - NO RAG
    # -------------------------------------------------

    if intent == "greeting":

        answer = llm_service.generate_greeting(
            message=message
        )

        return ChatResponse(
            answer=answer,
            type="greeting"
        )


    # -------------------------------------------------
    # 4. RESUME REQUEST
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
    # 5. UNRELATED QUESTION
    # Short Groq redirect - NO RAG
    # -------------------------------------------------

    if intent == "unrelated":

        answer = llm_service.generate_redirect(
            message=message
        )

        return ChatResponse(
            answer=answer,
            type="redirect"
        )


    # -------------------------------------------------
    # 6. QUESTION ABOUT YASSIN
    # RAG -> ChromaDB -> Groq
    # -------------------------------------------------

    if intent == "yassin_question":

        # Retrieve relevant knowledge
        results = rag_service.search(
            query=message,
            top_k=4
        )

        # Combine retrieved chunks
        context = "\n\n---\n\n".join(
            result["text"]
            for result in results
        )

        # Generate natural answer
        answer = llm_service.generate_answer(
            question=message,
            context=context
        )

        return ChatResponse(
            answer=answer,
            type="text"
        )


    # -------------------------------------------------
    # 7. FALLBACK
    # -------------------------------------------------

    return ChatResponse(
        answer=(
            "I'm here to help you learn about Yassin."
        ),
        type="text"
    )