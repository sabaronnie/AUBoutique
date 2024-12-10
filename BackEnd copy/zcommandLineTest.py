 def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), port))
    server.listen()
    print(f"[SERVER]: Listening on {port}")
    while True:
       connection,address= server.accept()
       server_thread = threading.Thread(target=handle_client, args=(connection, address))
       server_thread.start()



if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python filename.py <port>")
    sys.exit(1)

  try:
    port = int(sys.argv[1])
  except ValueError:
    print("Please provide a valid port number.")
    sys.exit(1)
  start_server(port)



  
  
