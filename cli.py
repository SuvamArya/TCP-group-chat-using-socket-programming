import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5299))

user_id = input("Enter your user ID: ")
group_id = input("Enter the group ID you want to join: ")

client.send(user_id.encode('utf-8'))
client.send(group_id.encode('utf-8'))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except Exception as e:
            print(f"Error: {str(e)}")
            break

def send_messages():
    while True:
        message = input()
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()
