import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import os
from dotenv import load_dotenv  # <-- NEW

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_fireworks import Fireworks

# --- Load API keys from .env ---
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

# --- Fireworks LLM Setup ---
llm = Fireworks(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct",
    fireworks_api_key=FIREWORKS_API_KEY  # use env variable
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful space weather assistant. Answer the question below:\n\nQuestion: {question}\nAnswer:"
)

chain = LLMChain(llm=llm, prompt=prompt)

# NASA DONKI API endpoint
NASA_URL = f"https://api.nasa.gov/DONKI/notifications?startDate=2024-03-01&endDate=2024-04-01&type=all&api_key={NASA_API_KEY}"

# --- GUI Class ---
class SpaceWeatherChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Weather Chatbot")
        self.root.configure(bg="#1E1E1E")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg="#252526", fg="white")
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.user_input = tk.Entry(root, width=50, bg="#333", fg="white")
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.process_input, bg="#0078D7", fg="white")
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.chat_history = self.load_chat_history()
        self.display_message("Bot: 👋 Hi! Ask me about space weather, alerts, or type 'history'.")

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def get_space_weather(self):
        try:
            response = requests.get(NASA_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                return "⚠️ No recent space weather alerts from NASA."

            latest_events = []
            for event in data[:3]:
                msg = f"\n🔹 {event.get('messageType', 'Unknown')}: {event.get('messageBody', 'No details')[:200]}..."
                latest_events.append(msg)

            return "🚀 Latest NASA Space Weather Alerts:" + "".join(latest_events)

        except requests.exceptions.RequestException as e:
            return f"⚠️ NASA API error: {e}"

    def process_input(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message(f"You: {user_text}")
        self.chat_history.append(("User", user_text))

        if user_text.lower() in ["exit", "quit", "bye"]:
            response = "Goodbye! Stay cosmic and safe! 👋"
            self.display_message(f"Bot: {response}")
            self.chat_history.append(("Bot", response))
            self.save_chat_history()
            self.root.quit()
            return

        elif "weather" in user_text.lower():
            response = self.get_space_weather()

        elif "history" in user_text.lower():
            history = "\n".join([f"{sender}: {msg}" for sender, msg in self.chat_history])
            response = f"📜 Chat History:\n{history}"

        else:
            response = chain.run(user_text)

        self.display_message(f"Bot: {response}")
        self.chat_history.append(("Bot", response))
        self.user_input.delete(0, tk.END)

    def save_chat_history(self):
        with open("chat_history.json", "w") as f:
            json.dump(self.chat_history, f)

    def load_chat_history(self):
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "r") as f:
                return json.load(f)
        return []

# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    bot = SpaceWeatherChatbot(root)
    root.mainloop() 

NASA_API_KEY = os.getenv("NASA_API_KEY")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

print("FIREWORKS_API_KEY =", FIREWORKS_API_KEY)
print("NASA_API_KEY =", NASA_API_KEY)


# --- End of File ---



