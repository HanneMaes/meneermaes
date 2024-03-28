#!/bin/bash

cd docs/
start firefox http://127.0.0.1:4000/meneermaes/ # I first need to start the browser because the next command (serve) doenst stop
bundle exec jekyll serve