

import json
import re
from pathlib import Path


class NovaChatbot:

    def __init__(self):
        self.running = True
        self.user_name = None
        self.last_faq = None
        self.conversation_history = []

        self.load_knowledge_base()
        self.display_welcome()

    # -----------------------------------------
    # LOAD JSON KNOWLEDGE BASE
    # -----------------------------------------

    def load_knowledge_base(self):

        json_path = Path(__file__).with_name("sample_faq.json")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)

            if not isinstance(self.data.get("greetings"), list):
                raise ValueError("Greetings must be a list.")

            if not isinstance(self.data.get("faqs"), list):
                raise ValueError("FAQs must be a list.")

            for faq in self.data["faqs"]:
                if not isinstance(faq, dict):
                    raise ValueError("Each FAQ must be an object.")

                if not isinstance(faq.get("question"), str):
                    raise ValueError("FAQ question must be text.")

                if not isinstance(faq.get("answer"), str):
                    raise ValueError("FAQ answer must be text.")

            print("[SYSTEM] Knowledge base loaded successfully.")

        except FileNotFoundError:
            print("[ERROR] sample_faq.json not found.")
            raise

        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format.")
            raise

    # -----------------------------------------
    # WELCOME SCREEN
    # -----------------------------------------

    def display_welcome(self):

        print("\n" + "=" * 55)
        print("              NOVA TERMINAL ASSISTANT")
        print("=" * 55)

        print("Hello! I am NOVA, your Datheon support assistant.")
        print("I can answer internship-related questions and FAQs.")

        print("\nAvailable Commands:")
        print("  help     - Show available commands")
        print("  history  - View conversation history")
        print("  bye      - Exit the assistant")

        print("=" * 55)

    # -----------------------------------------
    # INPUT NORMALIZATION
    # -----------------------------------------

    def normalize(self, text):

        text = text.lower().strip()

        text = re.sub(r"[^\w\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text

    # -----------------------------------------
    # GREETING RECOGNITION
    # -----------------------------------------

    def identify_greeting(self, message):

        for greeting in self.data["greetings"]:

            greeting = self.normalize(greeting)

            pattern = rf"\b{re.escape(greeting)}\b"

            if re.search(pattern, message):
                return True

        return False

    # -----------------------------------------
    # EXIT RECOGNITION
    # -----------------------------------------

    def identify_exit(self, message):

        exit_commands = {"bye", "goodbye", "exit", "quit"}

        return message in exit_commands

    # -----------------------------------------
    # NAME RECOGNITION
    # -----------------------------------------

    def identify_name(self, message):

        pattern = r"\b(?:my name is|call me|i am)\s+([a-z]+)\b"

        match = re.search(pattern, message)

        if match:
            self.user_name = match.group(1).capitalize()

            return (
                f"Nice to meet you, {self.user_name}!"
            )

        return None

    # -----------------------------------------
    # FAQ MATCHING ENGINE
    # -----------------------------------------

    def find_faqs(self, message):

        stop_words = {
            "what", "are", "is", "the", "a", "an",
            "your", "you", "i", "do", "how", "when",
            "will", "can", "me", "my", "to", "of",
            "for", "and", "in", "on", "about"
        }

        query_words = set(message.split()) - stop_words

        matches = []

        for faq in self.data["faqs"]:

            question = self.normalize(faq["question"])

            faq_words = set(question.split()) - stop_words

            if not faq_words:
                continue

            common_words = query_words.intersection(faq_words)

            score = len(common_words) / len(faq_words)

            if question in message or score >= 0.5:

                matches.append((score, faq))

        matches.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [faq for score, faq in matches]

    # -----------------------------------------
    # CONVERSATION HISTORY
    # -----------------------------------------

    def show_history(self):

        if not self.conversation_history:

            return "No conversation history available yet."

        history = []

        history.append("=" * 45)
        history.append("       NOVA CONVERSATION HISTORY")
        history.append("=" * 45)

        for index, chat in enumerate(
            self.conversation_history, start=1
        ):

            history.append(
                f"\n[{index}] You: {chat['user']}"
            )

            history.append(
                f"    NOVA: {chat['nova']}"
            )

        history.append("\n" + "=" * 45)

        return "\n".join(history)

    # -----------------------------------------
    # HELP COMMAND
    # -----------------------------------------

    def show_help(self):

        return (
            "\nI can help you with:\n"
            "1. Business hours\n"
            "2. Internship project submission\n"
            "3. Certificate information\n"
            "4. General internship FAQs\n"
            "5. Your conversation history\n\n"
            "Commands:\n"
            "help     - Show help\n"
            "history  - View conversation\n"
            "bye      - Exit NOVA"
        )

    # -----------------------------------------
    # RESPONSE GENERATION
    # -----------------------------------------

    def get_response(self, user_input):

        message = self.normalize(user_input)

        if not message:

            return "Please enter a message."

        # Exit handling
        if self.identify_exit(message):

            self.running = False

            return (
                "Thank you for chatting with NOVA. "
                "Have a great day!"
            )

        # Help command
        if message == "help":

            return self.show_help()

        # History command
        if message in {"history", "show history"}:

            return self.show_history()

        responses = []

        # Name recognition
        name_response = self.identify_name(message)

        if name_response:
            responses.append(name_response)

        # Greeting recognition
        if self.identify_greeting(message):

            if self.user_name:

                responses.append(
                    f"Hello {self.user_name}! How can I help you?"
                )

            else:

                responses.append(
                    "Hello! How can I assist you today?"
                )

        # Contextual follow-up
        follow_up_commands = {
            "tell me more",
            "repeat",
            "explain again",
            "more details"
        }

        if message in follow_up_commands:

            if self.last_faq:

                responses.append(
                    self.last_faq["answer"]
                )

            else:

                responses.append(
                    "Please ask me a question first."
                )

        else:

            # Multi-intent FAQ matching
            matches = self.find_faqs(message)

            if matches:

                self.last_faq = matches[0]

                for faq in matches:

                    responses.append(
                        f"Q: {faq['question']}\n"
                        f"A: {faq['answer']}"
                    )

        # Graceful fallback
        if not responses:

            return (
                "I'm sorry, I couldn't understand your question.\n"
                "Try asking about business hours, project "
                "submission, or certificate information.\n"
                "Type 'help' for assistance."
            )

        return "\n\n".join(responses)

    # -----------------------------------------
    # MAIN CHAT LOOP
    # -----------------------------------------

    def run(self):

        while self.running:

            try:

                user_input = input("\nYou: ")

                response = self.get_response(user_input)

                print(f"\nNOVA: {response}")

                # Store conversation
                self.conversation_history.append({
                    "user": user_input,
                    "nova": response
                })

            except KeyboardInterrupt:

                print(
                    "\n\nNOVA: Session interrupted. Goodbye!"
                )

                self.running = False


# -----------------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------------

if __name__ == "__main__":

    try:

        bot = NovaChatbot()

        bot.run()

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        ValueError
    ) as error:

        print(f"\nUnable to start NOVA: {error}")
