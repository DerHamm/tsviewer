# Teamspeak Web Dashboard

This project aims to provide a web interface for interacting with a Teamspeak 3 server using the Teamspeak Server Query
protocol. The web application is built using Python with Flask as the web server framework.

## Features

- **Display Information**: View details about clients connected to the Teamspeak server.
- **Customizable Configuration**: Easily configure server credentials and other settings using a JSON file.
- **Planned Features**: Implementing user interfaces to also issue Server Query commands, a File-Upload manager and an
easy-to-setup `Docker` image.

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

```json
{
  "server_query_host": "127.0.0.1",
  "server_query_port": 10011,
  "server_voice_port": 9987,
  "server_query_user": "serveradmin",
  "server_query_password": "v3rys3cret!",
  "server_id": 1,
  "teamspeak_install_path": "/home/teamspeak3",
  "website_password": "s3cret",
  "admin_password": "t3amsp3ak",
  "cookie_secret_key": "c00kie_s3cr3t",
  "cookie_signing_salt": "c00kie_s4lt",
  "disable_user_password_protection": true,
  "disable_admin_password_protection": true,
  "upload_channel_id": "1",
  "debug": true,
  "log_path": "log/tsviewer.log"
}
```

Replace the placeholders with your Teamspeak server details and query credentials.
By default, the name for the Server Query user is `serveradmin` and the port is `10011`.
The default configuration path points to `config/example_config.json`, which is just filled with example values.
You can replace that path by setting the environment variable `TSVIEWER_CONFIGURATION_FILE=/path/to/your/config`.

### Alternative: Environment variables

You can also set environment variables for the configuration fields. If a configuration file is specified the
environment variables for that configuration field will be overridden.
The environment variables do have the same name as their corresponding fields in uppercase with an added
prefix `TSVIEWER_CONFIGURATION_`. E.g.:

```json
{
  "server_query_host": "127.0.0.1"
}
```

expressed as an environment variable would become:

```shell
export TSVIEWER_CONFIGURATION_SERVER_QUERY_HOST=127.0.0.1
```

## Usage

1. Run the Flask application:

    ```bash
    python -m flask run
    ```

2. Access the web interface in your browser by navigating to `http://localhost:5000`.

