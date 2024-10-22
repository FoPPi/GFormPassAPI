# Use an official Node runtime as the parent image
FROM node:22.10.0-bullseye

# Set the working directory in the container
WORKDIR /GFormPassDocs

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your VitePress project
COPY . .

# Expose the port VitePress runs on
EXPOSE 5173

# Command to run the application
CMD ["npm", "run", "docs:dev", "--", "--host", "0.0.0.0"]