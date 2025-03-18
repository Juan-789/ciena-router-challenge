import subprocess
import sys
import time
import select
import threading

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        while True:
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

    cli_thread = threading.Thread(target=process_cli_input, args=(file_path, history, t))
    cli_thread.daemon = True  # Ensure thread exits when main program ends
    cli_thread.start()

    while t < 60:
        #reads hardware satte
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1
        if t%10 == 0:
            #tempoary values for index 1 and 2
            temp_for_index_1 = state_values[0]
            temp_for_index_2 = state_values[1]

            #swaps values at index_1 and index_2
            mutate_database(file_path, 0, temp_for_index_2)
            mutate_database(file_path, 1, temp_for_index_1)

            #stores the swap commands in history
            history.append(f"{t} swap {temp_for_index_1} {temp_for_index_2}")

        # Write Your Code Here Start
        if signal_values:
            if (signal_values[0]<=3 and signal_values[0]>=0):
                mutate_hardware(file_path, signal_values[0], signal_values[1])
            pass

        #print the values
        # print(f"state_values = {state_values}, control_values = {control_values}, signal_values = {signal_values}")
        
        #checks input
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            process_cli_input(file_path, history, t)
        
        # Write Your Code Here End

        time.sleep(1)  # Wait for 1 second 

    print_cli_history(history)
if __name__ == '__main__':
    main()
