#!/bin/sh

# 1. Start Docker daemon if not running
# systemctl manages system services. This ensures Docker daemon is running before we try to use Docker commands
systemctl start docker

# 2. Build docker image
# sudo: run the command with root privileges
# docker build: creates a new Docker image from a Dockerfile
# -t meneermaes-jekyll: tags (names) the image as "meneermaes-jekyll"
# . : looks for Dockerfile in the current directory
sudo docker build -t meneermaes-jekyll .

# 3. Run the Docker container with LiveReload enabled in the background
# sudo docker run: creates and starts a new container from our image
# -p 4000:4000: maps container's port 4000 to host's port 4000 (Jekyll server)
# -p 35729:35729: maps container's port 35729 to host's port 35729 (LiveReload server)
# -v $(pwd):/app: mounts current directory (pwd) to /app in container
#                 this allows real-time file editing from host machine
# meneermaes-jekyll: the image to use for this container
# bundle exec jekyll serve: runs Jekyll through Bundler to ensure correct gem versions
# --livereload: enables automatic browser refresh when files change
# &: runs the container in the background (async) so script can continue
sudo docker run \
   -p 4000:4000 \
   -p 35729:35729 \
   -v $(pwd):/app \
   meneermaes-jekyll \
   bundle exec jekyll serve --livereload &

# 4. Wait for Jekyll server to be ready
# This loop continuously checks if the server is responding
echo "Waiting for Jekyll server to start..."
while ! curl -s http://localhost:4000 > /dev/null; do
   # curl: tool for making HTTP requests
   # -s: silent mode (don't show progress)
   # > /dev/null: discard the output
   # while !: keep looping until the command succeeds (returns 0)
   sleep 1  # wait 1 second before trying again to avoid hammering the server
done
echo "Jekyll server is ready!"  # notify user when server is up

# 5. Launch Firefox
# Opens Firefox to the local Jekyll server address
# This is only executed after the server is confirmed running
firefox http://127.0.0.1:4000/

# Note: The script will finish executing but the Docker container continues running
# in the background. To stop the server:
# 1. Find the container ID: sudo docker ps
# 2. Stop it: sudo docker stop <container-id>













# # 1. Start Docker daemon if not running
# systemctl start docker
#
# # 2. Build docker image
# sudo docker build -t meneermaes-jekyll .
#
# # 3. Run the Docker container with LiveReload enabled in the background
# sudo docker run \
#     -p 4000:4000 \
#     -p 35729:35729 \
#     -v $(pwd):/app \
#     meneermaes-jekyll \
#     bundle exec jekyll serve --livereload &
#
# # 4. Wait for Jekyll server to be ready
# echo "Waiting for Jekyll server to start..."
# while ! curl -s http://localhost:4000 > /dev/null; do
#     sleep 1
# done
# echo "Jekyll server is ready!"
#
# # 5. Launch Firefox
# firefox http://127.0.0.1:4000/







# Start docker
# systemctl start docker
# sudo systemctl status docker # show status

# Build docker image: read the instructions in Dockerfile and package the application's environment, dependencies, and configurations into a reusable Docker image
# This image serves as a blueprint for containers, it is stored in the Docker daemon and can be used multiple times to start containers
# Read the Dockerfile in the current directory (.) and builds an image tagged as meneermaes-jekyll
# sudo docker build -t meneermaes-jekyll .

# Open website in Firefox
# firefox http://127.0.0.1:4000/
   # LiveReload address: where the see the site
   # Server address: don't use this one, its a separate server that handles the live reloading functionality

# Run the Docker container: create and start a new container for a specific image
# Runs any default commands specified in the image’s CMD or ENTRYPOINT
# sudo docker run -p 4000:4000 -v $(pwd):/app meneermaes-jekyll
   # -p 4000:4000 Maps port 4000 of the container to port 4000 on your host machine
   # -v Mounts your current directory to /app in the container, allowing you to make changes to your files and see them reflected immediately










# bundle exec jekyll serve --baseurl "" --watch --livereload
   # --baseurl "": added because when linking my meneermaes.be domain I had to change to baseurl to "" in _config.yml, and now it only works locally when I add --baseurl ""
   # --watch: watch for changes and automatically rebuild the site
   # --livereload: automatically refresh the browser
