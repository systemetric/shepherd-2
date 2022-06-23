# Shepherd requirements

## API
- Run
    - Default to zone zero but should be able to be set
- Stop
- Create, Read, Update, Delete usercode files
    - Lint usercode upon upload and return an error is
    - Let the user turn off the linting
    - MyPy once the robot module is fully typed
- Select user code to run
- Serve sheep
- PyLS socket
- Serve log/image files HTTP
- Sockets for logs/images/Robot State MQTT?
- Serve time left on internal robot clock

## Webserver
- Docs
- Editor
- Landing page
    - Should the landing page be the editor?
- Licenses
- Favicon

## RobotAPI interface
- Stop needs to turn off 12V on the robot
- Would be nice to at least expose read-only access to robot

## Management of UserCode
- Stop due to timeout
- Start due to start button being pressed
- Should be able to upload the following types:
    - text/py: interpreted as plain python file
    - zip:
        - Extract/Find the main.py
- Rescale image output of

## USB Config
- Detect Arena USB
- Get zone from arena USB
- Check `teamname.txt`
- Set round start image in preference order:
    - The robot stores the last image which it took, this just overwrites that image.
    - Image preference order:
        1. We have a team corner image on the USB
        2. The team have uploaded their own image to the robot
        3. We have a generic corner image on the USB
        4. The game image
