import subprocess
import requests # For making HTTP requests to the TartuNLP API
import os       # For handling file paths
from gtts import gTTS # For Google Text-to-Speech (English)

def estonian_tts_tartunlp(text, speaker="mari", speed=1.0, output_filename="tartunlp_output.wav"):
    """
    Generates Estonian speech from text using the TartuNLP Text-to-Speech API.

    Args:
        text (str): The Estonian text to convert to speech.
        speaker (str, optional): The speaker voice. Defaults to "mari".
                                 Available speakers include: "mari", "tambet", "liivika", "kalev",
                                 "külli", "meelis", "albert", "indrek", "vambola", "eva".
        speed (float, optional): Speaking speed. Defaults to 1.0.
                                 Values typically between 0.5 (slower) and 2.0 (faster).
        output_filename (str, optional): The filename to save the generated audio.
                                         Defaults to "tartunlp_output.wav".
    Returns:
        bool: True if speech was generated and saved successfully, False otherwise.
    """
    api_url = "https://api.tartunlp.ai/text-to-speech/v2"
    payload = {
        "text": text,
        "speaker": speaker,
        "speed": speed
    }
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Attempting to generate speech via TartuNLP API: \"{text}\" (Speaker: {speaker}, Speed: {speed})")

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60) # Increased to 60-second timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        # Save the audio content to a file
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"Speech audio saved to {output_filename}")

        # Attempt to play the audio using aplay (common on Linux)
        try:
            print(f"Attempting to play {output_filename} using aplay...")
            # Ensure output_filename is an absolute path if needed, or aplay is in PATH
            subprocess.run(['aplay', output_filename], check=True)
            print("Playback finished.")
        except FileNotFoundError:
            print("Could not find 'aplay' to play the audio. Please play it manually.")
            print("  (aplay is common on Linux. For other OS, you might need a different player.)")
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio with aplay: {e}")
        
        return True

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred with TartuNLP API: {e.response.status_code} - {e}")
        print(f"Response content from API: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to TartuNLP API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return False

def english_tts_gtts(text, lang='en', output_filename="gtts_english_output.mp3"):
    """
    Generates English speech from text using the gTTS library (Google Translate's TTS).
    Does not require an API key for basic use.

    Args:
        text (str): The English text to convert to speech.
        lang (str, optional): The language code. Defaults to 'en' for English.
        output_filename (str, optional): The filename to save the generated audio.
                                         Defaults to "gtts_english_output.mp3".
    Returns:
        bool: True if speech was generated and saved successfully, False otherwise.
    """
    try:
        print(f"Attempting to generate English speech via gTTS: \"{text[:70]}...\"")
        tts = gTTS(text=text, lang=lang)
        tts.save(output_filename)
        print(f'English audio content (gTTS) saved to file "{output_filename}"')

        # Attempt to play the audio using mpg123 (good for MP3s on Linux)
        try:
            print(f"Attempting to play {output_filename} using mpg123...")
            # Ensure mpg123 is installed: sudo apt install mpg123
            subprocess.run(['mpg123', output_filename], check=True)
            print("Playback finished.")
        except FileNotFoundError:
            print(f"Could not find 'mpg123' to play the audio. Please play '{output_filename}' manually.")
            print("  (Install with: sudo apt install mpg123)")
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio with mpg123: {e}")
        return True

    except Exception as e:
        print(f"An error occurred with gTTS: {e}")
        return False



if __name__ == "__main__":
    #Lesson #1
    story = "Tere Edward!"
    tartunlp_text_1 = "Tere, see on test Tartu Neurokõne API kaudu."
    estonian_tts_tartunlp(tartunlp_text_1, speaker="mari")
    print("-" * 30)

    tartunlp_text_2 = "Tere, hommikust Edward!."
    estonian_tts_tartunlp(tartunlp_text_2, speaker="vesta")
    print("-" * 30)

    english_text_1 = "Hello, Edward"
    english_tts_gtts(english_text_1)
    print("-" * 30)
