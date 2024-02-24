import ErrorCatcher as ec
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Linux command')
    parser.add_argument('--command', metavar='command', type=str, required=True, help='The Linux command to run')

    args = parser.parse_args()
    print(args.command)
    ec.run_file_with_error_catching(args.command)
    

