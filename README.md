# Ransomware ASCII Splash Screen Simulation

This Python script simulates a ransomware splash screen. It creates a server that listens for a specific secret message, and upon receiving the message, it displays a simulated ransomware splash screen.

## Requirements

- Python 3.x

## Usage

1. Set the desired environment variables for configuration (optional).
2. Run the Python script.

## Configuration

You can configure the script using the following environment variables:

- `LOG_LEVEL`: Logging level. Default is "DEBUG".
- `LISTEN_HOST`: Server host to listen on. Default is "127.0.0.1".
- `LISTEN_PORT`: Server port to listen on. Default is "1337".
- `LISTEN_SECRET`: Secret message to trigger the splash screen. Default is "UNCONTAINED".

## Splash Screen Configuration

The splash screen configuration options are as follows:

- `SPLASH_ESCAPE`: Keybinding to close the splash screen. Default is "<Escape>."
- `SPLASH_BG_COLOUR`: Background color of the splash screen. Default is "red".
- `SPLASH_FG_COLOUR`: Foreground color of the splash screen. Default is "white".
- `SPLASH_FONT`: Font used in the splash screen. Default is "Courier".
- `SPLASH_MESSAGE`: The message displayed on the splash screen.

## Code Structure

- `Worker`: A thread that creates a new `Splasher` instance.
- `Splasher`: A class that handles the splash screen creation and display.
- `Server`: A class that handles incoming connections and adds the received messages to a queue.

## Known Limitations

This script is provided for educational purposes only.
