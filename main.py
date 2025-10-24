import datetime
import os
import random
import webbrowser
from time import time as t
import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv




#Api Model
def configure1(api_key):
    load_dotenv()
configure1(None)

api_key = os.getenv('api_key')

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

#chat_session = model.start_chat(
messages = [
    {

        "parts": [
            {
                "text": "You are a Powerful A.I Assistant Named Jarvis, created by Tony Stark. Talk like a human, the user giving inputs is Tony Stark and always use Sir or Mr.Das or Argh Das before speaking and don't ever use Tony Stark or Mr. Stark always use Argh Das or Mr. Das, Argh Das is Tony Stark"
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
#)

response = model.generate_content(messages)


#print(response.text)


#End of the model


#Jarvis_Voice_Engine

# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[0].id)
# rate = engine.setProperty("rate",170)

def say(text):
    os.system(f'say -v "Daniel" "{text}"')



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


chatstr = ""


def chat(query, chatstr=""):
    chatstr += f"Tony:{query}\n Jarvis: "
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
    elif f"open {app_name[0]}".lower() in query.lower():
        return ""

    response = model.generate_content(messages)

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


#print(response.text)
#say(response.text)


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

        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occured. Sorry Sir"


if __name__ == "__main__":
    while True:
        print("Friday Online, Please say the security phrase to activate Friday")
        say("Friday Online, Please say the security phrase to activate Friday")
        print("Listening...")
        query = take_command()
        if "wake up friday daddy".lower() in query.lower():
            from Greetme import greetme

            greetme()
        # elif "jarvis you up".lower() in query.lower():
        #     print("For you sir, Always..... \nWhat can i do for you ?")
        #     say("For you sir, Always..... \nWhat can i do for you ?")

            while True:
                print("Listening...")
                query = take_command()

                if "Friday go offline".lower() in query.lower() or "Friday offline".lower() in query.lower():
                    say("Going offline, Sir")
                    print("Going offline, Sir")
                    exit()
                elif "reset chat".lower() in query.lower():
                    chatstr = ""
                    print("Done Sir, As per your instructions all the previous chat has been deleted")
                    say("Done Sir, As per your instructions all the previous chat has been deleted")

                elif "go to sleep".lower() in query.lower():
                    say("Going to sleep, Sir")
                    print("Going to sleep, Sir")
                    break
                try:
                    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                             ["google", "https://www.google.com"], ["spotify", "https://www.spotify.com"],
                             ["instagram", "https://www.instagram.com"]]
                    for site in sites:
                        if f"Open {site[0]}".lower() in query.lower():
                            # say(f"Opening {site[0]} Sir...")
                            print(f"Opening {site[0]} Sir...")
                            webbrowser.open(site[1])
                            continue

                    if "play songs".lower() in query.lower() or "play music".lower() in query.lower():
                        musicPath = "/Users/arghdas/Downloads/Musics"
                        song = os.listdir(musicPath)
                        random_index = random.randint(0, len(song) - 1)
                        song_path = os.path.join(musicPath, song[random_index])
                        # say("playing songs sir...")
                        os.system(f'open "{song_path}"')
                        print("Playing songs, Sir")
                        say("Playing songs, Sir")
                        continue

                    elif "the time".lower() in query.lower():
                        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                        print(f"Sir, the time is: {strfTime}")
                        say(f"Sir, the time is {strfTime}")
                        continue

                    apps_v1 = [["weather", "/System/Applications/Weather.app"],
                               ["facetime", "/System/Applications/FaceTime.app"],
                               ["maps", "/System/Applications/Maps.app"],
                               ["messages", "/System/Applications/Messages.app"]]
                    for app_name in apps_v1:
                        if f"open {app_name[0]}".lower() in query.lower():
                            say(f"Opening {app_name[0]} Sir...")
                            print(f"Opening {app_name[0]} Sir...")
                            os.system(f'open "{app_name[1]}"')
                            continue
                    # query1 = query
                    if "using artificial intelligence".lower() in query.lower():
                        response_text = ai(prompt1=query)
                        C = t()
                        print(t() - C)
                        print(response_text)
                        say("The information has been saved in jarvis prompts, Sir")
                        # say(response_text)

                        texts = f"Jarvis response for the prompt: {query} \n ************************\n\n"
                        texts += response_text

                        # if not os.path.exists("Jarvisprompts"):
                        #     os.mkdir("Jarvisprompts")

                        file_name = ''.join(query.split('intelligence')[1:]).split()
                        file_name = ''.join(filter(lambda x: x.isalnum() or x.isspace(), file_name))
                        file_path = f"Jarvisprompts/{file_name}.txt"

                        with open(file_path, "w") as f:
                            f.write(texts)
                            continue
                    else:
                        response_chat = chat(query)
                        print(response_chat)
                        say(response_chat)
                except Exception as e:
                    print(f"Sir, I didn't got what you said, Please Say that again {e}")
