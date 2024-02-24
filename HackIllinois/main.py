# python3 HackIllinois/main.py --command "python3 HackIllinois/Test.py"

import sys
import os
import argparse
import traceback
import subprocess
import gemini as gm

def run_command(command):
    print("Parent",os.getpid())
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    print("Pid: ",sp.pid)
    print("Output: ",out)
    print("Error: ",err)
    gm.error_lookup(str(err));

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Linux command')
    parser.add_argument('--command', metavar='command', type=str, required=True, help='The Linux command to run')

    args = parser.parse_args()
    print(args.command)
    run_command(args.command)
    
