import config
import openai
import sys
import subprocess


import platform
import os

# Get the system information
system = platform.system()
release = platform.release()
version = platform.version()
machine = platform.machine()
processor = platform.processor()

# Concatenate the information into a single string
sysinfo = "System: " + system + "\n" + "Release: " + release + "\n" + "Version: " + version + "\n" + "Machine: " + machine + "\n" + "Processor: " + processor


def convert_to_bash(instructions):
    # Use OpenAI's API key to access GPT-3
    openai.api_key = config.OPENAI_API_KEY

    # Define the prompt for GPT-3
    prompt = "Context:" + sysinfo + ". Convert the following instructions into bash code:\n" + instructions

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

# Get the input instructions from the terminal
input_instructions = input("Enter a set of instructions: ")

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
