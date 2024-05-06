# TODOs

## File Uploads
- The commands FTRENAMEFILE and FTDELETEFILE could be sufficient for the implementation
- Use a similar approach to `avatars.py` to make accessing files uploaded on your Teamspeak easier
- Add a `cleanup`-utility, that moves all files found in different channels to the designated upload-channel
- (NTH) Link all files from the designated upload-channel in the channel description
- Display the contents of the upload-channel on a sub-site

## Docker Deployment
- Add the functionality to deploy `tsviewer` in a docker container
- Add the Flask Webserver Port to the configuration

## Admin Page (Requires: Login)
- Build UI for all the troll commands
- Display client detail information

## Talk to designer
- ~ Jun. 15 2024

## Testing

### Configuration
- The current implementation for the configuration is not feasible anymore, add some kind of singleton so that
the `Configuration` class can be instantiated anywhere with the same configuration file / env vars
- Remove all occurrences of the default path used for the configuration file (`config/config.json`)
- The goal is to turn the `Configuration` class into a weak dependency for all the features that it is needed for, the
server should still be able to start without a configuration (Means that features like
custom cookie signing, avatars and file uploads should be disabled then)
