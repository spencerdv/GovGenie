## Provides interface and recieves address information from the user 

import zmq, time

# For testing any bugs with ZeroMQ
# print(f"Current libzmq version is {zmq.zmq_version()}")
# print(f"Current  pyzmq version is {zmq.__version__}")


print("Hello and welcome to GovGenie\n")

print("Please enter an address to obtain information regarding the elected officals for that area. You may quit by entering 'quit'.\n")


while True:
    
    user_input = input()
    address = user_input

    if user_input == 'quit':
        break

    # Sends user input to the API
    context = zmq.Context()
    # Socket to send information to server
    print("Connecting to messenger.py")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:21213")

    # Do 10 requests, waiting each time for a response
    for request in range(1,2):
        print(f"Sending request . . .")
        socket.send_string(user_input)
        print('.')
        time.sleep(.5)
        print('..')
        time.sleep(.5)
        print('...')
        time.sleep(.5)
        print('..')
        time.sleep(.5)
        print('.')
        time.sleep(.5)
        # Get reply (recived as bytes object)
        message = socket.recv()
        print(f"\nHere are the federally elected officals for {address}:\n")
        new_message = message.decode('utf-8')
        print(f"{new_message}\n")
        officals_list = new_message.split('\n\n')


        if new_message != "An error occured, please try a different address":
            # Party filter functionality
            print("Please enter 'yes' if you would you like to filter your results by party")
            party_input = input()
            if party_input == 'yes' or party_input == 'y':
                print("\nPlease enter 'R' to obtain the Republicans who represent this address. \nEnter 'D' to obtain the Democrats who represent this address.")
                party_input = input()
                if party_input == 'R' or party_input == 'r':
                    print("\nHere are the Republicans who federally represent this address:\n")
                    for offical in officals_list:
                        if 'Republican' in offical:
                            print(offical)
                if party_input == 'D' or party_input == 'd':
                    print("\nHere are the Democrats who federally represent this address:\n")
                    for offical in officals_list:
                        if 'Democrat' in offical:
                            print(offical + '\n')
            
                print("Enter 'yes' if you would like to see your unfiltered results again.")
                if input() == 'yes':
                    print('\n' + new_message)

        print("\nYou may enter another address if you would like to search again.  You may quit by entering 'quit'.")

print('\n\nThank you for using GovGeni.\n')
