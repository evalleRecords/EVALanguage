import speech_recognition as sr

def listen_from_mic():
    """Listens to the microphone and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Use Google Web Speech API for recognition
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == "__main__":
    user_input_text = listen_from_mic()
    if user_input_text:
        print(f"Processed input: {user_input_text}")
        # In a full application, you would send user_input_text to an AI here
