"""
Avatar Animator - Handles avatar display and lip sync animation (pygame version for macOS)
"""
import pygame
import numpy as np
import cv2
import time
from pathlib import Path
from typing import Optional
from PIL import Image
import config


class AvatarAnimator:
    """Animates avatar with lip sync using pygame"""
    
    def __init__(self):
        """Initialize avatar animator"""
        self.window_name = f"{config.CHARACTER_NAME} - Twitch Stream"
        
        # Animation state
        self.is_talking = False
        self.mouth_open = False
        self.running = False
        
        # Load avatar images
        self.idle_surface: Optional[pygame.Surface] = None
        self.talking_surface: Optional[pygame.Surface] = None
        
        # Create assets directory
        Path("assets").mkdir(exist_ok=True)
        
        # Initialize pygame
        pygame.init()
        
        # Try to load images (using OpenCV for creation, pygame for display)
        self._load_or_create_images()
        
    def _load_or_create_images(self):
        """Load avatar images or create placeholders"""
        # Check if images exist
        if not Path(config.AVATAR_IMAGE_PATH).exists() or not Path(config.AVATAR_MOUTH_OPEN_PATH).exists():
            self._create_placeholder_images()
        
        # Load images with PIL (better format support)
        try:
            if Path(config.AVATAR_IMAGE_PATH).exists():
                img = Image.open(config.AVATAR_IMAGE_PATH)
                img = img.convert('RGB')
                img = img.resize((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
                self.idle_surface = self._pil_to_pygame(img)
                print(f"✓ Загружено изображение: {config.AVATAR_IMAGE_PATH}")
        except Exception as e:
            print(f"⚠ Не удалось загрузить idle image: {e}")
        
        try:
            if Path(config.AVATAR_MOUTH_OPEN_PATH).exists():
                img = Image.open(config.AVATAR_MOUTH_OPEN_PATH)
                img = img.convert('RGB')
                img = img.resize((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
                self.talking_surface = self._pil_to_pygame(img)
                print(f"✓ Загружено изображение: {config.AVATAR_MOUTH_OPEN_PATH}")
        except Exception as e:
            print(f"⚠ Не удалось загрузить talking image: {e}")
    
    def _pil_to_pygame(self, pil_image):
        """Convert PIL image to pygame surface"""
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        
        return pygame.image.fromstring(data, size, mode)
    
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
        
        # Talking image - same but with open mouth
        talking_img = idle_img.copy()
        
        # Draw open mouth (oval)
        cv2.ellipse(talking_img, (center_x, mouth_y), (30, 40), 0, 0, 360, (100, 50, 80), -1)
        cv2.ellipse(talking_img, (center_x, mouth_y), (30, 40), 0, 0, 360, (200, 100, 150), 3)
        
        # Tongue (optional, makes it more expressive)
        cv2.ellipse(talking_img, (center_x, mouth_y + 15), (15, 10), 0, 0, 180, (150, 100, 180), -1)
        
        # Save placeholder images
        cv2.imwrite(config.AVATAR_IMAGE_PATH, idle_img)
        cv2.imwrite(config.AVATAR_MOUTH_OPEN_PATH, talking_img)
        
        print(f"✓ Placeholder изображения созданы")
        
        # Convert to pygame surfaces
        idle_img_rgb = cv2.cvtColor(idle_img, cv2.COLOR_BGR2RGB)
        talking_img_rgb = cv2.cvtColor(talking_img, cv2.COLOR_BGR2RGB)
        
        self.idle_surface = pygame.surfarray.make_surface(np.transpose(idle_img_rgb, (1, 0, 2)))
        self.talking_surface = pygame.surfarray.make_surface(np.transpose(talking_img_rgb, (1, 0, 2)))
    
    def start(self):
        """Start avatar display (must be called from main thread)"""
        self.running = True
        print(f"✓ Аватар готов к запуску: {self.window_name}")
    
    def stop(self):
        """Stop avatar display"""
        self.running = False
        pygame.quit()
    
    def update(self, screen, clock):
        """
        Update and draw avatar (call this from main loop)
        
        Args:
            screen: pygame display surface
            clock: pygame clock for FPS control
        """
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return False
        
        # Select appropriate frame
        if self.is_talking:
            # Animate mouth opening/closing
            frame_time = time.time() % 0.3  # Toggle every 300ms
            if frame_time < 0.15:
                current_surface = self.talking_surface
            else:
                current_surface = self.idle_surface
        else:
            current_surface = self.idle_surface
        
        # Draw frame
        if current_surface is not None:
            screen.blit(current_surface, (0, 0))
            
            # Draw status indicator
            font = pygame.font.SysFont('Arial', 24, bold=True)
            if self.is_talking:
                pygame.draw.circle(screen, (0, 255, 0), (50, 50), 20)
                text = font.render("ГОВОРИТ", True, (0, 255, 0))
                screen.blit(text, (80, 35))
            else:
                pygame.draw.circle(screen, (100, 100, 100), (50, 50), 20)
                text = font.render("СЛУШАЕТ", True, (150, 150, 150))
                screen.blit(text, (80, 35))
        
        pygame.display.flip()
        clock.tick(config.FRAME_RATE)
        
        return True
    
    def start_talking(self):
        """Start talking animation"""
        self.is_talking = True
        print("👄 Начало речи")
    
    def stop_talking(self):
        """Stop talking animation"""
        self.is_talking = False
        self.mouth_open = False
        print("🤐 Конец речи")
