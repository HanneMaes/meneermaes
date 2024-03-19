#!/bin/bash

git add *
git commit -m 'Push fast: $(date +"%Y-%m-%d %H:%M:%S")'
git push
git status