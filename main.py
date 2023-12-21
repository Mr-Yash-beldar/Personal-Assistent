import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import os
import pywhatkit
import webbrowser
import openai
import pywhatkit
import datetime
apikey="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"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Yash: {query}\n Assistant: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,    
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Delta"

def start_listening():
    def listen():
        while True:
            print("Listening...")
            query = takeCommand()
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ["twitter", "https://www.twitter.com"]]
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
            if "play" in query:
                search_query = query[4:]  # Extract the query after "play "
                say(f"Playing {search_query} on YouTube for you Yash...")
                pywhatkit.playonyt(search_query)
            elif "the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Sir The Time is {hour} hours and {min} minutes")

            elif "open brave".lower() in query.lower():
                say("Opening Brave for you Yash..")
                os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Brave")

            elif "open code".lower() in query.lower():
                os.startfile("C:\\Users\\yasho\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk")

            elif "sleep".lower() in query.lower():
                os.system("rundll32.exe user32.dll,LockWorkStation")

            elif "shutdown".lower() in query.lower():
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

            elif "Using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
            elif "Assistant Quit".lower() in query.lower():
                exit()
            elif "reset chat".lower() in query.lower():
                global chatStr
                chatStr = ""
            else:
                print("Chatting...")
                chat(query)

    listening_thread = threading.Thread(target=listen)
    listening_thread.daemon = True
    listening_thread.start()

def create_window():
    root = tk.Tk()
    root.title("Assistant GUI")
    root.geometry('400x400')  # Setting the window size to 10x10cm

    def on_start_button_click():
        start_listening()

    def on_stop_button_click():
        root.destroy()  # Close the window and terminate the program

    start_button = tk.Button(root, text="Listen", command=on_start_button_click, width=10, height=2)
    start_button.pack(pady=10)  # Increase padding between buttons

    stop_button = tk.Button(root, text="Stop", command=on_stop_button_click, width=10, height=2)
    stop_button.pack(pady=10)  # Increase padding between buttons

    root.mainloop()

# Modify your main function to call this new window creation function
if __name__ == "__main__":
    create_window()



