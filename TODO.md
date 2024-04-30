# TODOs

## Login
- Use Flask session for logging in (There wont be a user, just a password)
- Add Env-Var for Session Secret Key
- Add Env-Var for TsViewer password (one for admin, one for everything else)

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

