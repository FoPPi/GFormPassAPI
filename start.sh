#!/bin/bash

# Function to install Docker
install_docker() {
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    rm get-docker.sh
    echo "Docker installed successfully!"
}

# Function to install Docker Compose
install_docker_compose() {
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully!"
}

# Function to install apache2-utils and create password file
create_password_file() {
    echo "Installing apache2-utils..."
    sudo apt-get update
    sudo apt-get install -y apache2-utils

    echo "Creating nginx directory if it doesn't exist..."
    mkdir -p ./nginx

    # Generate random suffix for username (5 alphanumeric characters)
    random_suffix=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 7 | head -n 1)
    username="root_${random_suffix}"

    # Generate random password (15 characters)
    password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*()_+' | fold -w 15 | head -n 1)

    echo "Creating .htpasswd file with generated credentials..."
    htpasswd -bc ./nginx/.htpasswd "$username" "$password"

    # Print credentials in green color
    echo -e "\033[32mGenerated credentials:\033[0m"
    echo -e "\033[32mUsername: $username\033[0m"
    echo -e "\033[32mPassword: $password\033[0m"

    # Save credentials to a secure file
    echo "Username: $username" > ./nginx/secure_credentials.txt
    echo "Password: $password" >> ./nginx/secure_credentials.txt
    chmod 600 ./nginx/secure_credentials.txt

    echo "Credentials saved to ./nginx/secure_credentials.txt"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    install_docker
else
    echo "Docker is already installed."
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    install_docker_compose
else
    echo "Docker Compose is already installed."
    
fi

# Ensure the current user can run Docker commands without sudo
if ! groups $USER | grep &>/dev/null '\bdocker\b'; then
    echo "Adding user to the docker group..."
    sudo usermod -aG docker $USER
    echo "User added to the docker group. Please log out and log back in for this to take effect."
    echo "After logging back in, run this script again."
    exit 0
fi

# Create password file
create_password_file

# Check if docker-compose.yaml exists and run it
if [ -f "docker-compose.yaml" ]; then
    echo "docker-compose.yaml found. Running Docker Compose..."
    docker-compose up -d
else
    echo "docker-compose.yaml not found. Please make sure it is in the current directory."
fi