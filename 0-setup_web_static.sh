#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static.

# Install Nginx if it's not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
web_static_dir="/data/web_static"
test_dir="$web_static_dir/releases/test"
shared_dir="$web_static_dir/shared"
current_dir="$web_static_dir/current"

sudo mkdir -p "$web_static_dir" "$test_dir" "$shared_dir"
sudo touch "$test_dir/index.html"

# Create symbolic link (remove and recreate if it already exists)
if [ -L "$current_dir" ]; then
    sudo rm -f "$current_dir"
fi
sudo ln -s "$test_dir" "$current_dir"

# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu "$web_static_dir"

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_alias="location /hbnb_static/ {\n    alias $current_dir/;\n}"
if grep -q "location /hbnb_static/" "$config_file"; then
    sudo sed -i "s|location /hbnb_static/.*|$config_alias|" "$config_file"
else
    sudo sed -i "s|^\s*server {|&\n\n$config_alias|" "$config_file"
fi

# Restart Nginx
sudo service nginx restart

exit 0
