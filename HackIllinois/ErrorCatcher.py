import sys
import traceback


def run_file_with_error_catching(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
            exec(code)
    except Exception :
        # f = open("Output.txt", "x")
        f = open("Output.txt", "w")
        f.write(f"An error occurred while executing '{filename}':") 
        traceback.print_exc(file=f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_with_error_catching.py <filename>")
    else:
        filename = sys.argv[1]
        run_file_with_error_catching(filename)
