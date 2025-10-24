import datetime
import os
import random
import webbrowser
from time import time as t
import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv


# Load environment variables and configure API
def configure1(api_key):
    load_dotenv()


configure1(None)

api_key = os.getenv('api_key')

if not api_key:
    raise ValueError("API key not found. Please set 'api_key' in your .env file.")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Initialize chat messages
messages = [
    {
        "parts": [
            {
                "text": "You are a Powerful A.I Assistant Named Jarvis, created by Tony Stark. Talk like a human, the user giving inputs is Tony Stark and always use sir or Mr.Stark before speaking"
            }
        ],
        "role": "user"
    },
    {
        "parts": [
            "Hello! 👋 How can I help you today? 😊 \n",
        ],
        "role": "model"
    },
]


def generate_response():
    try:
        response = model.generate_content(messages)
        print("Full Response from AI:")
        print(response.text)  # Display full response
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I couldn't process that, Sir."


# Summarize function
def summarize(text, max_sentences=2):
    """
    Summarizes the given text to a specified number of sentences.
    Handles cases where text is too short or malformed.
    """
    if not text or len(text.strip()) == 0:
        return "Sorry Sir, I couldn't process the response."

    # Split text into sentences.
    sentences = text.split('. ')

    # Handle cases where sentences are separated by other punctuation
    if len(sentences) < max_sentences:
        # Attempt to split by newline or other delimiters if not enough sentences
        sentences = text.replace('\n', '. ').split('. ')

    # Ensure there's enough content to summarize.
    if len(sentences) < max_sentences:
        return text.strip()  # Return the full text if it's already short.

    # Join the first few sentences to form the summary.
    summary = '. '.join(sentences[:max_sentences]).strip() + '.'
    return summary


# Voice Engine Function
def say(text):
    os.system(f'say -v "Daniel" "{text}"')


# AI Interaction Function
def ai(prompt1):
    global messages
    messages.append({
        "parts": [
            {
                "text": prompt1
            }
        ],
        "role": "user"
    })

    response = model.generate_content(messages)

    messages.append({
        "parts": [
            {
                "text": response.text
            }
        ],
        "role": "model"
    })

    return response.text


# Chat Function
def chat(query, chatstr=""):
    chatstr += f"Tony: {query}\nJarvis: "
    global messages
    messages.append({
        "parts": [
            {
                "text": query
            }
        ],
        "role": "user"
    })
    if "play music" in query.lower() or "play songs" in query.lower():
        return ""
    elif any(f"open {site[0]}" in query.lower() for site in
             [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
              ["google", "https://www.google.com"], ["spotify", "https://www.spotify.com"],
              ["instagram", "https://www.instagram.com"]]):
        return ""

    try:
        response = model.generate_content(messages)
        print("Full Response from AI:")
        print(response.text)  # Display full response
        messages.append({
            "parts": [
                {
                    "text": response.text
                }
            ],
            "role": "model"
        })
        chatstr += f"{response.text}\n"
        return response.text
    except Exception as e:
        print("Error in generating response:", e)
        return "I couldn't understand that, Sir. Please try again."


# Voice Command Recognition
def take_command():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.pause_threshold = 0.6
    r.operation_timeout = None
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.5
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Recognition error: {e}")
            return "Some Error Occurred. Sorry Sir"


# Main Functionality
if __name__ == "__main__":
    while True:
        print("Jarvis Online, Please say the security phrase to activate Jarvis")
        say("Jarvis Online, Please say the security phrase to activate Jarvis")
        query = take_command()
        if "wake up jarvis daddy" in query.lower():
            try:
                from Greetme import greetme

                greetme()
            except ImportError:
                print("Greetme module not found.")
                say("Greetme module not found, Sir.")

            while True:
                print("Listening for further commands...")
                query = take_command()

                if "jarvis go offline" in query.lower() or "jarvis offline" in query.lower():
                    say("Going offline, Sir")
                    print("Going offline, Sir")
                    exit()
                elif "reset chat" in query.lower():
                    messages = [
                        {
                            "parts": [
                                {
                                    "text": "You are a Powerful A.I Assistant Named Jarvis, created by Tony Stark. Talk like a human, the user giving inputs is Tony Stark and always use sir or Mr.Stark before speaking"
                                }
                            ],
                            "role": "user"
                        },
                        {
                            "parts": [
                                "Hello! 👋 How can I help you today? 😊 \n",
                            ],
                            "role": "model"
                        },
                    ]
                    print("Chat has been reset, Sir.")
                    say("Done Sir, as per your instructions, all the previous chat has been deleted.")

                elif "go to sleep" in query.lower():
                    say("Going to sleep, Sir")
                    print("Going to sleep, Sir")
                    break

                try:
                    # Define sites and apps outside the try block for better structure
                    sites = [
                        ["youtube", "https://www.youtube.com"],
                        ["wikipedia", "https://www.wikipedia.com"],
                        ["google", "https://www.google.com"],
                        ["spotify", "https://www.spotify.com"],
                        ["instagram", "https://www.instagram.com"]
                    ]
                    apps_v1 = [
                        ["weather", "/System/Applications/Weather.app"],
                        ["facetime", "/System/Applications/FaceTime.app"],
                        ["maps", "/System/Applications/Maps.app"],
                        ["messages", "/System/Applications/Messages.app"]
                    ]

                    # Check for site openings
                    site_opened = False
                    for site in sites:
                        if f"open {site[0]}" in query.lower():
                            print(f"Opening {site[0]} Sir...")
                            say(f"Opening {site[0]} Sir...")
                            webbrowser.open(site[1])
                            site_opened = True
                            break
                    if site_opened:
                        continue

                    # Check for app openings
                    app_opened = False
                    for app in apps_v1:
                        if f"open {app[0]}" in query.lower():
                            print(f"Opening {app[0]} Sir...")
                            say(f"Opening {app[0]} Sir...")
                            os.system(f'open "{app[1]}"')
                            app_opened = True
                            break
                    if app_opened:
                        continue

                    # Play music
                    if "play songs" in query.lower() or "play music" in query.lower():
                        musicPath = "/Users/arghdas/Downloads/Musics"
                        if not os.path.exists(musicPath):
                            print("Music directory not found.")
                            say("Music directory not found, Sir.")
                            continue
                        songs = os.listdir(musicPath)
                        if not songs:
                            print("No songs found in the directory.")
                            say("No songs found in the directory, Sir.")
                            continue
                        song = random.choice(songs)
                        song_path = os.path.join(musicPath, song)
                        os.system(f'open "{song_path}"')
                        print(f"Playing {song}, Sir.")
                        say(f"Playing {song}, Sir.")
                        continue

                    # Tell the time
                    if "the time" in query.lower():
                        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                        print(f"Sir, the time is: {strfTime}")
                        say(f"Sir, the time is {strfTime}")
                        continue

                    # Using AI to respond
                    if "using artificial intelligence" in query.lower():
                        response_text = ai(prompt1=query)
                        print("Full AI Response:")
                        print(response_text)  # Display full response

                        say("The information has been saved in Jarvis prompts, Sir.")
                        # Optionally, you can still speak a summary
                        # summarized_response = summarize(response_text)
                        # say(summarized_response)

                        texts = f"Jarvis response for the prompt: {query} \n ************************\n\n"
                        texts += response_text

                        # Ensure the directory exists
                        os.makedirs("Jarvisprompts", exist_ok=True)

                        # Clean the file name
                        file_name = ''.join(query.split('intelligence')[1:]).strip()
                        file_name = ''.join(filter(lambda x: x.isalnum() or x.isspace(), file_name)).replace(' ', '_')
                        file_path = f"Jarvisprompts/{file_name}.txt"

                        with open(file_path, "w") as f:
                            f.write(texts)
                        continue

                    # General AI Chat
                    response_chat = chat(query)
                    print("Full AI Response:")
                    print(response_chat)  # Display full response

                    # Summarize the response for speaking
                    summarized_response = summarize(response_chat)
                    print("Summarized Response:")
                    print(summarized_response)

                    # Speak the summarized response
                    say(summarized_response)

                except Exception as e:
                    print(f"Sir, I didn't get what you said. Error: {e}")
                    say(f"Sir, I didn't get what you said. Please try again.")

