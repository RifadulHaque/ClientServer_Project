#Name: Rifadul Haque
#ID: 40107346
#purpose: It is the client side that conencts to the server,
# it also has the implementation of downloading, uploading,
# how the clients asks for the correspoding responses from the server.
#I am the sole auther of this file


import socket
import sys # returns the list of command
import os.path



def set_up():   # Initial setup like port and ip settings
    while True:
        try:
            host_ip = input("IP Address:")   #  ip  Address of the server you want to connect to
            port_no= int(input("Port No:"))      # port no of the server you want to connect to
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            break
        except:
            print("Please provide valid ip and port no")
            continue
        
    return [client_socket, host_ip, port_no]
   
# setting the initial requirements
FORMAT = "utf-8"
setup = set_up()
client_socket = setup[0]
host_ip = setup[1]
port_no = setup[2]

# Conenction is setup here
try:
    client_socket.connect((host_ip, port_no))  # trying to connect to the server 
    connection_established = True
    #if the host ip and port connects then a connection is established
    print("Session has been established")
except Exception as e:
    print(e)
    #if a connection is not established
    print("Couldn't Connect to Server Please try again \n Make sure you have provided the right information")
    connection_established = False

def download_file_to_server(name_of_file, connection):   # This function lets you download any kind of data
    # Trying to download data
    # stores the size of the file
    size_of_file = int(connection.recv(2048).decode(FORMAT))
    try:
        #opens the file
        file = open(name_of_file, "wb")
        downloaded = 0
        # as long as it is tre it downloads
        while downloaded <= int(size_of_file):
            # file is downloading
            file_data = connection.recv(8192)
            if not file_data:
                break
            #file is written into the directory
            file.write(file_data)
            downloaded += sys.getsizeof(file_data)
        print(f"{name_of_file} has been downloaded Successfully")
    finally:
        file.close()

def upload_file_to_server(name_of_file, connection):  # This function uploads the files to the server in chunks of file_data
    # stores the file size using the file name
    size_of_file = os.path.getsize(name_of_file)
    transfer_data = 0
    # communcation with the client for sending data
    connection.send("sending_data".encode(FORMAT))
    #size is sent
    connection.send(f"{size_of_file}".encode(FORMAT))
    try:
        # open file in read mode
        file = open(name_of_file, "rb")
        while transfer_data<=size_of_file:
            # file is read and the data is store in the file_data
            file_data = file.read(4096)
            if not file_data:
                break
             # else sends file to the client
            connection.sendall(file_data)
            # transfer data counter is incremented
            transfer_data += sys.getsizeof(file_data)
        print(connection.recv(2048).decode(FORMAT))
    finally:
        file.close()

def main():   # This is the main funtion which will run all the code

    while connection_established:   # if connection to the server is successful this loop will run else not
        user_command = input("myftp>").lower()   # This is the user_command input

        # checking  what command has been given by the user
        match user_command.split(" ")[0]:
            case "put":
                try:
                    #the str is converted into binary
                    client_socket.send(user_command.replace("put", "000").encode(FORMAT))
                    name_of_file = user_command.split(" ")[1]
                    #using the file name the file is uplaoded to the server
                    upload_file_to_server(name_of_file, client_socket)
                except:
                    print("invalid input")
            case "help":
                client_socket.send(user_command.replace("help", "011").encode(FORMAT))
                #users_message = client_socket.recv(1024).encode(FORMAT)
                print("Commands are: bye change get help put")
                #print(users_message)
            case "bye":
                client_socket.send(user_command.encode(FORMAT))
                print("Session is terminated")
                sys.exit()
            case "get":
                #the binary code is sent to server
                client_socket.send(user_command.replace("get", "001").encode(FORMAT))
                name_of_file = user_command.split(" ")[1]
                # file size to be transferred
                users_message = client_socket.recv(2048).decode(FORMAT)
                if users_message == "sending_data":
                    #download method is called
                    download_file_to_server(name_of_file, client_socket)
                else:
                    print(users_message)
            case "change":
                client_socket.send(user_command.replace("change", "010").encode(FORMAT))
                users_message = client_socket.recv(2048).decode(FORMAT)
                print(users_message)

            case _: 
                print("Unrecognized user_command")

if __name__ == "__main__":
    main()
