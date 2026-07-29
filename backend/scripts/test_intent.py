import os
import sys


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)


from app.services.intent_service import intent_service


test_messages = [
    "hi nutu what skills does Yassin have?",
"hello what projects has Yassin built?",
"namaste nutu tell me about Yassin",
"good evening nutu where did Yassin study?",
"hey nutu tell me a joke"
]


for message in test_messages:

    intent = intent_service.detect_intent(message)

    print(
        f"{message:<35} -> {intent}"
    )