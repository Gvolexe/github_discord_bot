# GitHub-Discord Integration Bot

![GitHub Stars](https://img.shields.io/github/stars/gvolexe/github_discord_bot?style=social) ![GitHub Forks](https://img.shields.io/github/forks/gvolexe/github_discord_bot?style=social) ![License](https://img.shields.io/github/license/gvolexe/github_discord_bot)

## Table of Contents

- [Overview](#overview)
- [Inspiration](#inspiration)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
    - [Setting Up GitHub Webhooks](#setting-up-github-webhooks)
    - [Discord Bot Commands](#discord-bot-commands)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The **GitHub-Discord Integration Bot** is a powerful tool that bridges GitHub events with Discord channels. By leveraging GitHub webhooks and a Discord bot, this application ensures that your Discord community stays updated with real-time activities from your GitHub repositories. Whether it's push events, pull requests, issues, or releases, the bot captures these events and presents them in a structured and visually appealing manner within Discord.

## Inspiration

This project was created to help my robotics team [Unirevsals](https://github.com/Unirevsals) organize their code and collaborate more effectively.

## Features

- **Real-Time Notifications:** Receive instant updates in Discord for various GitHub events such as pushes, pull requests, issues, releases, and more.
- **Customizable Channels:** Assign specific Discord channels for different GitHub event types.
- **Interactive Commands:** Manage event handlers directly from Discord using intuitive commands.
- **Persistent Data Storage:** Ensures that message mappings and event data persist across bot restarts.
- **Secure Webhook Handling:** Validates incoming GitHub webhooks using HMAC signatures to ensure authenticity.
- **Extensible Architecture:** Easily add support for additional GitHub events or extend existing functionalities.

## Project Structure

```
github_discord_bot/
├── bot/
│   ├── __init__.py
│   ├── commands.py
│   ├── discord_bot.py
│   └── utils.py
├── handlers/
│   ├── __init__.py
│   └── github_handlers.py
├── flask_app/
│   ├── __init__.py
│   └── webhook.py
├── persistence/
│   ├── __init__.py
│   └── data_persistence.py
├── config.py
├── main.py
├── requirements.txt
├── data_store.json
└── README.md
```

- **bot/**: Contains all Discord bot-related modules, including command definitions and utility functions.
- **handlers/**: Houses event handler functions for different GitHub events.
- **flask_app/**: Sets up the Flask web server to receive and process GitHub webhooks.
- **persistence/**: Manages data storage and retrieval, ensuring persistence across sessions.
- **config.py**: Handles configuration settings, primarily through environment variables.
- **main.py**: The entry point of the application, initializing and running both the Discord bot and Flask server.
- **requirements.txt**: Lists all Python dependencies required for the project.
- **data_store.json**: Stores persistent data such as message mappings and event data.

## Prerequisites

Before setting up the GitHub-Discord Integration Bot, ensure you have the following:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Discord Account**: To create and manage the Discord bot.
- **GitHub Repository**: To set up webhooks for your project.
- **A Server or Hosting Service**: To run the Flask web server and Discord bot (e.g., AWS, Heroku, DigitalOcean).

## Installation

1. **Clone the Repository**
    
    ```bash
    git clone https://github.com/gvolexe/github_discord_bot.git
    cd github_discord_bot
    ```
    
2. **Create a Virtual Environment**
    
    It's recommended to use a virtual environment to manage dependencies.
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3. **Install Dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```
    

## Configuration

1. **Create a `.env` File**
    
    To manage sensitive information securely, create a `.env` file in the root directory. **Ensure that this file is added to `.gitignore` to prevent it from being committed to version control.**
    
    ```bash
    touch .env
    ```
    
2. **Populate the `.env` File**
    
    Open the `.env` file in your preferred text editor and add the following configurations:
    
    ```env
    # .env
    
    # Discord Bot Token (Obtain from Discord Developer Portal)
    DISCORD_TOKEN=your_discord_bot_token_here
    
    # Discord Channel IDs
    # DEFAULT_DISCORD_CHANNEL_ID: Channel for general GitHub events
    # ERROR_DISCORD_CHANNEL_ID: Channel for error notifications
    DISCORD_CHANNEL_ID=123456789012345678
    ERROR_DISCORD_CHANNEL_ID=123456789012345678
    
    # GitHub Webhook Secret (Set in GitHub repository settings)
    GITHUB_WEBHOOK_SECRET=your_github_webhook_secret_here
    
    # Additional Configuration Flags
    SEND_UNEXPECTED_EVENTS=True          # Whether to send events without specific handlers
    INCLUDE_HANDLER_INFO=True            # Whether to include handler information in embeds
    
    # Data Persistence
    DATA_STORE_FILE=data_store.json       # Path to the data persistence file
    ```
    
    **Configuration Details:**
    
    - **DISCORD_TOKEN**: The token for your Discord bot. Obtain this from the [Discord Developer Portal](https://discord.com/developers/applications).
    - **DISCORD_CHANNEL_ID**: The ID of the Discord channel where general GitHub events will be posted.
    - **ERROR_DISCORD_CHANNEL_ID**: The ID of the Discord channel where error notifications will be sent.
    - **GITHUB_WEBHOOK_SECRET**: A secret token to secure your GitHub webhooks. Set this in your GitHub repository settings and ensure it matches the one in the `.env` file.
    - **SEND_UNEXPECTED_EVENTS**: If set to `True`, the bot will send events that don't have specific handlers.
    - **INCLUDE_HANDLER_INFO**: If set to `True`, the embeds will include information about which handler processed the event.
    - **DATA_STORE_FILE**: The path to the JSON file used for data persistence.

## Running the Application

The application consists of two main components: the Discord bot and the Flask web server. These run concurrently to handle Discord interactions and GitHub webhooks, respectively.

1. **Start the Application**
    
    ```bash
    python main.py
    ```
    
    **What Happens:**
    
    - **Flask Server**: Runs on `http://0.0.0.0:25578` and listens for incoming GitHub webhook events at the `/github-webhook` endpoint.
    - **Discord Bot**: Connects to Discord using the provided token and starts listening for commands and interactions.
2. **Running as a Background Service**
    
    For production environments, it's recommended to run the application as a background service or use a process manager like `pm2`, `supervisord`, or Docker containers.
    
    **Using `screen` or `tmux`:**
    
    ```bash
    screen -S github_discord_bot
    python main.py
    # Press Ctrl+A then D to detach
    ```
    
    **Using `nohup`:**
    
    ```bash
    nohup python main.py &
    ```
    

## Usage

### Setting Up GitHub Webhooks

To enable GitHub to send event data to your application:

1. **Navigate to Your GitHub Repository Settings**
    
    Go to the repository you want to integrate and click on **Settings**.
    
2. **Add a New Webhook**
    
    - Click on **Webhooks** in the sidebar.
    - Click the **Add webhook** button.
3. **Configure the Webhook**
    
    - **Payload URL**: `http://your_server_ip:25578/github-webhook`
    - **Content type**: `application/json`
    - **Secret**: Use the same `GITHUB_WEBHOOK_SECRET` you set in your `.env` file.
    - **Which events would you like to trigger this webhook?**: Select **Let me select individual events** and choose the events you want to monitor (e.g., Push, Pull Request, Issues).
    - **Active**: Ensure this is checked.
4. **Save the Webhook**
    
    Click **Add webhook** to save.
    

### Discord Bot Commands

The Discord bot offers several commands to manage and interact with GitHub event handlers. Only users with **Administrator** permissions can execute these commands.

1. **`/togglehandler`**
    
    **Description**: Toggles a specific event handler on or off.
    
    **Usage**:
    
    ```bash
    /togglehandler <handler_name>
    ```
    
    **Example**:
    
    ```bash
    /togglehandler push
    ```
    
    **Response**:
    
    ```
    📢 **Handler 'push' has been ✅ enabled.**
    ```
    
2. **`/sethandlerchannel`**
    
    **Description**: Assigns a Discord channel to a specific event handler.
    
    **Usage**:
    
    ```bash
    /sethandlerchannel <handler_name> <#channel>
    ```
    
    **Example**:
    
    ```bash
    /sethandlerchannel push #github-events
    ```
    
    **Response**:
    
    ```
    📍 **Handler 'push' channel set to #github-events.**
    ```
    
3. **`/listhandlers`**
    
    **Description**: Lists all event handlers with their current status and assigned channels.
    
    **Usage**:
    
    ```bash
    /listhandlers
    ```
    
    **Response**:
    
    ![List Handlers](https://i.imgur.com/yourimage.png)
    
    _(The embed will display each handler's status and associated channel.)_
    

### Customizing Event Handlers

You can extend the bot to handle additional GitHub events by modifying the `handlers/github_handlers.py` and `bot/utils.py` files. Ensure that each new event type has corresponding handler functions and embed structures.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. **Fork the Project**
    
    Click the **Fork** button at the top right of this repository to create your own fork.
    
2. **Clone Your Fork**
    
    ```bash
    git clone https://github.com/gvolexe/github_discord_bot.git
    cd github_discord_bot
    ```
    
3. **Create a Branch**
    
    ```bash
    git checkout -b feature/YourFeatureName
    ```
    
4. **Make Your Changes**
    
    Implement your feature or bug fix. Ensure that your code adheres to the existing style and conventions.
    
5. **Commit Your Changes**
    
    ```bash
    git add .
    git commit -m "Add feature: YourFeatureName"
    ```
    
6. **Push to Your Fork**
    
    ```bash
    git push origin feature/YourFeatureName
    ```
    
7. **Open a Pull Request**
    
    Navigate to the original repository and click **Compare & pull request**. Provide a clear description of your changes and submit.
    

### Guidelines

- **Code Style**: Follow PEP 8 guidelines for Python code.
- **Documentation**: Update the README and in-code comments where necessary.
- **Testing**: Ensure that new features are tested and do not break existing functionalities.
- **Issue Tracking**: If you're fixing a bug or implementing a feature, consider opening an issue first to discuss it.

## License

Distributed under the [MIT License](https://chatgpt.com/c/LICENSE). See `LICENSE` for more information.

## Contact

Gvol - [gvol@nexusystems.org](mailto:gvol@nexusystems.org)

Project Link: [https://github.com/gvolexe/github_discord_bot](https://github.com/gvolexe/github_discord_bot)

---

