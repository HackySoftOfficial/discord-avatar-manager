import sentry_sdk
import httpx
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QScrollArea, QFrame, QFileDialog,
                             QMessageBox)
from PyQt6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush
from PyQt6.QtCore import Qt, QTimer
from tkinter import filedialog, messagebox
from PIL import Image, ImageFont
import base64
import os
import json
import time
import threading
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup
from io import BytesIO
import tempfile
import shutil
from nodriver import Browser
import torch
from diffusers import StableDiffusionPipeline
import sys
import colorama
from colorama import Fore, Back, Style
import psutil
import platform
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.INFO,   # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

# Initialize Sentry SDK
sentry_sdk.init(
    dsn="https://6dc04a85255eda10e972558e9923032a@o4506762449387520.ingest.us.sentry.io/4506762522722304",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Load environment variables
load_dotenv()

# Constants
COOKIES = {
    '__Secure-recent_mfa': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MjY5OTI0NjEsIm5iZiI6MTcyNjk5MjQ2MSwiZXhwIjoxNzI2OTkyNzYxLCJpc3MiOiJ1cm46ZGlzY29yZC1hcGkiLCJhdWQiOiJ1cm46ZGlzY29yZC1tZmEtcmVwcm9tcHQiLCJ1c2VyIjoxMjU5NTE2MDkyMjU1MTc0NjU4fQ.lo7rr4-Y2ancStx_dgf5dSpdy5hrh8Gp7ahyb9cO1K4safmoLqABBlEJX03KUGBtFl-9b3OGrTf_9W_fzmo0Qg',
    'OptanonAlertBoxClosed': '2024-09-22T08:01:24.323Z',
    'locale': 'en-US',
}

HEADERS = {
    'accept': '*/*',
    'authorization': os.getenv("TOKEN"),
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}

# Global variables
images = []
selected_image = None
scheduled_task = None
last_send_time = 0
temp_dir = tempfile.mkdtemp()

# Font setup
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
os.makedirs(FONT_DIR, exist_ok=True)

FONT_URLS = {
    'regular': r'c:\Users\Catdrout\Downloads\SF-Pro.ttf',  # Changed to raw string
    'bold': r'c:\Users\Catdrout\Downloads\SF-Pro-Tex.ttf',  # Changed to raw string
}

def download_font(font_type):
    font_path = os.path.join(FONT_DIR, f'Montserrat-{font_type.capitalize()}.ttf')
    if not os.path.exists(font_path):
        url = FONT_URLS[font_type.lower()]
        response = httpx.get(url)
        with open(font_path, 'wb') as f:
            f.write(response.content)
    return font_path

# Download fonts
REGULAR_FONT = download_font('regular')
BOLD_FONT = download_font('bold')

def update_image_database():
    """Updates the existing_images.json file with the current state of images."""
    global images
    with open(os.path.join(temp_dir, 'existing_images.json'), 'w') as json_file:
        json.dump(images, json_file)

def clear_images():
    """Clears all images from memory and disk, and resets the selected image."""
    global images, selected_image
    
    # Clear images from memory
    images = []
    selected_image = None
    
    # Clear images from disk
    for file in os.listdir(temp_dir):
        if file.endswith('.png') or file == 'existing_images.json':
            os.remove(os.path.join(temp_dir, file))
    
    # Update the image database (which will now be empty)
    update_image_database()
    
    QMessageBox.information(None, "Info", "All images have been cleared from memory and disk.")
    
    # Update the send button state
    update_send_button_state()

def add_images():
    """Adds new images to the list."""
    global images
    if selected_image is not None:
        QMessageBox.warning(None, "Warning", "Please clear the selected image before adding new images.")
        return

import sentry_sdk
import httpx
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QScrollArea, QFrame, QFileDialog,
                             QMessageBox)
from PyQt6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush
from PyQt6.QtCore import Qt, QTimer
from tkinter import filedialog, messagebox
from PIL import Image, ImageFont
import base64
import os
import json
import time
import threading
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup
from io import BytesIO
import tempfile
import shutil
from nodriver import Browser
import torch
from diffusers import StableDiffusionPipeline
import sys
import colorama
from colorama import Fore, Back, Style
import psutil
import platform
import subprocess
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.INFO,   # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

# Initialize Sentry SDK
sentry_sdk.init(
    dsn="https://6dc04a85255eda10e972558e9923032a@o4506762449387520.ingest.us.sentry.io/4506762522722304",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Load environment variables
load_dotenv()

# Constants
COOKIES = {
    '__Secure-recent_mfa': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MjY5OTI0NjEsIm5iZiI6MTcyNjk5MjQ2MSwiZXhwIjoxNzI2OTkyNzYxLCJpc3MiOiJ1cm46ZGlzY29yZC1hcGkiLCJhdWQiOiJ1cm46ZGlzY29yZC1tZmEtcmVwcm9tcHQiLCJ1c2VyIjoxMjU5NTE2MDkyMjU1MTc0NjU4fQ.lo7rr4-Y2ancStx_dgf5dSpdy5hrh8Gp7ahyb9cO1K4safmoLqABBlEJX03KUGBtFl-9b3OGrTf_9W_fzmo0Qg',
    'OptanonAlertBoxClosed': '2024-09-22T08:01:24.323Z',
    'locale': 'en-US',
}

HEADERS = {
    'accept': '*/*',
    'authorization': os.getenv("TOKEN"),
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}

# Global variables
images = []
selected_image = None
scheduled_task = None
last_send_time = 0
temp_dir = tempfile.mkdtemp()

# Font setup
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
os.makedirs(FONT_DIR, exist_ok=True)

FONT_URLS = {
    'regular': r'c:\Users\Catdrout\Downloads\SF-Pro.ttf',  # Changed to raw string
    'bold': r'c:\Users\Catdrout\Downloads\SF-Pro-Tex.ttf',  # Changed to raw string
}

def download_font(font_type):
    font_path = os.path.join(FONT_DIR, f'Montserrat-{font_type.capitalize()}.ttf')
    if not os.path.exists(font_path):
        url = FONT_URLS[font_type.lower()]
        response = httpx.get(url)
        with open(font_path, 'wb') as f:
            f.write(response.content)
    return font_path

# Download fonts
REGULAR_FONT = download_font('regular')
BOLD_FONT = download_font('bold')

def update_image_database():
    """Updates the existing_images.json file with the current state of images."""
    global images
    with open(os.path.join(temp_dir, 'existing_images.json'), 'w') as json_file:
        json.dump(images, json_file)

def clear_images():
    """Clears all images from memory and disk, and resets the selected image."""
    global images, selected_image
    
    # Clear images from memory
    images = []
    selected_image = None
    
    # Clear images from disk
    for file in os.listdir(temp_dir):
        if file.endswith('.png') or file == 'existing_images.json':
            os.remove(os.path.join(temp_dir, file))
    
    # Update the image database (which will now be empty)
    update_image_database()
    
    QMessageBox.information(None, "Info", "All images have been cleared from memory and disk.")
    
    # Update the send button state
    update_send_button_state()

def add_images():
    """Adds new images to the list."""
    global images
    if selected_image is not None:
        QMessageBox.warning(None, "Warning", "Please clear the selected image before adding new images.")
        return

    file_paths, _ = QFileDialog.getOpenFileNames(None, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
    if file_paths:
        for file_path in file_paths:
            img = Image.open(file_path).convert("RGB")
            img_id = f"img_{int(time.time() * 1000)}"  # Use timestamp as ID
            img_path = os.path.join(temp_dir, f'{img_id}.png')
            img.save(img_path)
            with open(img_path, 'rb') as img_file:
                base64_image = base64.b64encode(img_file.read()).decode()
            images.append({'id': img_id, 'data': f'data:image/png;base64,{base64_image}'})
        update_image_database()

def send_images():
    """Sends the next image to Discord."""
    global images, last_send_time

    # Check if enough time has passed since the last send
    current_time = time.time()
    if current_time - last_send_time < 60:  # 60 seconds = 1 minute
        print("Please wait before sending another image.")
        return

    if not images:
        print("No images to send.")
        return

    image = images.pop(0)  # Get the first image from the list
    
    # Open the image file and encode it
    img_path = os.path.join(temp_dir, f"{image['id']}.png")
    with Image.open(img_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
    
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'authorization': os.getenv("TOKEN"),
        'content-type': 'application/json',
        'cookie': '; '.join([f'{k}={v}' for k, v in COOKIES.items()]),
        'origin': 'https://discord.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    }
    
    data = {
        "avatar": f"data:image/png;base64,{img_str}"
    }

    try:
        with httpx.Client() as client:
            response = client.patch(url, headers=headers, json=data)
            response.raise_for_status()
        print("Image sent successfully!")
        last_send_time = current_time
        update_send_button_state()
    except httpx.HTTPStatusError as e:
        print(f"Failed to send image. Status code: {e.response.status_code}")
        print(e.response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Remove the sent image file
    os.remove(img_path)
    update_image_database()

def load_existing_images():
    """Loads existing images from the temporary directory and JSON file."""
    global images
    images = []
    
    # Load images from the temporary directory
    for file in os.listdir(temp_dir):
        if file.lower().endswith('.png'):
            img_id = os.path.splitext(file)[0]
            img_path = os.path.join(temp_dir, file)
            with open(img_path, 'rb') as img_file:
                base64_image = base64.b64encode(img_file.read()).decode()
            images.append({'id': img_id, 'data': f'data:image/png;base64,{base64_image}'})
    
    # Load images from JSON file
    json_path = os.path.join(temp_dir, 'existing_images.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as json_file:
                json_images = json.load(json_file)
            images.extend(json_images)
        except json.JSONDecodeError:
            print("Error: existing_images.json is not a valid JSON file")
        except Exception as e:
            print(f"Error loading existing images: {e}")
    
    # Update the image database to ensure it's in sync with the current state
    update_image_database()
    
    # Check for AI-generated images and unlock the send button if found
    if any('data:image/png;base64' in img['data'] for img in images):
        update_send_button_state()  # Unlock the send button if AI images are found
    
    print(f"Loaded {len(images)} images")
    return len(images) > 0

def search_and_add_image(keyword):
    """Searches for an image using the given keyword and adds it to the images list."""
    global images
    
    try:
        # Perform the search using httpx and BeautifulSoup
        url = f"https://duckduckgo.com/?q={keyword}&ia=images&iax=images"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        
        with httpx.Client(http2=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the first image
            img_element = soup.select_one('img.tile--img__img')
            
            if not img_element:
                # If BeautifulSoup fails, use nodriver as fallback
                print("BeautifulSoup failed to find image. Using nodriver as fallback.")
                browser = Browser()
                browser.get(url)
                img_element = browser.find_element('img.tile--img__img')
                if not img_element:
                    raise Exception("No images found")
                img_url = img_element.get_attribute('src')
            else:
                img_url = img_element['src']
            
            # Download the image
            img_response = client.get(img_url)
            img_response.raise_for_status()
            img = Image.open(BytesIO(img_response.content)).convert("RGB")
        
        # Save and process the image
        img_id = f"img_{int(time.time() * 1000)}"
        img_path = os.path.join(temp_dir, f'{img_id}.png')
        img.save(img_path)
        with open(img_path, 'rb') as img_file:
            base64_image = base64.b64encode(img_file.read()).decode()
        
        # Add the image to the list
        images.append({'id': img_id, 'data': f'data:image/png;base64,{base64_image}'})
        
        # Update the image database
        update_image_database()
        
        # Update the send button state
        update_send_button_state()
        
        QMessageBox.information(None, "Success", f"Image for '{keyword}' has been added.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to find or add image: {str(e)}")

def update_send_button_state():
    """Updates the state of the Send Images button."""
    def update():
        if images:
            root.send_images_button.setEnabled(True)
        else:
            root.send_images_button.setEnabled(False)
    
    if threading.current_thread() is threading.main_thread():
        update()
    else:
        root.update_send_button_state.emit()

def schedule_image_change(delay_minutes):
    """Schedules an image change after the specified delay."""
    global scheduled_task
    if scheduled_task:
        QMessageBox.warning(None, "Warning", "A task is already scheduled. Please cancel it first.")
        return
    if not images:
        QMessageBox.warning(None, "Warning", "No images available to schedule.")
        return
    
    scheduled_task = threading.Timer(delay_minutes * 60, send_images)
    scheduled_task.start()
    QMessageBox.information(None, "Info", f"Image change scheduled in {delay_minutes} minutes.")

def cancel_scheduled_task():
    """Cancels the scheduled image change task."""
    global scheduled_task
    if scheduled_task:
        scheduled_task.cancel()
        scheduled_task = None
        QMessageBox.information(None, "Info", "Scheduled task has been cancelled.")
    else:
        QMessageBox.information(None, "Info", "No task currently scheduled.")

# Add these new global variables
stable_diffusion_model = None

def load_stable_diffusion_model():
    """Loads the Stable Diffusion model."""
    global stable_diffusion_model
    if stable_diffusion_model is None:
        stable_diffusion_model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
        if torch.cuda.is_available():
            stable_diffusion_model.to("cuda")
        else:
            stable_diffusion_model.to("cpu")

def generate_stable_diffusion_image(prompt):
    """Generates an image using Stable Diffusion based on the given prompt."""
    global images, stable_diffusion_model
    
    try:
        logging.info(f"Generating image for prompt: '{prompt}'")
        load_stable_diffusion_model()
        
        with torch.no_grad():
            image = stable_diffusion_model(prompt, num_inference_steps=50).images[0]
        
        # Save and process the image
        img_id = f"img_{int(time.time() * 1000)}"
        img_path = os.path.join(temp_dir, f'{img_id}.png')
        image.save(img_path)
        with open(img_path, 'rb') as img_file:
            base64_image = base64.b64encode(img_file.read()).decode()
        
        # Add the image to the list
        images.append({'id': img_id, 'data': f'data:image/png;base64,{base64_image}'})
        
        # Update the image database
        update_image_database()
        
        # Update the send button state
        update_send_button_state()
        
        QMessageBox.information(None, "Success", f"Stable Diffusion image for '{prompt}' has been generated and added.")
        logging.info(f"Image generated successfully for prompt: '{prompt}'")
    except Exception as e:
        logging.error(f"Failed to generate Stable Diffusion image: {str(e)}")
        QMessageBox.critical(None, "Error", f"Failed to generate Stable Diffusion image: {str(e)}")

def is_code_editor_running():
    """Check if any known code editor is running on the system."""
    code_editors = {
        'Windows': ['code.exe', 'atom.exe', 'sublime_text.exe', 'pycharm64.exe', 'intellij64.exe'],
        'Darwin': ['Visual Studio Code', 'Atom', 'Sublime Text', 'PyCharm', 'IntelliJ IDEA'],
        'Linux': ['code', 'atom', 'sublime_text', 'pycharm', 'idea']
    }
    
    system = platform.system()
    if system == 'Windows':
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in code_editors[system]:
                return True
    elif system in ['Darwin', 'Linux']:
        for editor in code_editors[system]:
            try:
                subprocess.run(['pgrep', '-f', editor], check=True, stdout=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                pass
    return False

def animate_ascii_art():
    """Display animated ASCII art if a code editor is running."""
    if not is_code_editor_running():
        return

    ascii_art = """
       ▌ ▐·▄▄▄ .▄▄▄  ▄▄▄ . ▐ ▄  ▄▄ • ▪   ▐ ▄ ▄▄▄ .▄▄▄ .▄▄▄  ▄▄▄ .·▄▄▄▄     ▄▄▄·  ▌ ▐· ▄▄▄· ▄▄▄▄▄ ▄▄▄· ▄▄▄    • ▌ ▄ ·.  ▄▄▄·  ▐ ▄  ▄▄▄·  ▄▄ • ▄▄▄ .▄▄▄  
 ▄█▀▄ ▪█·█▌▀▄.▀·▀▄ █·▀▄.▀·•█▌▐█▐█ ▀ ▪██ •█▌▐█▀▄.▀·▀▄.▀·▀▄ █·▀▄.▀·██· ██   ▐█ ▀█ ▪█·█▌▐█ ▀█ •██  ▐█ ▀█ ▐▀▀▄   ▐█ ▌▐▌▐█·▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄▐▀▀▄ 
▐█▌.▐▌▐█▐█•▐▀▀▪▄▐▀▀▄ ▐▀▀▪▄▐█▐▐▌▄█ ▀█▄▐█·▐█▐▐▌▐▀▀▪▄▐▀▀▪▄▐▀▀▄ ▐▀▀▪▄▐█▪ ▐█▌  ▄█▀▀█ ▐█▐█•▄█▀▀█  ▐█.▪▄█▀▀█ ▐█•█▌  ██ ██▌▐█▌▐█▪ ▐▌██▐█▌▐█▪ ▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
▐█▌.▐▌ ███ ▐█▄▄▌▐█•█▌▐█▄▄▌██▐█▌▐█▄▪▐█▐█▌██▐█▌▐█▄▄▌▐█▄▄▌▐█•█▌▐█▄▄▌██. ██   ▐█▪ ▐▌ ███ ▐█▪ ▐▌ ▐█▌·▐█▪ ▐▌▐█•█▌  ██ ██▌▐█▌▐█▪ ▐▌██▐█▌▐█▪ ▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
 ▀█▄▀▪. ▀   ▀▀▀ .▀  ▀ ▀▀▀ ▀▀ █▪·▀▀▀▀ ▀▀▀▀▀ █▪ ▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀ ▀▀▀▀▀•    ▀  ▀ . ▀   ▀  ▀  ▀▀▀  ▀  ▀ .▀  ▀  ▀▀  █▪▀▀▀ ▀  ▀ ▀▀ █▪ ▀  ▀ ·▀▀▀▀  ▀▀▀ .▀  ▀
    """
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    color_index = 0
    
    for _ in range(30):  # Display for about 3 seconds
        if platform.system() == 'Windows':
            os.system('cls')  # Clear console on Windows
        else:
            os.system('clear')  # Clear console on Unix-based systems
        
        colored_art = ""
        for char in ascii_art:
            if char != '\n':
                colored_art += colors[color_index] + char + Style.RESET_ALL
                color_index = (color_index + 1) % len(colors)
            else:
                colored_art += char
        print(colored_art)
        time.sleep(0.1)
        color_index = (color_index + 1) % len(colors)
    
    # Clear the console after animation
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Avatar Manager")
        self.setGeometry(100, 100, 700, 800)

        # Set macOS title bar style
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # Set background image
        self.set_background_image()

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Create a widget for the scroll area content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        # Welcome message and instructions
        welcome_label = QLabel("Discord Avatar Manager")
        welcome_label.setFont(QFont("SF Pro", 28, QFont.Weight.Bold))
        scroll_layout.addWidget(welcome_label)

        subtitle_label = QLabel("Manage and schedule your Discord avatar changes with ease.")
        subtitle_label.setFont(QFont("SF Pro", 16))
        scroll_layout.addWidget(subtitle_label)

        instructions = (
            "1. Add images using the 'Add Images' button or generate with AI.\n"
            "2. Send an image to update your Discord avatar.\n"
            "3. Schedule avatar changes for later.\n"
            "4. Clear all images when you're done."
        )
        instructions_label = QLabel(instructions)
        instructions_label.setFont(QFont("SF Pro", 14))
        instructions_label.setWordWrap(True)
        scroll_layout.addWidget(instructions_label)

        # Image Management Section
        image_management_label = QLabel("Image Management")
        image_management_label.setFont(QFont("SF Pro", 20, QFont.Weight.Bold))
        scroll_layout.addWidget(image_management_label)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear All Images")
        clear_button.clicked.connect(clear_images)
        add_button = QPushButton("Add Images")
        add_button.clicked.connect(add_images)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(add_button)
        scroll_layout.addLayout(button_layout)

        self.send_images_button = QPushButton("Send Images")
        self.send_images_button.clicked.connect(send_images)
        scroll_layout.addWidget(self.send_images_button)

        # Scheduling Section
        schedule_label = QLabel("Schedule Image Change")
        schedule_label.setFont(QFont("SF Pro", 20, QFont.Weight.Bold))
        scroll_layout.addWidget(schedule_label)

        delay_layout = QHBoxLayout()
        self.delay_entry = QLineEdit()
        self.delay_entry.setPlaceholderText("Delay in minutes")
        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.schedule_image_change)
        delay_layout.addWidget(self.delay_entry)
        delay_layout.addWidget(schedule_button)
        scroll_layout.addLayout(delay_layout)

        cancel_button = QPushButton("Cancel Scheduled Task")
        cancel_button.clicked.connect(cancel_scheduled_task)
        scroll_layout.addWidget(cancel_button)

        # AI Image Generation Section
        ai_label = QLabel("AI Image Generation")
        ai_label.setFont(QFont("SF Pro", 20, QFont.Weight.Bold))
        scroll_layout.addWidget(ai_label)

        self.prompt_entry = QLineEdit()
        self.prompt_entry.setPlaceholderText("Enter prompt for image generation")
        scroll_layout.addWidget(self.prompt_entry)

        generate_button = QPushButton("Generate with Stable Diffusion")
        generate_button.clicked.connect(self.generate_stable_diffusion_image)
        scroll_layout.addWidget(generate_button)

        # Status bar
        self.statusBar().showMessage("Ready")

        # Set initial state of Send Images button
        self.update_send_button_state()

    def update_send_button_state(self):
        self.send_images_button.setEnabled(bool(images))

    def schedule_image_change(self):
        try:
            delay_minutes = int(self.delay_entry.text())
            schedule_image_change(delay_minutes)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number of minutes.")

    def generate_stable_diffusion_image(self):
        prompt = self.prompt_entry.text()
        generate_stable_diffusion_image(prompt)

    def set_background_image(self):
        # Optionally set a background color if no image is available
        palette = QPalette()
        # Uncomment the next line to set a default background color (e.g., light gray)
        # palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))  # Light gray background
        self.setPalette(palette)

def create_ui():
    global root
    app = QApplication(sys.argv)
    root = MainWindow()
    root.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:        
        # Display the animated ASCII art
        animate_ascii_art()
        
        create_ui()
    finally:
        # Clean up the temporary directory when the program exits
        shutil.rmtree(temp_dir, ignore_errors=True)