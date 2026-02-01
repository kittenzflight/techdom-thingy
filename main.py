import os
import sys
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import random
import threading
import time
import ctypes
import webbrowser
import platform
from queue import Queue

# Fix paths for EXE
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Queues for popup requests
image_popup_queue = Queue()
text_popup_queue = Queue()

def show_image_popup_window(image_path, duration=3000):
    """Show image popup window (must be called from main thread)"""
    try:
        popup = tk.Toplevel()
        popup.title("Popup Image")
        
        img = Image.open(image_path)
        max_size = (800, 600)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(popup, image=photo)
        label.image = photo
        label.pack()
        
        label.bind("<Button-1>", lambda e: popup.destroy())
        
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f'+{x}+{y}')
        
        popup.after(duration, popup.destroy)
        popup.bind("<Escape>", lambda e: popup.destroy())
        popup.attributes('-topmost', True)
        
    except Exception as e:
        pass

def show_text_popup_window(message, duration=3000):
    """Show text popup window (must be called from main thread)"""
    try:
        popup = tk.Toplevel()
        popup.title("Message")
        
        label = tk.Label(popup, text=message, font=("Arial", 16), padx=30, pady=20)
        label.pack()
        
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f'+{x}+{y}')
        
        popup.after(duration, popup.destroy)
        popup.bind("<Escape>", lambda e: popup.destroy())
        popup.attributes('-topmost', True)
        
    except Exception as e:
        pass

def check_popup_queues(root):
    """Check queues and show popups in main thread"""
    try:
        # Check image queue
        if not image_popup_queue.empty():
            image_path, duration = image_popup_queue.get_nowait()
            show_image_popup_window(image_path, duration)
        
        # Check text queue
        if not text_popup_queue.empty():
            message, duration = text_popup_queue.get_nowait()
            show_text_popup_window(message, duration)
    except:
        pass
    
    # Check again in 100ms
    root.after(100, lambda: check_popup_queues(root))

def get_image_files(folder="images"):
    """Get all image files from folder"""
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    folder_path = os.path.join(application_path, folder)
    
    if not os.path.exists(folder_path):
        return []
    
    images = [f for f in os.listdir(folder_path) 
              if f.lower().endswith(image_extensions)]
    
    return images

def queue_random_image_popup(duration=3000):
    """Queue a random image popup"""
    images = get_image_files("images")
    
    if images:
        random_image = random.choice(images)
        image_path = os.path.join(application_path, "images", random_image)
        
        if os.path.exists(image_path):
            image_popup_queue.put((image_path, duration))

def image_popup_scheduler(min_interval=5, max_interval=15, duration=3000):
    """Schedule random image popups at intervals"""
    while True:
        queue_random_image_popup(duration)
        wait_time = random.randint(min_interval, max_interval)
        time.sleep(wait_time)

def queue_random_text_popup(duration=3000):
    """Queue a random text popup"""
    messages = [
        "Hello pet!",
        "such a slut",
        "you belong to me",
        "your pc is mine",
        "good clicksluts just need to surrender to me",
        "I own you",
        "Be a good pet and surrender",
        "you will never be free from me",
        "resist all you want, you belong to me",
        "I am always watching you", 
        "you can't escape me",
        "submit to your owner",
        "Naugty pets get their ip revealed",
        "you are mine forever",
        "there's no escape",
        "you will always be my pet",
        "obedience is your only option",
        "you are nothing without me",
        "give in to your owner",
        "your fate is sealed",
        "you will always be under my control"
        "Surrender is the only option",
        "you are destined to be my pet"
        "Be a good pet and obey",
        "your resistance is futile",
        "you will always be mine",
        "there's no running away from me",
        "you belong to me now",
        "obedience is your destiny",
        
    ]
    
    message = random.choice(messages)
    text_popup_queue.put((message, duration))

def text_popup_scheduler(min_interval=5, max_interval=15, duration=3000):
    """Schedule random text popups at intervals"""
    while True:
        queue_random_text_popup(duration)
        wait_time = random.randint(min_interval, max_interval)
        time.sleep(wait_time)

# ============= WALLPAPER FUNCTIONS =============

def get_wallpaper_files(folder="wallpaper"):
    """Get all wallpaper files from folder"""
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    folder_path = os.path.join(application_path, folder)
    
    if not os.path.exists(folder_path):
        return []
    
    wallpapers = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(image_extensions)]
    
    return wallpapers

def set_wallpaper(image_path):
    """Set desktop wallpaper (cross-platform)"""
    
    system = platform.system()
    
    if system == "Windows":
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            bmp_path = os.path.join(application_path, 'temp_wallpaper.bmp')
            img.save(bmp_path, 'BMP')
            abs_bmp_path = os.path.abspath(bmp_path)
            
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, abs_bmp_path, 3
            )
            return True
        except:
            return False
            
    elif system == "Linux":
        try:
            import subprocess
            abs_path = os.path.abspath(image_path)
            
            subprocess.run([
                'gsettings', 'set', 
                'org.gnome.desktop.background', 
                'picture-uri', 
                f'file://{abs_path}'
            ], check=False, capture_output=True)
            
            subprocess.run([
                'gsettings', 'set', 
                'org.gnome.desktop.background', 
                'picture-uri-dark', 
                f'file://{abs_path}'
            ], check=False, capture_output=True)
            
            return True
        except:
            return False
    
    return False

def change_wallpaper_randomly(folder="wallpaper"):
    """Change desktop wallpaper to a random image"""
    wallpapers = get_wallpaper_files(folder)
    
    if wallpapers:
        random_wallpaper = random.choice(wallpapers)
        wallpaper_path = os.path.join(application_path, folder, random_wallpaper)
        set_wallpaper(wallpaper_path)

def wallpaper_changer_forever(interval_hours=7):
    """Change wallpaper every specified hours"""
    change_wallpaper_randomly("wallpaper")
    
    interval_seconds = interval_hours * 3600
    while True:
        time.sleep(interval_seconds)
        change_wallpaper_randomly("wallpaper")


if __name__ == "__main__":
    # Open URL once at startup
    webbrowser.open("https://iplogger.com/2qNgG4")
    
    # Image popup settings
    IMAGE_MIN_INTERVAL = 10   
    IMAGE_MAX_INTERVAL = 30
    IMAGE_DURATION = 3000
    
    # Text popup settings
    TEXT_MIN_INTERVAL = 15
    TEXT_MAX_INTERVAL = 45
    TEXT_DURATION = 4000
    
    # Wallpaper settings
    WALLPAPER_INTERVAL_HOURS = 7
    
    # Start image popup scheduler thread
    image_thread = threading.Thread(
        target=image_popup_scheduler, 
        args=(IMAGE_MIN_INTERVAL, IMAGE_MAX_INTERVAL, IMAGE_DURATION),
        daemon=True
    )
    image_thread.start()
    
    # Start text popup scheduler thread
    text_thread = threading.Thread(
        target=text_popup_scheduler,
        args=(TEXT_MIN_INTERVAL, TEXT_MAX_INTERVAL, TEXT_DURATION),
        daemon=True
    )
    text_thread.start()
    
    # Start wallpaper changer thread
    wallpaper_thread = threading.Thread(
        target=wallpaper_changer_forever,
        args=(WALLPAPER_INTERVAL_HOURS,),
        daemon=True
    )
    wallpaper_thread.start()
    
    # Create invisible main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Start checking for popup requests
    check_popup_queues(root)
    
    # Run tkinter main loop (required for popups to work)
    root.mainloop()