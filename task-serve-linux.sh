#!/bin/bash

cd docs/
firefox http://127.0.0.1:4000/ # I first need to start the browser because the next command (serve) doenst stop
bundle exec jekyll serve --baseurl "" # --baseurl "" was added because when linking my meneermaes.be domain I had to change to baseurl to "" in _config.yml, and now it only works locally when I add --baseurl ""