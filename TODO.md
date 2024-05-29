# TODOs

## Routing
- Find a way to do partial updates on the index page (So users can be updated)
- The routing concept right now abstracts weird teamspeak parameters with route names
  (e.g. There is a parameter for CLIENTKICK, that kicks the client from the channel if a param is `4`,
  but it kicks the client from the server when it's `5`. In the current routing, this is abstracted as two routes
  `kick_client_from_server` and `kick_client_from_channel`). Should we keep it that way? Overthink that

## Admin Page (Requires: Login)
- Build UI for all the troll commands
- Display client detail information

## Colors, Icons, etc
- Decide on a color palette for the website
- Decide on an icon pack an stick to it

## Docker Deployment
- Add the functionality to deploy `tsviewer` in a docker container
- Add the Flask Webserver Port to the configuration
- This also means we have to use a production WSGI server within the container (unicorn?)

## Unit and integration tests
- Add unit tests where applicable
- After `Docker Deployment` is done, we can start to implement some integration tests as well

## Talk to designer
- ~ Jun. 15 2024

## Misc.
- Create avatars and the log folder automatically
- Muted Sound icon is not showing. Why?
- Document Security Feautures in README.md
