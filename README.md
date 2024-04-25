# Teamspeak Web Dashboard

This project aims to provide a web interface for interacting with a Teamspeak 3 server using the Teamspeak Server Query protocol. The web application is built using Python with Flask as the web server framework.

## Features

- **Display Information**: View details about clients connected to the Teamspeak server.
- **Customizable Configuration**: Easily configure server credentials and other settings using a JSON file.
- **Planned Features**: Future enhancements include adding authorization for the website and implementing user interfaces to also issue Server Query commands.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DerHamm/tsviewer.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `config.json` file in the project root with the following structure:

    ```json
    {
      "HOST": "127.0.0.1",
      "PORT": 10011,
      "USER": "serveradmin",
      "PASS": "v3rys3cret!",
      "SERVER_ID": 1,
      "TEAMSPEAK_INSTALL_PATH": "/home/teamspeak3"
    }
    ```

    Replace the placeholders with your Teamspeak server details and query credentials. By default, the name for the Server Query user is `serveradmin` and the port is `10011`.

## Usage

1. Run the Flask application:

    ```bash
    python -m flask run
    ```

2. Access the web interface in your browser by navigating to `http://localhost:5000`.

