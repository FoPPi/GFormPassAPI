#!/bin/bash

# Function to prompt for confirmation
# Dont work
#confirm() {
#    read -p "$1 (y/n) " -n 1 -r
#    echo
#    if [[ ! $REPLY =~ ^[Yy]$ ]]
#    then
#        exit 1
#    fi
#}

# Confirm before proceeding
echo "This script will uninstall Docker, Docker Compose. Are you sure you want to continue?"

# Stop and remove all Docker containers
echo "Stopping and removing all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Remove all Docker images
echo "Removing all Docker images..."
docker rmi $(docker images -q) 2>/dev/null

# Remove all Docker volumes
echo "Removing all Docker volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null

# Uninstall Docker
echo "Uninstalling Docker..."
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo apt-get autoremove -y
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

# Remove Docker Compose
echo "Removing Docker Compose..."
sudo rm /usr/local/bin/docker-compose

# Remove user from docker group
echo "Removing current user from docker group..."
sudo gpasswd -d $USER docker

echo "Uninstallation complete. You may need to restart your system for all changes to take effect."
