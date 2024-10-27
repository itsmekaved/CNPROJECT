import socket
import threading

# Server address and port
HOST = '127.0.0.1'  # Localhost for testing
PORT = 8080

# Function to handle each client connection
def handle_request(conn):
    try:
        request = conn.recv(1024).decode('utf-8')
        headers = request.split('\n')
        request_type = headers[0].split()[0]
        requested_file = headers[0].split()[1]

        if request_type == 'POST':
            # Extract POST data
            post_data = headers[-1]
            data_dict = dict(item.split('=') for item in post_data.split('&'))
            name = data_dict.get('name', '').replace('+', ' ')
            message = data_dict.get('message', '').replace('+', ' ')

            # Serve the response.html with injected data
            with open('./response.html', 'r') as file:
                content = file.read()
                # Replace placeholders with actual data
                content = content.replace('{{ name }}', name)
                content = content.replace('{{ message }}', message)

            response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{content}'

        elif request_type == 'GET':
            if requested_file == '/':
                requested_file = '/index.html'
            try:
                with open(f'.{requested_file}', 'r') as file:
                    content = file.read()
                response = f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{content}'
            except FileNotFoundError:
                response = 'HTTP/1.1 404 Not Found\n\n404 Page Not Found'

        else:
            response = 'HTTP/1.1 405 Method Not Allowed\n\nOnly GET and POST methods are allowed'

        # Send response and close connection
        conn.sendall(response.encode())

    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        conn.close()

# Main server function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Listen for up to 5 connections
    print(f"Server running on {HOST}:{PORT}...")

    while True:
        # Accept incoming client connection
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_request, args=(conn,))
        client_thread.start()

# Run the server
if __name__ == "__main__":
    start_server()

