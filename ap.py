import wifi
import socketpool
import led
import secrets
import hid

MAXBUF = 8192


def parse(url):
    encoding_map = {
        '%20': ' ',
        '%21': '!',
        '%22': '"',
        '%23': '#',
        '%24': '$',
        '%25': '%',
        '%26': '&',
        '%27': "'",
        '%28': '(',
        '%29': ')',
        '%2A': '*',
        '%2B': '+',
        '%2C': ',',
        '%2D': '-',
        '%2E': '.',
        '%2F': '/',
        '%3A': ':',
        '%3B': ';',
        '%3C': '<',
        '%3D': '=',
        '%3E': '>',
        '%3F': '?',
        '%40': '@',
        '%5B': '[',
        '%5C': '\\',
        '%5D': ']',
        '%5E': '^',
        '%5F': '_',
        '%60': '`',
        '%7B': '{',
        '%7C': '|',
        '%7D': '}',
        '%7E': '~',
        '%C3%A4': 'ä',
        '%C3%84': 'Ä',
        '%C3%B6': 'ö',
        '%C3%96': 'Ö',
        '%C3%BC': 'ü',
        '%C3%9C': 'Ü'
    }

    # Replace percent-encoded characters with their decoded equivalents
    for encoded_char, decoded_char in encoding_map.items():
        url = url.replace(encoded_char, decoded_char)

    return url


def start_ap():
    global pool

    # You may also need to enable the wifi radio with wifi.radio.enabled(true)

    # configure access point
    wifi.radio.start_ap(ssid=secrets.ap_ssid, password=secrets.ap_password)

    # print access point settings
    print("SSID: {}, password: {}".format(secrets.ap_ssid, secrets.ap_password))

    # print IP address
    print("IP: ", wifi.radio.ipv4_address_ap)
            

    pool = socketpool.SocketPool(wifi.radio)
    
    led.blink(2, 0.1)

# Create a simple HTTP server function
def http_server():
    server_socket = pool.socket()
    server_socket.bind((str(wifi.radio.ipv4_address_ap), 80))
    server_socket.listen(1)

    print("Listening on {}:80".format(wifi.radio.ipv4_address_ap))
    
    buf = bytearray(MAXBUF)

    while True:
        #print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        #print("Accepted connection from:", client_address)
        
        size = client_socket.recv_into(buf, MAXBUF)
        
        if b"GET /submit?data=" in buf:
            

            resp = buf.decode().replace("GET /submit?data=", "")
            
            buf = bytearray(MAXBUF)

            payload = parse(resp[:resp.find("HTTP/1")]).split("%0A")

            for line in payload:
                hid.parseLine(line)

        with open("index.html", "r") as html:
            response = html.read()
        content_length = len(response)
                
        client_socket.sendall(f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n")
        client_socket.sendall(response.encode())
        
        client_socket.close()