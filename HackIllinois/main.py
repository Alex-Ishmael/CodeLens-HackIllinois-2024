# python3 HackIllinois/main.py --command "python3 HackIllinois/Test.py"

history_dir = "history"

import sys
import os
import psutil
import argparse
import traceback
import subprocess
import datetime
import time
import re
import gemini
import pyfiglet

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def update_history(args) :
    if not os.path.isfile("HackIllinois/history/history_contents.txt") :
        f = open("HackIllinois/history/history_contents.txt", "x")

    f = open("HackIllinois/history/history_contents.txt", "a")
    f.write(str(args)+"\n")
    f.close()

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_next_filename(directory, base_name='run', extension='txt'):
    files = [f for f in os.listdir(directory) if f.startswith(base_name) and f.endswith(f".{extension}")]

    if not files:
        file_path = os.path.join(directory, f"{base_name}1.{extension}")
        return file_path

    file_numbers = [int(file[len(base_name):-len(f'.{extension}')]) for file in files]
    next_file_number = max(file_numbers) + 1
    file_path = os.path.join(directory, f"{base_name}{next_file_number}.{extension}")

    return file_path


def measure_max_memory(pid):
    process = psutil.Process(pid)
    max_memory = 0
    done = False
    while not done:
        try:
            memory_info = process.memory_info().rss/ 1024 ** 2
            max_memory = max(max_memory, memory_info)
            time.sleep(0.1)
        except:
            done = True
            return max_memory

    return max_memory

def run_command(command, output):

    try:
        start_time = datetime.datetime.now()
        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        max_mem = measure_max_memory(sp.pid)
        result = pyfiglet.figlet_format("CODE LENS", font="slant") 
        print(bcolors.OKCYAN,"\n",result,"\n") 
        time.sleep(2)
        print(bcolors.OKGREEN,"Memory: ",max_mem, " MB",bcolors.ENDC)
        output.write("Memory: " + str(max_mem) + " MB\n")
        out, err = sp.communicate()
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(bcolors.OKGREEN, "Execution time: ",duration.microseconds/1000," ms",bcolors.ENDC)
        output.write("Execution time: " + str(duration.microseconds/1000) + " ms\n")
        if sp.returncode != 0:
            print(bcolors.WARNING,"An error occurred while executing",bcolors.ENDC)
            print(bcolors.FAIL,err.decode(),bcolors.ENDC)
            output.write("An error occurred while executing\n")
            output.write(err.decode() + "\n")
            lines = err.decode().strip().split('\n')
            error_message = lines[-1]
            match = re.search(r'File "([^"]+)", line (\d+), (.+)', err.decode())
            if match:
                filename, line_number = match.group(1), int(match.group(2))
                print(bcolors.WARNING,f"The following error occurred in your code: {error_message}",bcolors.ENDC)
                print(bcolors.WARNING,f"This error occurred in {filename} at line {line_number}",bcolors.ENDC)
                print(bcolors.WARNING, "Start looking for bugs in the following section: \n")
                output.write(f"This error occurred in {filename} at line {line_number}\n")
                output.write("Start looking for bugs in the following section: \n")         
                code = []
                with open(filename) as file:
                    lines = file.readlines()
                    start = max(0, int(line_number) - 5)
                    end = min(len(lines), int(line_number) + 5)
                    for i, line in enumerate(lines[start:end], start + 1):
                        code.append(line.strip())
                        if (i == int(line_number)):
                            print(bcolors.FAIL, f"--> {i}: {line.strip()}",bcolors.ENDC)
                            output.write(f"--> {i}: {line.strip()}\n")
                        else:
                            print(bcolors.OKGREEN, f"    {i}: {line.strip()}",bcolors.ENDC)
                            output.write(f"    {i}: {line.strip()}\n")
                # AI section
                print(bcolors.BOLD +"\nWhat your error means:" + bcolors.ENDC)
                out1 = gemini.error_lookup(str(error_message))
                print(bcolors.BOLD + "\nHere's some tips on what you can do for your specific code:"+ bcolors.ENDC)
                out2 = gemini.tips(str(error_message), code)
                print(bcolors.BOLD + "\nHere's some resources to learn more:"+ bcolors.ENDC)
                out3 = gemini.links(str(error_message), code)
                output.write("\nWhat your error means:\n")
                output.write(str(out1) + "\n")
                output.write("\nHere's some tips on what you can do for your specific code:\n")
                output.write(str(out2) + "\n")
                output.write("\nHere's some resources to learn more:\n")
                output.write(str(out3) + "\n")
            else:
                print("Line number information not found in the traceback.")
                output.write("Line number information not found in the traceback.\n")
                # You can also parse the stderr to extract specific error messages or line numbers
        else:
            print(bcolors.BOLD,"Output: ",out.decode())
            output.write("Output: " + out.decode() + "\n")
    except Exception as e:
        # print(f"An exception occurred while executing: \n{e}")
        output.write(f"An exception occurred while executing: \n{e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Linux command')
    parser.add_argument('--command', metavar='command', type=str, required=True, help='The Linux command to run')

    args = parser.parse_args()
    create_directory_if_not_exists(history_dir)
    filename = get_next_filename(history_dir)
    # print(args.command)
    file = open(filename, 'a')
    run_command(args.command, file)
    file.close()
    
    print(bcolors.BOLD + "See the full report:"+ bcolors.ENDC, filename, "\n")
    