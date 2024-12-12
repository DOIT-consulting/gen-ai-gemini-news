from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import enum

class Score(enum.Enum):
    BEAR = "Bear"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"
    BULLISH = "Bullish"
    BULL = "Bull"

def main():
    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    google_search_tool = Tool(
        google_search = GoogleSearch()
    )

    response = client.models.generate_content(
        model=model_id,
        contents="Using latest crypto news evaluate the sentiment on eth for the last hour",
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        ),
    )

    sentiment = ''
    for each in response.candidates[0].content.parts:
        print(each.text)
        sentiment = sentiment + each.text

    print("===========================================================")
    
    response = client.models.generate_content(
        model=model_id,
        contents=f"""
        Using this sentiment analisys: 
        {sentiment}
        Generate a score from 1 to 5 where 1 is bear and 5 is bullish market. Be very concise.
        """,
        config=GenerateContentConfig(
            response_mime_type="application/json", response_schema=Score
        ),
    )

    for each in response.candidates[0].content.parts:
        print(each.text)


if __name__ == "__main__":
    main()
