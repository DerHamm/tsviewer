# Teamspeak Web Dashboard

This project aims to provide a web interface for interacting with a Teamspeak 3 server using the Teamspeak Server Query
protocol. The web application is built using Python with Flask as the web server framework.

## Features

- **Display Information**: View details about clients connected to the Teamspeak server.
- **Customizable Configuration**: Easily configure server credentials and other settings using a JSON file.
- **Planned Features**: Future enhancements include adding authorization for the website and implementing user
  interfaces to also issue Server Query commands.

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

Create a `config.json` file in the project sub-folder `config` with the following structure:

https://github.com/DerHamm/tsviewer/blob/9ff63c3b73617342e2bea57d77cc3e5f44ea2cc2/config/example_config.json

Replace the placeholders with your Teamspeak server details and query credentials. By default, the name for the Server Query user is `serveradmin` and the port is `10011`.
The default configuration path is `config/config.json`. You can replace that path by setting the environment variable `TSVIEWER_CONFIGURATION_FILE=/path/to/your/config`.

### Alternative: Environment variables

You can also set environment variables for the configuration fields. If a configuration file is specified the
environment variables for that configuration field will be overridden.
The environment variables do have the same name as their corresponding fields in uppercase with an added
prefix `TSVIEWER_CONFIGURATION_`. E.g.:

```json
{
  "host": "127.0.0.1"
}
```

expressed as an environment variable would become:

```shell
export TSVIEWER_CONFIGURATION_HOST=127.0.0.1
```

## Usage

1. Run the Flask application:

    ```bash
    python -m flask run
    ```

2. Access the web interface in your browser by navigating to `http://localhost:5000`.

