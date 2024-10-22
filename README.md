<div align=center>
   <img width=150 src=https://github.com/FoPPi/GFormPassAPI/blob/master/docs/logo.png?raw=true alt='logo' />
   <h1>GFormPassAPI</h1>
</div>

## Description

This project is a [brief project type or description, e.g., "FastAPI-based donation platform using Docker"] designed to [key functionality, e.g., "process user donations securely and efficiently using a headless API system"]. It includes key features like user key generation, API integration, and real-time updates.

## Features

- **User Key Management**: Generate and activate user keys for secure API access.
- **Donation Handling**: Process and manage user donations with customizable amounts and currencies.
- **GPT Question Handling**: Send questions to GPT for automated processing and response.
- **Admin Controls**: Update user limits and manage expired questions efficiently.

## Setup Instructions

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FoPPi/GFormPassAPI.git
   ```

2. **Configure Environment Variables**:
   - Rename `.env.example` to `.env`.
   - Add your API keys, admin keys, and other necessary configurations.

3. **Run the project**:
   - Make the start script executable:
     ```bash
     chmod +x start.sh
     ```
   - Start the application:
     ```bash
     sh start.sh
     ```

4. **Access the API**:  
   The application will be available at `http://127.0.0.1:8000`.


## License

This project is licensed under the [RPL1.5 License](LICENSE.md).
