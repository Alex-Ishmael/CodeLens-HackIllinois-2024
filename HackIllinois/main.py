# python3 HackIllinois/main.py --command "python3 HackIllinois/Test.py"

import sys
import os
import argparse
import traceback
import subprocess
import re

def run_command(command):
    print("Parent",os.getpid())
    try:
        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sp.communicate()
        if sp.returncode != 0:
            print(f"An error occurred while executing")
            print("Traceback:")
            print(err.decode())
            match = re.search(r'File "([^"]+)", line (\d+),', err.decode())
            if match:
                filename, line_number = match.group(1), match.group(2)
                print(f"Error occurred in {filename}, line {line_number}")
                with open(filename) as file:
                    lines = file.readlines()
                    start = max(0, int(line_number) - 5)
                    end = min(len(lines), int(line_number) + 5)
                    for i, line in enumerate(lines[start:end], start + 1):
                        if (i == int(line_number)):
                            print(f"--> {i}: {line.strip()}")
                        else:
                            print(f"    {i}: {line.strip()}")
            else:
                print("Line number information not found in the traceback.")
                # You can also parse the stderr to extract specific error messages or line numbers
    except Exception as e:
        print(f"An exception occurred while executing: \n{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Linux command')
    parser.add_argument('--command', metavar='command', type=str, required=True, help='The Linux command to run')

    args = parser.parse_args()
    print(args.command)
    run_command(args.command)
    
