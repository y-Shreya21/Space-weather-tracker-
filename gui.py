import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os

class SpaceWeatherChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Weather Chatbot")
        self.root.configure(bg="#1E1E1E")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg="#252526", fg="white")
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        # User input field
        self.user_input = tk.Entry(root, width=50, bg="#333", fg="white")
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.process_input, bg="#0078D7", fg="white")
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Load chat history
        self.chat_history = self.load_chat_history()

        # Display welcome message
        self.display_message("Bot: Hello! I am your Space Weather Tracker bot. Type 'exit' to end the chat.")

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def get_space_weather(self):
        api_key = "wdfC0b3cpKatbQCZnDPmPLgejUurgZBOUP4p2XpJ"
        url = f"https://api.nasa.gov/DONKI/notifications?startDate=2024-03-01&endDate=2024-04-01&type=all&api_key={api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  
            data = response.json()
            
            if not data:
                return "⚠️ No recent space weather alerts from NASA."

            latest_events = []
            for event in data[:3]:  # Get up to 3 latest alerts
                message = f"\n🔹 {event.get('messageType', 'Unknown')} - {event.get('messageBody', 'No details')[:150]}..."
                latest_events.append(message)

            return "🌍 Latest NASA Space Weather Alerts 🚀" + "".join(latest_events)

        except requests.exceptions.RequestException as e:
            return f"⚠️ Error fetching data from NASA: {e}"

    def process_input(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message(f"You: {user_text}")
        self.chat_history.append(("User", user_text))

        if user_text.lower() in ["exit", "quit", "bye"]:
            response = "Goodbye! Stay safe under the cosmic weather! 🚀"
            self.display_message(f"Bot: {response}")
            self.save_chat_history()
            self.root.quit()
        elif "weather" in user_text:
            response = self.get_space_weather()
        elif "history" in user_text:
            response = "Here is your chat history:\n" + "\n".join([f"{sender}: {msg}" for sender, msg in self.chat_history])
        else:
            response = "I can provide space weather updates. Try asking about space weather!"

        self.display_message(f"Bot: {response}")
        self.chat_history.append(("Bot", response))
        self.user_input.delete(0, tk.END)

    def save_chat_history(self):
        with open("chat_history.json", "w") as file:
            json.dump(self.chat_history, file)

    def load_chat_history(self):
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "r") as file:
                return json.load(file)
        return []

# Run the Tkinter GUI
if __name__ == "__main__":
    root = tk.Tk()
    bot = SpaceWeatherChatbot(root)
    root.mainloop()

