#!/bin/bash

# Remove any existing content in the 'public' directory
rm -rf public

# Run the main Python script which includes generating the page
python3 src/main.py

# Navigate to 'public' and start the web server on port 8888
cd public && python3 -m http.server 8888
