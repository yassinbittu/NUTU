import json
from typing import Any


def object_to_text(data: Any, prefix: str = "") -> str:
    """
    Convert a JSON object into readable text for embeddings.
    """

    parts = []

    if isinstance(data, dict):
        for key, value in data.items():

            readable_key = key.replace("_", " ").title()

            if isinstance(value, (dict, list)):
                nested_text = object_to_text(value, readable_key)

                if nested_text:
                    parts.append(nested_text)

            else:
                parts.append(f"{readable_key}: {value}")

    elif isinstance(data, list):
        for item in data:
            parts.append(object_to_text(item, prefix))

    else:
        parts.append(str(data))

    return "\n".join(
        part for part in parts if part
    )


def create_chunks(filename: str, data: dict) -> list[dict]:
    """
    Convert each knowledge JSON file into smaller semantic chunks.
    """

    chunks = []

    # PROFILE
    if filename == "profile.json":

        chunks.append({
            "text": object_to_text(data),
            "source": filename,
            "category": "profile"
        })

    # EDUCATION
    elif filename == "education.json":

        for index, education in enumerate(
            data.get("education", [])
        ):
            chunks.append({
                "text": object_to_text(education),
                "source": filename,
                "category": "education",
                "item": str(index)
            })

    # EXPERIENCE
    elif filename == "experience.json":

        for index, experience in enumerate(
            data.get("experience", [])
        ):
            chunks.append({
                "text": object_to_text(experience),
                "source": filename,
                "category": "experience",
                "item": str(index)
            })

    # PROJECTS
    elif filename == "projects.json":

        for index, project in enumerate(
            data.get("projects", [])
        ):
            chunks.append({
                "text": object_to_text(project),
                "source": filename,
                "category": "project",
                "item": str(index)
            })

    # FAQ
    elif filename == "faq.json":

        for index, faq in enumerate(
            data.get("faqs", [])
        ):
            chunks.append({
                "text": (
                    f"Question: {faq.get('question', '')}\n"
                    f"Answer: {faq.get('answer', '')}"
                ),
                "source": filename,
                "category": "faq",
                "item": str(index)
            })

    # SKILLS
    elif filename == "skills.json":

        skills = data.get("skills", {})

        for category, values in skills.items():

            chunks.append({
                "text": (
                    f"Skill Category: "
                    f"{category.replace('_', ' ').title()}\n"
                    f"Skills: {', '.join(values)}"
                ),
                "source": filename,
                "category": "skills",
                "item": category
            })

    # CERTIFICATIONS
    elif filename == "certifications.json":

        for index, certification in enumerate(
            data.get("certifications", [])
        ):

            if isinstance(certification, dict):
                text = object_to_text(certification)
            else:
                text = str(certification)

            chunks.append({
                "text": text,
                "source": filename,
                "category": "certification",
                "item": str(index)
            })

    # FALLBACK
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