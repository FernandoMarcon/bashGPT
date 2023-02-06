import config
import openai
import subprocess
import tempfile
import speech_recognition as sr
import keyboard

def convert_to_bash(instructions):
    # Use OpenAI's API key to access GPT-3
    openai.api_key = config.OPENAI_API_KEY

    # Define the prompt for GPT-3
    prompt = "I am using arch linux. Convert the following instructions into bash code:\n" + instructions

    # Generate the response using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    return response

# Record the audio input through the microphone
r = sr.Recognizer()

def listen_keyboard(r, source):
    with sr.Microphone() as source:
        print("Speak your instructions:")
        audio = r.listen(source, phrase_time_limit=5)
        return audio

with sr.Microphone() as source:
    print("Speak your instructions:")
    audio = None
    while True:
        if keyboard.is_pressed('space'):
            break
        elif keyboard.is_pressed('enter'):
            break
        else:
            audio = listen_keyboard(r, source)

# Save the audio to a temporary file
with tempfile.NamedTemporaryFile(prefix="instructions_", suffix=".wav", delete=False) as f:
    f.write(audio.get_wav_data())
    file_name = f.name

# Transcribe the audio to text using the Google Speech API
try:
    input_instructions = r.recognize_google(audio)
    print("You said: " + input_instructions)
except sr.UnknownValueError:
    print("Google Speech API could not understand the audio")
except sr.RequestError as error:
    print("Could not request results from Google Speech API; {0}".format(error))

# Generate the bash code
output_code = convert_to_bash(input_instructions)

# Output the generated bash code
print("Bash code:")
print(output_code)

# Run the generated bash code
try:
    result = subprocess.run(output_code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(result.stdout.decode())
except subprocess.CalledProcessError as error:
    print(error.stderr.decode())

# Remove the temporary audio file
subprocess.run(["rm", file_name], shell=True)
