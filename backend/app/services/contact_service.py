import re


class ContactService:

    def __init__(self):

        self.state = "idle"

        self.visitor_email = None
        self.visitor_phone = None
        self.visitor_message = None
        self.contact_type = None

        self.email_subject = None
        self.email_body = None


    # -------------------------------------------------
    # START CONTACT
    # -------------------------------------------------

    def start_contact(self):

        self.state = "waiting_for_email"

        self.visitor_email = None
        self.visitor_phone = None
        self.visitor_message = None
        self.contact_type = None

        self.email_subject = None
        self.email_body = None


    # -------------------------------------------------
    # VALIDATE EMAIL
    # -------------------------------------------------

    def is_valid_email(
        self,
        email: str
    ) -> bool:

        pattern = (
            r"^[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+"
            r"\.[A-Za-z]{2,}$"
        )

        return bool(
            re.match(
                pattern,
                email.strip()
            )
        )


    def extract_contact_details(self, text: str) -> tuple[str | None, str | None]:

        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
        phone_match = re.search(
            r"(?:\+?\d[\d\s().-]{7,}\d)",
            text
        )

        email = email_match.group(0) if email_match else None
        phone = phone_match.group(0).strip() if phone_match else None

        return email, phone


    # -------------------------------------------------
    # SAVE VISITOR CONTACT DETAILS
    # -------------------------------------------------

    def save_email(
        self,
        email: str | None,
        phone: str | None = None
    ):

        self.visitor_email = email.strip() if email else None
        self.visitor_phone = phone

        self.state = "waiting_for_contact_type"


    # -------------------------------------------------
    # PARSE CONTACT TYPE
    # -------------------------------------------------

    def parse_contact_type(
        self,
        message: str
    ) -> str | None:

        normalized = message.lower().strip()

        if "interview" in normalized:
            return "interview"

        if "resume" in normalized and (
            "shortlist" in normalized
            or "short listed" in normalized
            or "shortlisted" in normalized
        ):
            return "resume_shortlisted"

        if (
            "user detail" in normalized
            or "user details" in normalized
            or "user information" in normalized
            or normalized == "details"
        ):
            return "user_details"

        if "other" in normalized or "others" in normalized:
            return "other"

        return None


    # -------------------------------------------------
    # SAVE CONTACT TYPE
    # -------------------------------------------------

    def save_contact_type(
        self,
        contact_type: str
    ):

        self.contact_type = contact_type
        self.state = "waiting_for_message"


    # -------------------------------------------------
    # SAVE VISITOR MESSAGE
    # -------------------------------------------------

    def save_message(
        self,
        message: str
    ):

        self.visitor_message = message.strip()

        self.state = "preparing_email"


    # -------------------------------------------------
    # SAVE GENERATED EMAIL
    # -------------------------------------------------

    def save_generated_email(
        self,
        subject: str,
        body: str
    ):

        self.email_subject = subject.strip()
        self.email_body = body.strip()

        self.state = "waiting_for_confirmation"


    # -------------------------------------------------
    # CHECK CONFIRMATION
    # -------------------------------------------------

    def is_confirmation(
        self,
        message: str
    ) -> bool:

        message = message.lower().strip()

        confirmation_words = [
            "yes",
            "yes send",
            "yes send it",
            "send",
            "send it",
            "confirm",
            "confirmed",
            "okay send",
            "ok send",
            "go ahead",
            "sure send it"
        ]

        return message in confirmation_words


    # -------------------------------------------------
    # CHECK CANCELLATION
    # -------------------------------------------------

    def is_cancellation(
        self,
        message: str
    ) -> bool:

        message = message.lower().strip()

        cancellation_words = [
            "no",
            "cancel",
            "don't send",
            "do not send",
            "stop",
            "no thanks",
            "no thank you"
        ]

        return message in cancellation_words


    # -------------------------------------------------
    # RESET CONTACT
    # -------------------------------------------------

    def reset(self):

        self.state = "idle"

        self.visitor_email = None
        self.visitor_phone = None
        self.visitor_message = None
        self.contact_type = None

        self.email_subject = None
        self.email_body = None


contact_service = ContactService()
