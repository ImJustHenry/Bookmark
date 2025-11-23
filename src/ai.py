from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def get_recommendations(previous_searches, current_book, num_recs=5):
    if not previous_searches:
        previous_searches = []
    elif isinstance(previous_searches, str):
        previous_searches = [previous_searches]
    elif isinstance(previous_searches, list):
        flattened = []
        for item in previous_searches:
            if isinstance(item, list):
                flattened.extend([str(x) for x in item])
            else:
                flattened.append(str(item))
        previous_searches = flattened
    else:
        raise ValueError("previous_searches must be a list or string")

    if isinstance(current_book, list):
        current_book = " ".join([str(x) for x in current_book])
    else:
        current_book = str(current_book)

    recent_searches = previous_searches[-5:]
    books_list = recent_searches + [current_book]
    prompt = (
        f"Recommend {num_recs} books based on the following books: "
        f"{', '.join(books_list)}. "
        "Provide your recommendations in JSON format like this:\n"
        '[{"title": "Book Title 1", "summary": "Short summary"}, ...]'
    )

    client = get_client()

    if client is None:
        return [{"title": current_book, "summary": "No AI recommendations available."}]

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```") and text.endswith("```"):
            text = "\n".join(text.split("\n")[1:-1])

        try:
            recommendations = json.loads(text)
        except json.JSONDecodeError:
            recommendations = []
            for line in text.split("\n"):
                if not line.strip():
                    continue
                parts = line.split("Summary:")
                if len(parts) == 2:
                    title = parts[0].split("Title:")[-1].strip()
                    summary = parts[1].strip()
                    recommendations.append({"title": title, "summary": summary})

        if not recommendations:
            recommendations = [{"title": current_book, "summary": "No AI recommendations available."}]

    except Exception as e:
        print(f"AI recommendation error: {e}")
        recommendations = [{"title": current_book, "summary": "No AI recommendations available."}]

    return recommendations


if __name__ == "__main__":
    recs = get_recommendations(
        previous_searches=["To Kill a Mockingbird", "1984"],
        current_book="Pride and Prejudice"
    )
    print("Recommendations:", recs)
