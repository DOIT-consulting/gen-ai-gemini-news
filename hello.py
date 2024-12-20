from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from pydantic import BaseModel
import enum

class Score(enum.IntEnum):
    BEAR = 1
    BEARISH = 2
    NEUTRAL = 3
    BULLISH = 4
    BULL = 5
    
class Result(BaseModel):
    score: int


def main():
    client = genai.Client()
    model_id = "gemini-2.0-flash-exp"

    google_search_tool = Tool(
        google_search = GoogleSearch()
    )

    response = client.models.generate_content(
        model=model_id,
        contents="Using latest crypto news evaluate the sentiment on eth for the last hour. be very brief",
        # config=GenerateContentConfig(
        #     tools=[google_search_tool],
        #     response_modalities=["TEXT"],
        # ),
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
            response_mime_type="application/json", response_schema=Result
        ),
    )

    responseStr = ''
    for each in response.candidates[0].content.parts:
        responseStr = responseStr + each.text

    result = Result.model_validate_json(responseStr)
    print(result)


if __name__ == "__main__":
    main()
