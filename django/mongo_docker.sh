#!/usr/bin/env bash
sudo docker run -d -p 27017:27017 -v ~/Docker/mongodb/:/data/db --name mymongo mongo:latest
