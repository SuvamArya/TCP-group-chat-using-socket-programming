import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5299))
server.listen()

print("Server is running and listening...")

clients = {}
groups = {}

def handle_client(client_socket, client_address):
    try:
        user_id = client_socket.recv(1024).decode('utf-8')
        
        group_id = client_socket.recv(1024).decode('utf-8')

        client_socket.send(f"Welcome to group {group_id}! You are user {user_id}.".encode('utf-8'))

        # Add the client to the clients dictionary with user ID as the key
        clients[user_id] = client_socket

        # Add the client to the specified group or create a new group
        if group_id not in groups:
            groups[group_id] = [user_id]
        else:
            groups[group_id].append(user_id)
        #server side message for new user joining
        print(f"User {user_id} has joined group {group_id}", group_id, user_id)

        # Broadcast a message to the group that the user has joined
        broadcast_message(f"User {user_id} has joined group {group_id}", group_id, user_id)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            if message=='/quit':
                break

            #server side record of all messages from all groups
            print(f"{user_id}: {message} :: room {group_id}")
            # Broadcast the message to everyone in the same group
            broadcast_message(f"User {user_id}: {message}", group_id, user_id)
    except Exception as e:
        print(f"Error: {str(e)}")
    


def broadcast_message(message, group_id, user_id):
    for user in groups.get(group_id, []):
        if user != user_id:
            client = clients[user]
            client.send(message.encode('utf-8'))


while True:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
