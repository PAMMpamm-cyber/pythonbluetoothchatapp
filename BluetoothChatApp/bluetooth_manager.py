import bluetooth

class BluetoothManager:
    def __init__(self, uuid):
        self.uuid = uuid
        self.server_socket = None
        self.client_socket = None

    def start_server(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)
        bluetooth.advertise_service(self.server_socket, "BluetoothChatApp",
                                    service_id=self.uuid,
                                    service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Bluetooth server started and waiting for connections...")

    def accept_connection(self):
        self.client_socket, client_info = self.server_socket.accept()
        print(f"Accepted connection from {client_info}")

    def connect_to_server(self, address):
        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((address, 1))
        print(f"Connected to server at {address}")

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.send(message)

    def receive_message(self):
        if self.client_socket:
            return self.client_socket.recv(1024).decode("utf-8")
        return None

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()

    def discover_devices(self):
        return bluetooth.discover_devices(lookup_names=True)