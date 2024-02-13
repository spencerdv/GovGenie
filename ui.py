## Provides interface and recieves address information from the user 

import zmq, time

# For testing any bugs with ZeroMQ
# print(f"Current libzmq version is {zmq.zmq_version()}")
# print(f"Current  pyzmq version is {zmq.__version__}")


print("Hello and welcome to GovGenie\n")

print("Please enter an address to obtain information regarding the elected officals for that area.\n")

user_input = input()


# Sends user input to the API
context = zmq.Context()
# Socket to send information to server
print("Connecting to messenger.py")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2121")

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
    print(f"\nHere are your elected officals:\n")
    print(f"{message}")

#print(message.decode())
