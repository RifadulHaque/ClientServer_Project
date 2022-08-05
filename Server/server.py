#Name: Rifadul Haque
#ID: 40107346
#purpose: It is the server side that bind ths conenction of the IP address and the port,
# it also has the implementation of downloading, uploading,changing name of the file and also
# the corresponding way the client and server communcates.

#I am the sole auther of this file

# I have placed some links that has helped me understand the socket programming better

import socket
import sys # returns the list of command
import os #interating with the operaing syestem
import os.path
from threading import Thread

def set_up():  # initial set_up funtion
    while True:  
        port = input("Port number of Server: ")  # port no
        try:
            port = int(port) # checks if port no is valid
            host = input("Host ip address:") # ip address of server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            break
        except:
            print("Please provide valid ip and port no")
            continue
    return server, host, port


setup= set_up() # creating an initial setup
server = setup[0] # server given by the setup fuction
host = setup[1] # host given by the setup funtion
port = setup[2] # port given by the setup functioin

# binding  server to the port and address
server.bind((host, port))

FORMAT = "utf-8" # the format in which messages will be encoded

#method used to change the file name
def change_name_of_file(name_of_file, new_name_of_file, connection): # file change command
    try:
        #checks the directory to rename the name
        os.rename(name_of_file, new_name_of_file)
        #informs that the file name has been changed
        connection.send(f"{name_of_file} has been changed to {new_name_of_file}".encode(FORMAT))
    except Exception as e:
        connection.send("Name change was unsuccessful".encode(FORMAT))
        print(e)

def upload_file_to_client(name_of_file, connection):   # Uploads files to clients folder

    try:
        #stores the file size using the file name
        file_size = os.path.getsize(name_of_file)
        transfer = 0
        #communcation with the client for sending data
        connection.send("sending_data".encode(FORMAT))
        #data that is sent
        connection.send(f"{file_size}".encode(FORMAT))
        try:
            #open file in read mode
            file = open(name_of_file, "rb")
            #checks if the transfered data is less than the file size or not
            while transfer<=file_size: #continue on being True
                #file is read and the data is store in the file_data
                file_data = file.read(8192)
                #gives the exception
                if not file_data:
                    break
                #else sends file to the client
                connection.sendall(file_data)
                #transfer data is incremented
                transfer += sys.getsizeof(file_data)
        finally:
            file.close()

    except Exception as e:
        connection.send("File is not in the directory".encode(FORMAT))
        print(e)

#used for putting file inside server directory
def download_file_from_client(name_of_file, connection): # Downloads files from clients folder
    #stores the size of the file
    size = int(connection.recv(2048).decode(FORMAT))
    try:
        #opens the file
        file = open(name_of_file, "wb")
        #the data that is downloaded is set to 0
        downloaded = 0
        #as long as it is true it downloads
        while downloaded <= int(size):
            #file is downloading
            file_data = connection.recv(8192)
            if not file_data:
                break
            #file is copied into the server directory
            file.write(file_data)
            #data transferred and hence download is incremented
            downloaded += sys.getsizeof(file_data)
    finally:
        file.close()

    connection.send(f"{name_of_file} has been uploaded successfully.".encode(FORMAT))



def Connection(connection, ip_address): # handles clients
    try:
        #as long as the connection is true message is received
        connection_established = True
        while connection_established:      # Main loop
            clients_messages = connection.recv(2048).decode(FORMAT).lower()
            # Checking what kind of message is given
            match clients_messages.split(" ")[0]:
                #responds to the put message
                case "000":
                    #file that the client has sent
                    file = clients_messages.split(" ")[1]
                    #file size to be transferred
                    clients_messages = connection.recv(2048).decode(FORMAT)
                    if clients_messages == "sending_data":
                        #calling the download method to download the file
                        download_file_from_client(file, connection)
                #get
                case "001":
                    #file that will be sent
                    file = clients_messages.split(" ")[1]
                    #Calling the upload file to sent the file
                    upload_file_to_client(file, connection)
                #change name
                case "010":
                    #recives 2 names
                    name_of_file, new_name_of_file = clients_messages.split(" ")[1], clients_messages.split(" ")[2]
                    #calling the method to chnage the name
                    change_name_of_file(name_of_file, new_name_of_file, connection)
                #help
                case "011":
                    #clients_messages = connection.recv(2048).decode(FORMAT)
                    connection.send("Commands are: bye change get help put").encode(FORMAT)
                case "bye":
                    connection.close()
                case _:
                    pass
    except Exception as e:
        print(e)
        print(f"connection {ip_address} and {port} is closed")
            
def main():  # all the clients handling
    print("server is listening to receive signals from clients")
    server.listen()

    # Note for referenc: https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python
    # https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
    while True:  
        try:
            #conenction is accepted
            connection, ip_address = server.accept()
            #thread is used to create the connection between client and server
            Thread(target=Connection, args=(connection, ip_address)).start()
        except:
            print("Connection error")

if __name__ == "__main__":
    main() # the main function is called




