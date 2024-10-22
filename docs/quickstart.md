# Quickstart Guide

## Introduction

This guide provides step-by-step instructions for setting up a **FastAPI** application using **Docker** as the server.

## Prerequisites

Before starting, ensure the following:

- You are using a **Unix-based system** (e.g., Linux, macOS).

## Getting Started

### Step 1: Clone the Repository

1. Open a terminal and navigate to the directory where you want to clone the repository.
2. Run the following command:

```bash
git clone https://github.com/FoPPi/GFormPassAPI.git
```

### Step 2: Configure Environment Variables

1. Locate the `.env.example` file in the project directory.
2. Rename the file to `.env` and update the required environment variables with your keys.

### Step 3: Start the Application

1. Navigate to the project directory in your terminal.
2. Run the following commands to start the application:

```bash
chmod +x start.sh
sh start.sh
```

> After a few moments, all components will be up and running, and you can start using the API at `http://127.0.0.1:8000`.

### Step 4: Uninstall the Application

1. Navigate to the project directory in your terminal.
2. Run the following command to uninstall the application:

```bash
chmod +x uninstall.sh
sh uninstall.sh
```

## What's Next?

You are now ready to connect to the database or use the **GFormPassAPI**.