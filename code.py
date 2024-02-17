import led

print("Booted up")

led.blink(3, 0.1)

import ap
ap.start_ap()
ap.http_server()