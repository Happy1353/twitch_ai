"""
Avatar Animator - Handles avatar display and lip sync animation
"""
import cv2
import numpy as np
import threading
import time
from pathlib import Path
from typing import Optional
import config


class AvatarAnimator:
    """Animates avatar with lip sync"""
    
    def __init__(self):
        """Initialize avatar animator"""
        self.window_name = f"{config.CHARACTER_NAME} - Twitch Stream"
        
        # Animation state
        self.is_talking = False
        self.mouth_open = False
        self.animation_thread: Optional[threading.Thread] = None
        self.running = False
        
        # Load avatar images
        self.idle_image: Optional[np.ndarray] = None
        self.talking_image: Optional[np.ndarray] = None
        self.current_frame: Optional[np.ndarray] = None
        
        # Create assets directory
        Path("assets").mkdir(exist_ok=True)
        
        # Try to load images
        self._load_images()
        
        # If images don't exist, create placeholder
        if self.idle_image is None:
            self._create_placeholder_images()
    
    def _load_images(self):
        """Load avatar images from disk"""
        try:
            if Path(config.AVATAR_IMAGE_PATH).exists():
                self.idle_image = cv2.imread(config.AVATAR_IMAGE_PATH)
                print(f"✓ Загружено изображение: {config.AVATAR_IMAGE_PATH}")
        except Exception as e:
            print(f"⚠ Не удалось загрузить idle image: {e}")
        
        try:
            if Path(config.AVATAR_MOUTH_OPEN_PATH).exists():
                self.talking_image = cv2.imread(config.AVATAR_MOUTH_OPEN_PATH)
                print(f"✓ Загружено изображение: {config.AVATAR_MOUTH_OPEN_PATH}")
        except Exception as e:
            print(f"⚠ Не удалось загрузить talking image: {e}")
    
    def _create_placeholder_images(self):
        """Create placeholder avatar images with attractive anime-style girl"""
        print("📝 Создание placeholder изображений...")
        
        # Create base canvas
        width, height = config.WINDOW_WIDTH, config.WINDOW_HEIGHT
        
        # Idle image - attractive anime-style placeholder
        idle_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Gradient background (purple to pink)
        for i in range(height):
            r = int(180 + (i / height) * 75)  # 180 to 255
            g = int(120 - (i / height) * 50)  # 120 to 70
            b = int(200 - (i / height) * 50)  # 200 to 150
            idle_img[i, :] = [b, g, r]
        
        # Draw face circle (skin tone)
        center_x, center_y = width // 2, height // 2
        face_radius = 200
        cv2.circle(idle_img, (center_x, center_y), face_radius, (200, 180, 255), -1)
        cv2.circle(idle_img, (center_x, center_y), face_radius, (150, 120, 200), 3)
        
        # Draw eyes (big anime eyes)
        eye_y = center_y - 40
        left_eye_x = center_x - 60
        right_eye_x = center_x + 60
        
        # White of eyes
        cv2.ellipse(idle_img, (left_eye_x, eye_y), (30, 40), 0, 0, 360, (255, 255, 255), -1)
        cv2.ellipse(idle_img, (right_eye_x, eye_y), (30, 40), 0, 0, 360, (255, 255, 255), -1)
        
        # Pupils (with shine)
        cv2.circle(idle_img, (left_eye_x, eye_y + 5), 20, (100, 50, 150), -1)
        cv2.circle(idle_img, (right_eye_x, eye_y + 5), 20, (100, 50, 150), -1)
        cv2.circle(idle_img, (left_eye_x - 8, eye_y - 2), 8, (255, 255, 255), -1)
        cv2.circle(idle_img, (right_eye_x - 8, eye_y - 2), 8, (255, 255, 255), -1)
        
        # Eyelashes
        cv2.ellipse(idle_img, (left_eye_x, eye_y - 35), (32, 15), 0, 0, 180, (50, 30, 80), 2)
        cv2.ellipse(idle_img, (right_eye_x, eye_y - 35), (32, 15), 0, 0, 180, (50, 30, 80), 2)
        
        # Nose (small)
        nose_y = center_y + 20
        cv2.line(idle_img, (center_x, nose_y - 10), (center_x + 5, nose_y + 5), (180, 150, 220), 2)
        
        # Mouth closed (smile)
        mouth_y = center_y + 60
        cv2.ellipse(idle_img, (center_x, mouth_y - 10), (40, 20), 0, 0, 180, (200, 100, 150), 3)
        
        # Blush
        cv2.circle(idle_img, (center_x - 110, center_y + 30), 25, (180, 140, 255), -1)
        cv2.circle(idle_img, (center_x + 110, center_y + 30), 25, (180, 140, 255), -1)
        
        # Hair (long flowing hair)
        hair_color = (120, 70, 180)  # Purple hair
        cv2.ellipse(idle_img, (center_x, center_y - 80), (220, 180), 0, 180, 360, hair_color, -1)
        
        # Hair details
        cv2.ellipse(idle_img, (center_x - 150, center_y), (50, 200), 20, 0, 360, hair_color, -1)
        cv2.ellipse(idle_img, (center_x + 150, center_y), (50, 200), -20, 0, 360, hair_color, -1)
        
        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = config.CHARACTER_NAME
        text_size = cv2.getTextSize(text, font, 2, 3)[0]
        text_x = (width - text_size[0]) // 2
        cv2.putText(idle_img, text, (text_x, height - 100), font, 2, (255, 255, 255), 3)
        
        # Add subtitle
        subtitle = "AI Streamer"
        sub_size = cv2.getTextSize(subtitle, font, 1, 2)[0]
        sub_x = (width - sub_size[0]) // 2
        cv2.putText(idle_img, subtitle, (sub_x, height - 50), font, 1, (200, 200, 255), 2)
        
        self.idle_image = idle_img
        
        # Talking image - same but with open mouth
        talking_img = idle_img.copy()
        
        # Draw open mouth (oval)
        cv2.ellipse(talking_img, (center_x, mouth_y), (30, 40), 0, 0, 360, (100, 50, 80), -1)
        cv2.ellipse(talking_img, (center_x, mouth_y), (30, 40), 0, 0, 360, (200, 100, 150), 3)
        
        # Tongue (optional, makes it more expressive)
        cv2.ellipse(talking_img, (center_x, mouth_y + 15), (15, 10), 0, 0, 180, (150, 100, 180), -1)
        
        self.talking_image = talking_img
        
        # Save placeholder images
        cv2.imwrite(config.AVATAR_IMAGE_PATH, idle_img)
        cv2.imwrite(config.AVATAR_MOUTH_OPEN_PATH, talking_img)
        
        print(f"✓ Placeholder изображения созданы")
    
    def start(self):
        """Start avatar display"""
        self.running = True
        self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
        self.animation_thread.start()
        print(f"✓ Аватар запущен: {self.window_name}")
    
    def stop(self):
        """Stop avatar display"""
        self.running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1)
        cv2.destroyAllWindows()
    
    def _animation_loop(self):
        """Main animation loop"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        mouth_toggle_time = 0
        mouth_toggle_interval = 0.15  # Toggle mouth every 150ms when talking
        
        while self.running:
            current_time = time.time()
            
            # Select appropriate frame
            if self.is_talking:
                # Animate mouth opening/closing
                if current_time - mouth_toggle_time > mouth_toggle_interval:
                    self.mouth_open = not self.mouth_open
                    mouth_toggle_time = current_time
                
                frame = self.talking_image if self.mouth_open else self.idle_image
            else:
                frame = self.idle_image
            
            # Display frame
            if frame is not None:
                # Add status indicator
                display_frame = frame.copy()
                
                # Add talking indicator
                if self.is_talking:
                    cv2.circle(display_frame, (50, 50), 20, (0, 255, 0), -1)
                    cv2.putText(display_frame, "ГОВОРИТ", (80, 60), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.circle(display_frame, (50, 50), 20, (100, 100, 100), -1)
                    cv2.putText(display_frame, "СЛУШАЕТ", (80, 60), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 2)
                
                cv2.imshow(self.window_name, display_frame)
            
            # Handle key press (ESC to quit)
            key = cv2.waitKey(int(1000 / config.FRAME_RATE)) & 0xFF
            if key == 27:  # ESC
                self.running = False
                break
    
    def start_talking(self):
        """Start talking animation"""
        self.is_talking = True
        print("👄 Начало речи")
    
    def stop_talking(self):
        """Stop talking animation"""
        self.is_talking = False
        self.mouth_open = False
        print("🤐 Конец речи")

