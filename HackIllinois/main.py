# python3 HackIllinois/main.py --command "python3 HackIllinois/Test.py"

history_dir = "HackIllinois/history"

import sys
import os
import psutil
import argparse
import traceback
import subprocess
import datetime
import time
import re

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

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def get_next_filename(directory, base_name='run', extension='txt'):
    files = [f for f in os.listdir(directory) if f.startswith(base_name) and f.endswith(f".{extension}")]

    if not files:
        return f"{base_name}1.{extension}"

    file_numbers = [int(file[len(base_name):-len(f'.{extension}')]) for file in files]
    next_file_number = max(file_numbers) + 1

    return f"{base_name}{next_file_number}.{extension}"


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

def run_command(command):

    try:
        start_time = datetime.datetime.now()
        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(bcolors.OKGREEN,"Memory: ",measure_max_memory(sp.pid), "MB", bcolors.ENDC)
        out, err = sp.communicate()
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print(bcolors.OKGREEN, "Execution time: ",duration.microseconds/1000,"ms", bcolors.ENDC,"\n")
        if sp.returncode != 0:
            print(bcolors.FAIL,"An error occurred while executing",bcolors.ENDC)
            print(bcolors.FAIL,err.decode(),bcolors.ENDC)
            match = re.search(r'File "([^"]+)", line (\d+),', err.decode())
            if match:
                filename, line_number = match.group(1), match.group(2)
                print(bcolors.WARNING,f"Error occurred in {filename}, line {line_number}",bcolors.ENDC)
                with open(filename) as file:
                    lines = file.readlines()
                    start = max(0, int(line_number) - 5)
                    end = min(len(lines), int(line_number) + 5)
                    for i, line in enumerate(lines[start:end], start + 1):
                        if (i == int(line_number)):
                            print(bcolors.FAIL,f"--> {i}: {line.strip()}", bcolors.ENDC)
                        else:
                            print(bcolors.OKGREEN,f"    {i}: {line.strip()}",bcolors.ENDC)
            else:
                print("Line number information not found in the traceback.")
                # You can also parse the stderr to extract specific error messages or line numbers
        else:
            print("Output: ",out)
    except Exception as e:
        print(f"An exception occurred while executing: \n{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Linux command')
    parser.add_argument('--command', metavar='command', type=str, required=True, help='The Linux command to run')

    args = parser.parse_args()
    print(bcolors.HEADER,"Executed command: ", args.command, bcolors.ENDC,"\n")
    run_command(args.command)
    create_directory_if_not_exists(history_dir)
    print(get_next_filename(history_dir))
    
