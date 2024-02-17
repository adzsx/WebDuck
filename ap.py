import wifi
import socketpool
import led
import secrets


def start_ap():
    global pool

    # You may also need to enable the wifi radio with wifi.radio.enabled(true)

    # configure access point
    wifi.radio.start_ap(ssid=ap_ssid, password=secrets.ap_password)

    # print access point settings
    print("SSID: {}, password: {}".format(secrets.ap_ssid, secrets.ap_password))

    # print IP address
    print("IP: ", wifi.radio.ipv4_address_ap)
    

    led.blink(2, 0.1)
            

    pool = socketpool.SocketPool(wifi.radio)

# Create a simple HTTP server function
def http_server():
    server_socket = pool.socket()
    server_socket.bind((str(wifi.radio.ipv4_address_ap), 80))
    server_socket.listen(1)

    print("Listening on {}:80".format(wifi.radio.ipv4_address_ap))

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from:", client_address)
        led.blink(1, 0.2)
        
        response = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rubby</title>
    </head>
    <body>
        <h>World Hello</h>
    </body>
</html>
"""
        
        client_socket.send(response.encode())
        client_socket.close()
        

        # HTTP response with status line and headers




