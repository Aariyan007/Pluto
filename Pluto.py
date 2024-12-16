import os
import datetime
import sys
from time import sleep

import speech_recognition as sr
import webbrowser
import pyaudio
import numpy as np
import time
from config import passkey
from config import passkey_2
from Api import search_api
import config
import pywhatkit as kit
import urllib.request

# Function to use macOS "say" command for text-to-speech
def send_whatsapp_message(number, message):
    try:
        # Send message instantly
        kit.sendwhatmsg_instantly(number, message)
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def schedule_message(time_str, number, message):
    try:
        # Check if the time format is "HH:MM" or "HHMM"
        if len(time_str) == 4:
            hours = int(time_str[:2])
            minutes = int(time_str[2:])
        else:
            hours, minutes = map(int, time_str.split(':'))

        # Schedule message
        kit.sendwhatmsg(number, message, hours, minutes)
        return True
    except Exception as e:
        print(f"Error scheduling message: {e}")
        return False


def search_youtube(video_name):
    if video_name:

        base_url = "https://www.youtube.com/results"
        query_string = urllib.parse.urlencode({"search_query": video_name})
        search_url = f"{base_url}?{query_string}"


        print(f"Searching YouTube for: {video_name}")
        webbrowser.open(search_url)
    else:
        return False

def say(text, voice="Daniel"):
    escaped_text = text.replace('"', '\\"').replace("'", "\\'")
    os.system(f"say -v {voice} \"{escaped_text}\"")

def detect_clap(threshold=20000, duration=2):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening for claps...")
    clap_detected = False
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        peak = np.abs(data).max()
        if peak > threshold:
            clap_detected = True
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    return clap_detected

# Function to take voice command and recognize it as text
def takeCommand():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            print("Listening...")
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your voice."
    except sr.RequestError:
        return "Speech recognition service is unavailable."
    except Exception as e:
        print(f"Error: {e}")
        return "Error occurred while processing your voice."

# Function to verify the passkey
def verify_passkey():
    say("Please say your passkey to continue", voice="Daniel")
    passkey_input = takeCommand().lower().strip()
    if passkey_input == passkey.lower() or passkey_2 in passkey_input:
        say("Passkey verified. You may proceed.", voice="Daniel")
        return True
    else:
        say("Incorrect passkey. Access denied.", voice="Daniel")
        return False

def name_whatsapp(name):
    names = {

    }
    name = name.lower()
    return names.get(name, None)

if __name__ == '__main__':
    say("SYSTEMS GETTING READY SIR......PLEASE WAIT", voice="Daniel")
    time.sleep(2)
    say("Sir, activation ready.", voice="Daniel")

    # Verify passkey only once
    if verify_passkey():
        while True:
            if detect_clap():  # Wait for a clap to trigger interaction
                say("Hi Sir, Pluto on command and ready for activation", voice="Daniel")

                query = takeCommand().lower().strip()

                if not query:
                    say("No command detected. Please try again.", voice="Daniel")
                    continue

                if "open google" in query:
                    say("Alright Sir... Opening Google", voice="Daniel")
                    webbrowser.open("https://google.com")

                elif "open youtube" in query or "i want to watch a video" in query:
                    say("Sure Sir...", voice="Daniel")
                    say("What do you want to watch?", voice="Daniel")

                    while True:

                        query_youtube = takeCommand().lower().strip()
                        if query_youtube:
                            say(f"Searching YouTube for {query_youtube}...", voice="Daniel")
                            search_youtube(query_youtube)
                            break

                        else:
                            say("I didn't catch that. Please tell me again.", voice="Daniel")


                elif "open facebook" in query:
                    say("Alright Sir... Opening Facebook", voice="Daniel")
                    webbrowser.open("https://www.facebook.com")

                elif "open twitter" in query:
                    say("Sure Sir... Hope something good to tweet", voice="Daniel")
                    webbrowser.open("https://www.twitter.com")

                elif "open linkedin" in query:
                    say("Want some job openings, Sir?", voice="Daniel")
                    webbrowser.open("https://www.linkedin.com")

                elif "open instagram" in query:
                    say("Sure Sir... Opening Instagram", voice="Daniel")
                    webbrowser.open("https://www.instagram.com")

                elif "open reddit" in query:
                    say("Opening Reddit... Sir, Reddit has heavy traffic", voice="Daniel")
                    webbrowser.open("https://www.reddit.com")

                elif "open amazon" in query:
                    say("Opening Amazon... What do you wish to buy, Sir?", voice="Daniel")
                    webbrowser.open("https://www.amazon.com")

                elif "open netflix" in query:
                    say("Sure Sir... Sit back and relax", voice="Daniel")
                    webbrowser.open("https://www.netflix.com")

                elif "open wikipedia" in query:
                    say("Opening Wikipedia for you", voice="Daniel")
                    webbrowser.open("https://www.wikipedia.org")

                elif "search github" in query or "find github user" in query:
                    say("Sure Sir...", voice="Daniel")
                    say("What is the GitHub username?", voice="Daniel")

                    while True:

                        github_user = takeCommand().lower().strip()

                        if github_user:
                            say(f"Searching GitHub for user {github_user}...", voice="Daniel")

                            github_url = f"https://github.com/{github_user}"

                            webbrowser.open(github_url)
                            break

                        else:
                            say("I didn't catch that. Please tell me the GitHub username again.", voice="Daniel")


                elif "open spotify" in query:
                    say("Opening Spotify for music", voice="Daniel")
                    os.system("open -a spotify")


                elif "open quora" in query:
                    say("Sure Sir... Opening Quora", voice="Daniel")
                    webbrowser.open("https://www.quora.com")

                elif "open pinterest" in query:
                    say("Opening Pinterest for you", voice="Daniel")
                    webbrowser.open("https://www.pinterest.com")

                elif "open tiktok" in query:
                    say("Opening TikTok for you", voice="Daniel")
                    webbrowser.open("https://www.tiktok.com")

                elif "open safari" in query:
                    say("Opening Safari for you", voice="Daniel")
                    os.system("open -a Safari")

                elif "open mail" in query:
                    say("Opening Mail for you", voice="Daniel")
                    os.system("open -a Mail")

                elif "open messages" in query:
                    say("Opening Messages", voice="Daniel")
                    os.system("open -a Messages")

                elif "open whatsapp" in query or "i want to text someone" in query or "i want to send a message" in query:
                    say("Sir, would you like me to send a message, or would you prefer to send it yourself?",
                        voice="Daniel")
                    query1 = takeCommand().lower().strip()

                    if "i will" in query1 or "no" in query1 or "just open" in query1 or "myself" in query1:
                        say("Yes, Sir. I am opening WhatsApp for you.", voice="Daniel")
                        os.system("open -a WhatsApp")
                    else:
                        say("Whom would you like to send a message to, Sir?..........", voice="Daniel")
                        name = takeCommand().lower().strip()

                        num = name_whatsapp(name)

                        if num is None:
                            say("I'm sorry, Sir. I couldn't find the contact you requested.", voice="Daniel")
                        else:
                            say(f"Sending message to {name}, Sir.", voice="Daniel")
                            say(f"what would you like me to send,Sir?", voice="Daniel")
                            message_query = takeCommand().lower().strip()

                            while True:
                                say(f"Sir, would you like me to send the message now or schedule it for later?",
                                    voice="Daniel")
                                schedule_query = takeCommand().lower().strip()

                                if "now" in schedule_query or "send now" in schedule_query:
                                    if send_whatsapp_message(num, message_query):
                                        say(f"Message sent to {name}.", voice="Daniel")
                                    else:
                                        say("Sorry, I couldn't send the message.", voice="Daniel")
                                        break
                                    break
                                elif "later" in schedule_query or "schedule" in schedule_query:
                                    say(f"At what time would you like to schedule the message?", voice="Daniel")
                                    time_query = takeCommand().lower().strip()

                                    if schedule_message(time_query, num, message_query):
                                        say(f"Your message to {name} has been scheduled for {time_query}.",
                                            voice="Daniel")
                                    else:
                                        say("Sorry, I couldn't schedule the message.", voice="Daniel")
                                    break
                                else:
                                    say(f"Sorry, I didn't understand.",voice="Daniel")

                elif "open calendar" in query:
                    say("Opening Calendar for you", voice="Daniel")
                    os.system("open -a Calendar")

                elif "open finder" in query:
                    say("Opening Finder for you", voice="Daniel")
                    os.system("open -a Finder")

                elif "open notes" in query:
                    say("Opening Notes for you", voice="Daniel")
                    os.system("open -a Notes")

                elif "open music" in query:
                    say("Opening Music for you", voice="Daniel")
                    os.system("open -a Music")

                elif "open photos" in query:
                    say("Opening Photos... You don't have many memories, Sir", voice="Daniel")
                    os.system("open -a Photos")

                elif "open visual studio" in query or "i want to build something" in query:
                    say("Yes sir,Just a second sir...getting things ready!", voice="Daniel")
                    sleep(1)
                    say("Is this a Vite project you want to create?", voice="Daniel")
                    response = takeCommand().lower().strip()

                    if "yes" in response or "vite" in response:
                        say("What should we name the project?", voice="Daniel")
                        project_name = takeCommand().lower().strip()

                        if project_name:
                            say(f"Creating a Vite project named {project_name}. Please wait...", voice="Daniel")
                            import os

                            os.system(f"npm create vite@latest {project_name} -- --template react")
                            os.system(f"cd {project_name} && npm install")
                            say(f"Opening {project_name} in Visual Studio Code.", voice="Daniel")
                            os.system(f"code {project_name}")
                        else:
                            say("I couldn't catch the project name. Please try again.", voice="Daniel")
                    else:
                        os.system("open -a 'Visual Studio Code'")


                elif "what is the time" in query or "what's the time" in query or "time" in query:
                    strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                    say(f"Sir, the time is {strfTime}", voice="Daniel")

                elif "Thank you" in query or "stop" in query:
                    say("Bye Sir", voice="Daniel")
                    break
                elif "sleep" in query or "switch off" in query:
                    say(f"Going to sleep...",voice="Daniel")
                    os.system("pmset sleep")
                else:
                    say(f"Just a second sir.....I am facing issues...I will respond soon ", voice="Daniel")
                    gemini_message = search_api(query)
                    say(gemini_message, voice="Daniel")
    else:
        say("Exiting the program due to incorrect passkey.", voice="Daniel")