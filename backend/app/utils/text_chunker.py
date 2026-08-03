import json
from typing import Any
from datetime import datetime


# =================================================
# GENERIC JSON -> TEXT
# =================================================

def object_to_text(
    data: Any,
    prefix: str = ""
) -> str:
    """
    Convert a JSON object into readable text
    for embeddings.
    """

    parts = []

    if isinstance(data, dict):

        for key, value in data.items():

            readable_key = (
                key
                .replace("_", " ")
                .title()
            )

            if isinstance(
                value,
                (dict, list)
            ):

                nested_text = object_to_text(
                    value,
                    readable_key
                )

                if nested_text:
                    parts.append(nested_text)

            else:

                parts.append(
                    f"{readable_key}: {value}"
                )


    elif isinstance(data, list):

        for item in data:

            if isinstance(
                item,
                (dict, list)
            ):

                text = object_to_text(
                    item,
                    prefix
                )

                if text:
                    parts.append(text)

            else:

                parts.append(str(item))


    else:

        parts.append(str(data))


    return "\n".join(
        part
        for part in parts
        if part
    )


# =================================================
# DATE FORMATTER
# =================================================

def format_date(date_string: str) -> str:

    try:

        date_object = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        return date_object.strftime(
            "%B %d, %Y"
        )

    except (ValueError, TypeError):

        return str(date_string)


# =================================================
# PROFILE CHUNKING
# =================================================

def create_profile_chunks(
    filename: str,
    data: dict
) -> list[dict]:

    chunks = []

    name = data.get(
        "name",
        "Mohammed Yassin"
    )


    # -------------------------------------------------
    # IDENTITY
    # -------------------------------------------------

    chunks.append({
        "text": (
            f"The person's full name is {name}. "
            f"He is also referred to as Yassin "
            f"or Mohammed Yassin."
        ),
        "source": filename,
        "category": "profile",
        "item": "identity"
    })


    # -------------------------------------------------
    # LOCATION
    # -------------------------------------------------

    location = data.get("location")

    if location:

        chunks.append({
            "text": (
                f"{name} is from {location}. "
                f"{name}'s location is {location}."
            ),
            "source": filename,
            "category": "profile",
            "item": "location"
        })


    # -------------------------------------------------
    # DATE OF BIRTH
    # -------------------------------------------------

    dob = data.get("date_of_birth")

    if dob:

        formatted_dob = format_date(dob)

        chunks.append({
            "text": (
                f"{name}'s date of birth is "
                f"{formatted_dob}. "
                f"{name} was born on "
                f"{formatted_dob}. "
                f"The DOB of {name} is "
                f"{formatted_dob}."
            ),
            "source": filename,
            "category": "profile",
            "item": "date_of_birth"
        })


    # -------------------------------------------------
    # NATIONALITY
    # -------------------------------------------------

    nationality = data.get(
        "nationality"
    )

    if nationality:

        chunks.append({
            "text": (
                f"{name}'s nationality is "
                f"{nationality}. "
                f"{name} is {nationality}."
            ),
            "source": filename,
            "category": "profile",
            "item": "nationality"
        })


    # -------------------------------------------------
    # PROFESSIONAL TITLE
    # -------------------------------------------------

    professional_title = data.get(
        "professional_title"
    )

    if professional_title:

        chunks.append({
            "text": (
                f"{name}'s professional title is "
                f"{professional_title}."
            ),
            "source": filename,
            "category": "professional",
            "item": "professional_title"
        })


    # -------------------------------------------------
    # CURRENT ROLE
    # -------------------------------------------------

    current_role = data.get(
        "current_role"
    )

    if current_role:

        chunks.append({
            "text": (
                f"{name}'s current role is "
                f"{current_role}."
            ),
            "source": filename,
            "category": "professional",
            "item": "current_role"
        })


    # -------------------------------------------------
    # EXPERTISE
    # -------------------------------------------------

    expertise = data.get(
        "expertise",
        []
    )

    if expertise:

        expertise_text = ", ".join(
            expertise
        )

        # General expertise chunk
        chunks.append({
            "text": (
                f"{name}'s technical expertise "
                f"includes {expertise_text}."
            ),
            "source": filename,
            "category": "skills",
            "item": "expertise"
        })


        # Individual skill chunks
        for skill in expertise:

            chunks.append({
                "text": (
                    f"{name} has technical "
                    f"experience with {skill}. "
                    f"{skill} is part of "
                    f"{name}'s technical expertise."
                ),
                "source": filename,
                "category": "skills",
                "item": skill
            })


    # -------------------------------------------------
    # PROFESSIONAL SUMMARY
    # -------------------------------------------------

    summary = data.get("summary")

    if summary:

        chunks.append({
            "text": (
                f"Professional summary of "
                f"{name}: {summary}"
            ),
            "source": filename,
            "category": "professional",
            "item": "summary"
        })


    # -------------------------------------------------
    # CAREER GOALS
    # -------------------------------------------------

    career_goals = data.get(
        "career_goals"
    )

    if career_goals:

        chunks.append({
            "text": (
                f"{name}'s career goal is: "
                f"{career_goals}"
            ),
            "source": filename,
            "category": "career",
            "item": "career_goals"
        })


    # -------------------------------------------------
    # LANGUAGES
    # -------------------------------------------------

    languages = data.get(
        "languages",
        []
    )

    if languages:

        language_text = ", ".join(
            languages
        )

        chunks.append({
            "text": (
                f"{name} speaks "
                f"{language_text}. "
                f"The languages spoken by "
                f"{name} are {language_text}."
            ),
            "source": filename,
            "category": "profile",
            "item": "languages"
        })


    # -------------------------------------------------
    # EMAIL
    # -------------------------------------------------

    email = data.get("email")

    if email:

        chunks.append({
            "text": (
                f"{name}'s email address is "
                f"{email}. "
                f"He can be contacted by email "
                f"at {email}."
            ),
            "source": filename,
            "category": "contact",
            "item": "email"
        })


    # -------------------------------------------------
    # PHONE
    # -------------------------------------------------

    phone = data.get("phone")

    if phone:

        chunks.append({
            "text": (
                f"{name}'s phone number is "
                f"{phone}. "
                f"He can be contacted by phone "
                f"at {phone}."
            ),
            "source": filename,
            "category": "contact",
            "item": "phone"
        })


    return chunks


# =================================================
# MAIN CHUNK CREATOR
# =================================================

def create_chunks(
    filename: str,
    data: dict
) -> list[dict]:

    chunks = []


    # =================================================
    # PROFILE
    # =================================================

    if filename == "profile.json":

        return create_profile_chunks(
            filename,
            data
        )


    # =================================================
    # EDUCATION
    # =================================================

    elif filename == "education.json":

        for index, education in enumerate(
            data.get("education", [])
        ):

            chunks.append({
                "text": object_to_text(
                    education
                ),
                "source": filename,
                "category": "education",
                "item": str(index)
            })


    # =================================================
    # EXPERIENCE
    # =================================================

    elif filename == "experience.json":

        for index, experience in enumerate(
            data.get("experience", [])
        ):

            chunks.append({
                "text": object_to_text(
                    experience
                ),
                "source": filename,
                "category": "experience",
                "item": str(index)
            })


    # =================================================
    # PROJECTS
    # =================================================

    elif filename == "projects.json":

        for index, project in enumerate(
            data.get("projects", [])
        ):

            chunks.append({
                "text": object_to_text(
                    project
                ),
                "source": filename,
                "category": "project",
                "item": str(index)
            })


    # =================================================
    # FAQ
    # =================================================

    elif filename == "faq.json":

        for index, faq in enumerate(
            data.get("faqs", [])
        ):

            chunks.append({
                "text": (
                    f"Question: "
                    f"{faq.get('question', '')}\n"
                    f"Answer: "
                    f"{faq.get('answer', '')}"
                ),
                "source": filename,
                "category": "faq",
                "item": str(index)
            })


    # =================================================
    # SKILLS
    # =================================================

    elif filename == "skills.json":

        skills = data.get(
            "skills",
            {}
        )

        for category, values in (
            skills.items()
        ):

            chunks.append({
                "text": (
                    f"Skill Category: "
                    f"{category.replace('_', ' ').title()}\n"
                    f"Skills: "
                    f"{', '.join(values)}"
                ),
                "source": filename,
                "category": "skills",
                "item": category
            })


    # =================================================
    # CERTIFICATIONS
    # =================================================

    elif filename == "certifications.json":

        for index, certification in enumerate(
            data.get(
                "certifications",
                []
            )
        ):

            if isinstance(
                certification,
                dict
            ):

                text = object_to_text(
                    certification
                )

            else:

                text = str(
                    certification
                )


            chunks.append({
                "text": text,
                "source": filename,
                "category": "certification",
                "item": str(index)
            })


    # =================================================
    # FALLBACK
    # =================================================

    else:

        chunks.append({
            "text": json.dumps(
                data,
                ensure_ascii=False
            ),
            "source": filename,
            "category": "general"
        })


    return chunks