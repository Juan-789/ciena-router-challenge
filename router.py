import subprocess
import sys
import time
import select

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        user_input = input("Enter CLI command: ")
        command, *args = user_input.split()
        if command == "set":
            index = int(args[0]) - 1
            value = int(args[1])
            if index < 0 or index >3 :
                print(f"Invalid Input - Error: {index}")
            else:
                mutate_database(file_path, index, value)
                history.append(f"{t} set {index} {value}")
    except Exception as e:
        print(f"Invalid Input - Error: {str(e)}")

def main():
    history = []
    t = 0

    #opens file or creates file if it doesn't exist
    try:
        with open(file_path, 'r'):
                pass
    except FileNotFoundError:
        create_hardware_file(file_path)

    while t < 60:
        #reads hardware satte
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1

        # Write Your Code Here Start

        #print the values
        print(f"state_values = {state_values}, control_values = {control_values}, signal_values = {signal_values}")
        
        #checks input
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            process_cli_input(file_path, history, t)
        

       

        # Write Your Code Here End

        time.sleep(1)  # Wait for 1 second 

    print_cli_history(history)
if __name__ == '__main__':
    main()