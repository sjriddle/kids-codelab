"""
Start the Browser Playground! 🎨

Run this with:
    python3 06_browser_playground/start_playground.py

It starts a little web server on your own computer (that's what "localhost"
means) and opens the playground in your web browser. Your child can draw by
clicking and dragging, pick colors, and stamp emojis.

When you're done playing, come back to the Terminal and press Ctrl + C to stop.
"""

import functools
import http.server
import os
import socketserver
import webbrowser

# Serve the files from the "web" folder that sits next to this script.
WEB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def find_free_port(start=8000, tries=20):
    """Find a port number that isn't already being used."""
    for port in range(start, start + tries):
        try:
            with socketserver.TCPServer(("", port), http.server.BaseHTTPRequestHandler):
                return port
        except OSError:
            continue  # that port was busy, try the next one
    return start


def main():
    port = find_free_port()
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=WEB_FOLDER
    )

    with socketserver.ThreadingTCPServer(("", port), handler) as server:
        url = "http://localhost:" + str(port)
        print("=" * 50)
        print("  🎨  The Playground is OPEN!")
        print("  Opening your browser at: " + url)
        print("  When you're done, press  Ctrl + C  to stop.")
        print("=" * 50)
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Playground closed. Great drawing!")


if __name__ == "__main__":
    main()
