# TODOs

## File Uploads
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

## Frontpage
- Add the user's mic-/headphone status on their card

## Virtual Server
- The virtual server id is hardcoded in some paths. Parametrize it with the configured server id.