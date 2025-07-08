#!/bin/bash

git status
git add *
now=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Push fast: $now"
git push
git status