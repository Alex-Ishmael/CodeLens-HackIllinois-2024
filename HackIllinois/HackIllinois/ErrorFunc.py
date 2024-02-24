import sys
import traceback

def run_file_with_error_catching(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
            exec(code)
    except Exception:
        print(f"An error occurred while executing '{filename}':")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_with_error_catching.py <filename>")
    else:
        filename = sys.argv[1]
        run_file_with_error_catching(filename)