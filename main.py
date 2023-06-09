
import os
import pyttsx3
import speech_recognition as sr
import openai
from datetime import date

"""
Required installations (pip):
* pyttsx3
* SpeechRecognition
* pyAudio (needed for the SpeechRecognition functionality,
  if you get and error with "wheels", install directly from PYPI
* openAI
** payment for openAI "davinci" model usage - https://openai.com/api/pricing/
"""

"""
Things to add: 
- History option
- UI
"""


def read_string(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def stt(recording: sr.AudioData) -> str:
    print("STT function...")
    # receives a recording and returns text
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`

        # generating the text from recording
        output_text = r.recognize_google(recording)
        print(f"The program thinks you said: \n>>>\t\t {output_text}")
        return output_text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        # read_string("I could not understand you")
        pass

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        read_string("Error, restart the app please")


def activate_assistant(mic):
    print("Activation function... ")
    # listens and waits until the user has called the AI name ('name.txt') and "activates" the assistant if so.
    with open('name.txt', 'r') as f:
        name = f.readline().strip()

    while True:
        print("Listening... ")
        audio = r.listen(mic)  # starts and stops recording by default silence time
        generated_text = stt(audio)

        try:
            # if the user called the AI name (inside 'name.txt')
            if name in generated_text:
                print("Confirmed name... ")
                read_string("ask me anything")
                # return to main
                break
        except TypeError:
            pass


def date_check():
    current_date = str(date.today())

    with open("history.txt", 'r') as hfile:
        all_lines = hfile.readlines()

    # check if the file is empty
    if not all_lines:
        with open("history.txt", 'a') as hfile:
            hfile.write(f"<date>\n{current_date}\n")
            return  # leave the function

    """
    because there is a '\n' at the end of each line of the file, every item in all_lines will have one,
    thus, we must remove it.
    """
    all_lines = [line.strip() for line in all_lines]

    # search for the last time the user used the program
    all_lines.reverse()
    last_date = ""  # the last date the program was used
    for index, value in enumerate(all_lines):
        if value == "<date>":
            last_date = all_lines[index-1]  # the previous line is the date itself
            break

    if last_date != current_date:
        with open("history.txt", 'a') as hfile:
            hfile.write(f"<date>\n{current_date}\n")  # add the current date to the history file


# connection with openAI API
openai.api_key = os.environ.get("OPENAI_KEY")

# setup audio and speech recognizer instance
r = sr.Recognizer()

# check for the date, add a date if needed
date_check()

with sr.Microphone() as source:
    while True:
        activate_assistant(source)

        print("listening to user question...")
        while True:
            user_q = r.listen(source)  # listening for user question
            user_q_text = stt(user_q)
            if user_q_text is not None:
                break

        # add the user question to history.txt file
        with open("history.txt", 'a') as hfile:  # option 'a' in order to write to the end of the file
            hfile.write("<question>\n")
            hfile.write(user_q_text + "\n")

        print(f"user question > {user_q_text}")

        # Sending the received text to chatGPT
        response = openai.Completion.create(
            model="text-davinci-003",  # chatGPT model
            prompt=user_q_text,
            temperature=0.3,  # creativeness
            max_tokens=150,
            frequency_penalty=0.0,  # recurrence of sentences
            presence_penalty=0.6,  # less repetitiveness
        )

        # add the response to history.txt file
        with open("history.txt", 'a') as hfile:  # option 'a' in order to write to the end of the file
            hfile.write("<response>\n")
            # the response will always start with \n\n, so we do [2:] do to remove it.
            hfile.write(response.choices[0].text[2:] + "\n")

        print(response.choices[0].text)
        read_string(response.choices[0].text)
