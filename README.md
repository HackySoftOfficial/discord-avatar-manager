# Discord Avatar Manager

Discord Avatar Manager is a powerful tool for managing and scheduling Discord avatar changes with ease. This application provides a user-friendly interface to add, generate, send, and schedule avatar updates for your Discord account.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Add multiple images to be used as Discord avatars
- Send images to update your Discord avatar
- Schedule avatar changes for later
- Generate AI images using Stable Diffusion
- Search and add images from the web
- Animated ASCII art display (when a code editor is running)
- User-friendly GUI built with PyQt6

## Installation

1. Clone the repository:
   ````
   git clone https://github.com/yourusername/discord-avatar-manager.git
   ```

2. Navigate to the project directory:
   ````
   cd discord-avatar-manager
   ```

3. Install the required dependencies:
   ````
   pip install -r requirements.txt
   ```

4. Set up your Discord token:
   - Create a `.env` file in the project root
   - Add your Discord token: `TOKEN=your_discord_token_here`

## Usage

1. Run the application:
   ````
   python main.py
   ```

2. Use the GUI to add images, generate AI images, or search for images online
3. Send images to update your Discord avatar
4. Schedule avatar changes for later using the scheduling feature

## Dependencies

This project relies on several Python libraries, including:

- PyQt6
- Pillow
- httpx
- BeautifulSoup4
- torch
- diffusers
- sentry-sdk
- python-dotenv
- nodriver
- colorama

For a complete list of dependencies, please refer to the `requirements.txt` file.

## Contributing

Contributions to the Discord Avatar Manager are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
