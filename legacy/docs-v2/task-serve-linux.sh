#!/bin/bash

cd docs/
firefox http://127.0.0.1:4000/
   # LiveReload address: where the see the site
   # Server address: don't use this one, its a separate server that handles the live reloading functionality

bundle exec jekyll serve --baseurl "" --watch --livereload
   # --baseurl "": added because when linking my meneermaes.be domain I had to change to baseurl to "" in _config.yml, and now it only works locally when I add --baseurl ""
   # --watch: watch for changes and automatically rebuild the site
   # --livereload: automatically refresh the browser
