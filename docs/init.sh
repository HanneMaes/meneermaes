#!/bin/sh

# Start docker
systemctl start docker
# sudo systemctl status docker # show status

# Build docker image: read the instructions in Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
# Read the Dockerfile in the current directory (.) and builds an image tagged as meneermaes-jekyll
sudo docker build -t meneermaes-jekyll .

# Open website in Firefox
# firefox http://127.0.0.1:4000/
   # LiveReload address: where the see the site
   # Server address: don't use this one, its a separate server that handles the live reloading functionality

# Run the Docker container: create and start a new container for a specific image
# Runs any default commands specified in the image’s CMD or ENTRYPOINT
sudo docker run -p 4000:4000 -v $(pwd):/app meneermaes-jekyll
   # -p 4000:4000 Maps port 4000 of the container to port 4000 on your host machine
   # -v Mounts your current directory to /app in the container, allowing you to make changes to your files and see them reflected immediately










# bundle exec jekyll serve --baseurl "" --watch --livereload
   # --baseurl "": added because when linking my meneermaes.be domain I had to change to baseurl to "" in _config.yml, and now it only works locally when I add --baseurl ""
   # --watch: watch for changes and automatically rebuild the site
   # --livereload: automatically refresh the browser
