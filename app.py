from flask import Flask, request, render_template
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

# Load API Key securely from environment variable
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Error: Missing GOOGLE_API_KEY environment variable")

os.environ["GOOGLE_API_KEY"] = api_key  # Required by ChatGoogleGenerativeAI

app = Flask(__name__)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@app.route("/", methods=["GET", "POST"])
def enhance():
    improved_prompt = None

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "").strip()
        if user_prompt:
            messages = [
                SystemMessage(content="Rewrite the user's prompt to be more clear, specific, and effective. Return only the improved prompt."),
                HumanMessage(content=user_prompt)
            ]
            try:
                improved_prompt = llm.invoke(messages)
            except Exception as e:
                improved_prompt = f"❌ Error: {e}"

    return render_template("index.html", improved_prompt=improved_prompt)

if __name__ == "__main__":
    app.run(debug=True)

