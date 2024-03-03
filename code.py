import led

print("Booted up")

led.blink(1, 1)

import ap
ap.start_ap()
ap.http_server()