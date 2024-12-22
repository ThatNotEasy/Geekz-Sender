import json
import os
import time
from EmailHandler import SMS_Handler, print_dict

EMAIL = "your_email@domain.com"
SENDER_NAME = "your_name"
PHONE = os.environ.get("PHONE")
PASS = os.environ.get("PASS")
DATA_FILE = "data.json"
DEFAULT_PHONE = "1234567890"
DEFAULT_PASS = "YOUR_PASS"

if PHONE == DEFAULT_PHONE or PASS == DEFAULT_PASS:
    raise Exception("Please set PASS and PHONE in the Secrets tab.")
if EMAIL == "your_email@domain.com":
    raise Exception("Please change EMAIL to your email.")

def save_texts_to_file(texts):
    with open(DATA_FILE, "w") as file:
        json.dump(texts, file, indent=4)

def load_texts_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def process_new_texts(sms_handler, last_texts):
    texts = sms_handler.get_texts()
    new_texts = [text for text in texts if text not in last_texts]

    for text in new_texts:
        print("New email:")
        print_dict({
            "sender": text["from"],
            "subject": text["subject"],
            "text": text["content"][:100]
        })
        print("Sending email content to phone...")
        sms_handler.send_text(PHONE, "nerd", "response", text["content"][:100].upper())
        print("----")
    
    return texts

def main():
    sms_handler = SMS_Handler(EMAIL, SENDER_NAME, PASS)
    sms_handler.setup()

    last_texts = load_texts_from_file()

    while True:
        print("Updating...")
        texts = process_new_texts(sms_handler, last_texts)
        save_texts_to_file(texts)
        time.sleep(60)

if __name__ == "__main__":
    main()
