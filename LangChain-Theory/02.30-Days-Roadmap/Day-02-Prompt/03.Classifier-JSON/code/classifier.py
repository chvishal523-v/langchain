import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import CLASSIFIER_PROMPT, format_labels

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
labels = ["bug", "feature_request", "billing", "general_question"]
text = "Your app is charging me twice every month. Please fix this."

msg = CLASSIFIER_PROMPT.format_messages(
    text=text,
    labels=format_labels(labels)
)

resp = llm.invoke(msg)
print("RAW:", resp.content)

# Clean and parse JSON - handles markdown code fences
content = resp.content.strip()

# Remove markdown code fences if present
if "```" in content:
    # Try to extract JSON from code fences
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    else:
        # Fallback: remove all backticks
        content = content.replace('```json', '').replace('```', '').strip()

# Parse the cleaned JSON
try:
    data = json.loads(content)
    print("PARSED:", data)
except json.JSONDecodeError as e:
    print(f"JSON Parse Error: {e}")
    print(f"Cleaned content: {content}")
    raise