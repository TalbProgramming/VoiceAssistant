
import pyttsx3
import speech_recognition as sr
import openai

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


def stt(recording: sr.AudioData):
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
        read_string("I could not understand you")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        read_string("Error, restart the app please")


def activate_assistant(mic):
    print("Activation function... ")
    # listens and waits until the user has called the AI name ('name.txt') and "activates" the assistant if so.
    with open('name.txt', 'r') as f:
        while True:
            print("Listening... ")
            audio = r.listen(mic)  # starts and stops recording by default silence time
            generated_text = stt(audio)

            try:
                # if the user called the AI name (inside 'name.txt')
                if f.readline().strip() in generated_text:
                    print("Confirmed name... ")
                    read_string("ask me anything")
                    # return to main
                    break
            except TypeError:
                pass


# connection with openAI API
openai.api_key = "MY_API_KEY"

# setup audio and speech recognizer instance
r = sr.Recognizer()

with sr.Microphone() as source:
    while True:
        activate_assistant(source)

        print("listening to user question...")
        user_q = r.listen(source)  # listening for user question
        user_q_text = stt(user_q)
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

        print(response.choices[0].text)
        read_string(response.choices[0].text)
