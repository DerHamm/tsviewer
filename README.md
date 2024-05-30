# Teamspeak Web Dashboard

This project aims to provide a web interface for interacting with a Teamspeak 3 server using the Teamspeak Server Query
protocol. The web application is built using Python with Flask as the web server framework.

## Features

- **Client Information**: View details about clients connected to the Teamspeak server.
- **File Information**: Configure a designated upload channel, that aggregates all files from other channels
 and manage them.
- **Query Commands**: Issue Teamspeak Server Query commands
- **Customizable Configuration**: Easily configure server credentials and other settings using a JSON file.
- **Planned Features**: An easy-to-setup `Docker` image, More supported query commands and Server management Features

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
  "website_password": "s3cret",
  "admin_password": "t3amsp3ak",
  "cookie_secret_key": "c00kie_s3cr3t",
  "cookie_signing_salt": "c00kie_s4lt",
  "disable_user_password_protection": true,
  "disable_admin_password_protection": true,
  "upload_channel_id": "1",
  "clean_up_upload_channel": true,
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


## Security

There are configuration options to secure the TsViewer with a password. There are two roles: `Admin` and `User`.
Admins can issue commands and see detailed client information, while Users can't.

You have to set the configuration flags `disable_user_password_protection` and or `disable_admin_password_protection` to
`true` to activate either one or both of the roles.

If `disable_user_password_protection` is set to `true`, then `website_password` has to be set.
The same goes for `disable_admin_password_protection` and `admin_password`.

The TsViewer uses a signed session cookie to store the role of a client. Make sure to also set the flags
`cookie_secret_key` and `cookie_signing_salt`, so the cookies can't be forged or messed with otherwise.