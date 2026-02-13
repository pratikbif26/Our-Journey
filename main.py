import pygame
import random
import os
import json

# --- 1. Configuration ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_SPEED = 3
GAP_SIZE = 175 

# --- Retro Color Palette ---
C_BG_PINK = (255, 192, 203)
C_DEEP_RED = (200, 40, 60)
C_BRIGHT_RED = (255, 80, 80)
C_WHITE = (255, 255, 255)
C_BLACK = (20, 20, 20)
C_GREEN = (50, 205, 50)
C_SHADOW = (80, 20, 30)

GALLERY_ITEMS = [
    {
        "id": 0, "price": 0, "img": "photo1.jpg", "unlocked": True,
        "msg": "I remember watching you leave this day and feeling a strange emptiness I couldn't quite explain. It didn't take long to realize why: I hadn't just started missing you; I had started falling for you."
    },
    {
        "id": 1, "price": 0, "img": "photo2.jpg", "unlocked": False,
        "msg": "On our second group trip, I kept sticking close to you. Every picture was an excuse to look at you longer. When our eyes finally met, we both just knew that what we felt was special."
    },
    {
        "id": 2, "price": 0, "img": "photo3.jpg", "unlocked": False,
        "msg": "The week after the confession was pure magic. Life felt complete and I was at my absolute happiest. Our first kiss changed everything—I haven't been able to stop myself since. ❤️"
    },
    {
        "id": 3, "price": 0, "img": "photo4.jpg", "unlocked": False,
        "msg": "That weekend was pure bliss. Our bucket list was basically just food, food, and food—which is so 'us.' But being away from everything and everyone, just focused on you, made it the most perfect date. I'm still so reminiscent of those moments where it was just us against the world. ❤️"
    },
    {
        "id": 4, "price": 0, "img": "photo5.jpg", "unlocked": False,
        "msg": "Jodhpur wasn't exactly a 'study' trip, was it? Cruising through those narrow blue alleys on our scooty with the wind in our faces... those moments were pure magic. Top-tier memories for sure."
    },
    {
        "id": 5, "price": 0, "img": "photo6.jpg", "unlocked": False,
        "msg": "Finding our 'regular' food spots was a win, but the real highlight was that dance. Watching the fireworks under the stars... it felt like the world had gone quiet just for us. ❤️"
    },
    {
        "id": 6, "price": 0, "img": "photo7.jpg", "unlocked": False, "rotate": True,
        "msg": "The fights didn't stop, but neither did we. No matter how hard it gets, we still choose each other at the end of the day. This is proof that we’re stronger than any argument. Through it all, always. ✨"
    },
    {
        "id": 7, "price": 0, "img": "photo8.jpg", "unlocked": False, "rotate": True,
        "msg": "Our trip to Udaipur, the City of Love, was pure magic. The sunsets and the food were great, but you looked finer than any view. I didn't want it to end—let's hope for more of these times together! ❤️"
    },
]

# --- 2. Initialize Engine & Audio ---
pygame.mixer.pre_init(44100, -16, 2, 512) 
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Our Journey: Love Letters")
clock = pygame.time.Clock()

# --- Retro Fonts ---
try:
    font = pygame.font.SysFont("Consolas", 14, bold=True)
    small_font = pygame.font.SysFont("Consolas", 11, bold=True)
    big_font = pygame.font.SysFont("Consolas", 20, bold=True)
    title_font = pygame.font.SysFont("Consolas", 26, bold=True)
except:
    font = pygame.font.SysFont("Arial", 14, bold=True)
    small_font = pygame.font.SysFont("Arial", 11, bold=True)
    big_font = pygame.font.SysFont("Arial", 20, bold=True)
    title_font = pygame.font.SysFont("Arial", 26, bold=True)

# --- 3. Sound Loading ---
def load_sound(file_name, volume=1.0):
    if os.path.exists(file_name):
        s = pygame.mixer.Sound(file_name)
        s.set_volume(volume)
        return s
    return None

flap_snd = load_sound("flap.wav", 0.6)
score_snd = load_sound("score.wav", 0.7)

if os.path.exists("valentine_theme.mp3"):
    pygame.mixer.music.load("valentine_theme.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

# --- 4. Helper Functions ---
def save_data(hearts, unlocked_ids):
    # ANDROID PATH FIX
    try:
        from android.storage import primary_external_storage_path
        dir = primary_external_storage_path()
        path = os.path.join(dir, 'valentine_save_data.txt')
    except:
        path = 'save_data.txt'
        
    with open(path, "w") as f:
        json.dump({"hearts": hearts, "unlocked": unlocked_ids}, f)

def load_data():
    # ANDROID PATH FIX
    try:
        from android.storage import primary_external_storage_path
        dir = primary_external_storage_path()
        path = os.path.join(dir, 'valentine_save_data.txt')
    except:
        path = 'save_data.txt'

    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                for item in GALLERY_ITEMS:
                    if item["id"] in data["unlocked"]:
                        item["unlocked"] = True
                return data["hearts"]
        except: return 0
    return 0

def reset_progress():
    global total_hearts
    total_hearts = 0
    for item in GALLERY_ITEMS:
        if item["id"] == 0:
            item["unlocked"] = True
        else:
            item["unlocked"] = False
    save_data(0, [0])

def wrap_text(text, font_obj, max_width):
    words = text.split(' ')
    lines, current_line = [], []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font_obj.size(test_line)[0] < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

total_hearts = load_data()

# --- 5. UI Helpers (Pixel Style) ---
def draw_pixel_btn(surface, text, rect, bg_color, text_color=C_WHITE):
    shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
    pygame.draw.rect(surface, C_BLACK, shadow_rect)
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, C_BLACK, rect, 3)
    txt_surf = font.render(text, True, text_color)
    surface.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))

def draw_pixel_box(surface, rect, bg_color):
    s_rect = pygame.Rect(rect.x + 6, rect.y + 6, rect.width, rect.height)
    pygame.draw.rect(surface, C_BLACK, s_rect)
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, C_BLACK, rect, 3)

# --- 6. Asset Loading & Processing ---
def load_and_scale(file_name, target_size, alpha=True):
    if not os.path.exists(file_name): return None
    img = pygame.image.load(file_name)
    img = img.convert_alpha() if alpha else img.convert()
    return pygame.transform.smoothscale(img, target_size)

def apply_brightness_contrast(surface, brightness, contrast):
    """Lowers brightness for background"""
    if surface is None: return None
    new_surf = surface.copy()
    
    # Brightness (Darken)
    darken = pygame.Surface(new_surf.get_size()).convert_alpha()
    darken.fill((0, 0, 0, int((1.0 - brightness) * 255)))
    new_surf.blit(darken, (0, 0))
    
    # Contrast (Grey blend)
    contrast_surf = pygame.Surface(new_surf.get_size()).convert_alpha()
    contrast_surf.fill((128, 128, 128, int((1.0 - contrast) * 255)))
    new_surf.blit(contrast_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return new_surf

# Load Original Assets
BG_IMG = load_and_scale("valentine_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT), False)
BIRD_IMG = load_and_scale("heart_bird.png", (45, 40))
PIPE_TOP_IMG = load_and_scale("pipe_top.png", (60, 500))
PIPE_BOTTOM_IMG = load_and_scale("pipe_bottom.png", (60, 500))

# --- Process Assets ---

# 1. Darken BG for Gameplay (Brightness 0.94 = 6% Darker)
BG_PLAYING_IMG = apply_brightness_contrast(BG_IMG, 0.94, 0.94)

# --- 7. Classes ---
class Bird:
    def __init__(self):
        self.x, self.y, self.velocity = 50, SCREEN_HEIGHT // 2, 0
        self.rect = pygame.Rect(self.x + 10, self.y + 10, 25, 20)
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
    def flap(self):
        self.velocity = FLAP_STRENGTH
        if flap_snd: flap_snd.play()
    def draw(self):
        if BIRD_IMG: screen.blit(BIRD_IMG, (self.x, self.y))
        else: pygame.draw.circle(screen, C_DEEP_RED, (self.x + 22, int(self.y) + 20), 15)

class Pipe:
    def __init__(self, x):
        self.x, self.passed = x, False
        self.gap_center = random.randint(200, 450)
        self.top_rect = pygame.Rect(self.x + 15, 0, 30, self.gap_center - (GAP_SIZE // 2))
        self.bottom_rect = pygame.Rect(self.x + 15, self.gap_center + (GAP_SIZE // 2), 30, SCREEN_HEIGHT)
    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x, self.bottom_rect.x = self.x + 15, self.x + 15
    def draw(self):
        if PIPE_TOP_IMG and PIPE_BOTTOM_IMG:
            t = pygame.transform.smoothscale(PIPE_TOP_IMG, (60, self.top_rect.height))
            b = pygame.transform.smoothscale(PIPE_BOTTOM_IMG, (60, SCREEN_HEIGHT - self.bottom_rect.y))
            screen.blit(t, (self.x, 0)); screen.blit(b, (self.x, self.bottom_rect.y))
        else:
            pygame.draw.rect(screen, C_GREEN, self.top_rect)
            pygame.draw.rect(screen, C_BLACK, self.top_rect, 2)
            pygame.draw.rect(screen, C_GREEN, self.bottom_rect)
            pygame.draw.rect(screen, C_BLACK, self.bottom_rect, 2)

# --- 8. UI Screens ---
def show_about():
    global total_hearts
    showing = True
    message = "I coded this game as a special Valentine's gift for you, to remind us of the beautiful journey we've shared. Every heart you collect represents a moment I cherish. From our first trip to our quiet fireworks, I wanted to capture it all. I love you! ❤️"
    while showing:
        screen.fill(C_BG_PINK)
        
        box_rect = pygame.Rect(20, 60, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 140)
        draw_pixel_box(screen, box_rect, C_WHITE)
        
        title = big_font.render("About This Gift", True, C_DEEP_RED)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        wrapped = wrap_text(message, font, box_rect.width - 40)
        for i, line in enumerate(wrapped):
            txt = font.render(line, True, C_BLACK)
            screen.blit(txt, (40, 130 + (i * 25)))
            
        reset_btn = pygame.Rect(80, 440, 240, 40)
        draw_pixel_btn(screen, "RESET PROGRESS", reset_btn, C_DEEP_RED)

        back_btn = pygame.Rect(100, 500, 200, 50)
        draw_pixel_btn(screen, "BACK", back_btn, (80, 80, 80))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos): showing = False
                if reset_btn.collidepoint(event.pos): reset_progress()
        pygame.display.flip()

def draw_gallery():
    global total_hearts
    viewing = True
    while viewing:
        screen.fill(C_BG_PINK)
        
        header_rect = pygame.Rect(20, 10, SCREEN_WIDTH-40, 40)
        draw_pixel_box(screen, header_rect, C_WHITE)
        head_txt = big_font.render(f"Gallery - {total_hearts} ❤️", True, C_DEEP_RED)
        screen.blit(head_txt, (SCREEN_WIDTH//2 - head_txt.get_width()//2, 20))

        buttons = []
        for i, item in enumerate(GALLERY_ITEMS):
            color = C_GREEN if item["unlocked"] else C_DEEP_RED
            status_text = "OPEN" if item["unlocked"] else f"BUY: {item['price']} H"
            
            rect = pygame.Rect(50, 65 + (i * 58), 300, 40)
            draw_pixel_btn(screen, f"Letter {i+1}: {status_text}", rect, color)
            buttons.append((rect, item))

        back_rect = pygame.Rect(100, 540, 200, 45)
        draw_pixel_btn(screen, "BACK TO MENU", back_rect, (80, 80, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos): viewing = False
                for rect, item in buttons:
                    if rect.collidepoint(event.pos):
                        if item["unlocked"]: show_letter(item)
                        elif total_hearts >= item["price"]:
                            total_hearts -= item["price"]
                            item["unlocked"] = True
                            save_data(total_hearts, [it["id"] for it in GALLERY_ITEMS if it["unlocked"]])
        pygame.display.flip()

def show_letter(item):
    showing = True
    shared_msg = ""
    while showing:
        screen.fill((255, 240, 240))
        try:
            photo = pygame.image.load(item["img"]).convert_alpha()
            if item.get("rotate", False): photo = pygame.transform.rotate(photo, 90)
            w, h = photo.get_size()
            aspect = w / h
            new_w, new_h = 320, int(320 / aspect)
            if new_h > 240: new_h = 240; new_w = int(240 * aspect)
            photo = pygame.transform.smoothscale(photo, (new_w, new_h))
            
            rect = photo.get_rect(center=(SCREEN_WIDTH//2, 160))
            draw_pixel_box(screen, rect.inflate(20, 20), C_WHITE)
            screen.blit(photo, rect)
            y_offset = rect.bottom + 30
        except: y_offset = 100

        wrapped = wrap_text(item["msg"], font, SCREEN_WIDTH - 60)
        for line in wrapped:
            txt = font.render(line, True, C_BLACK)
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, y_offset)))
            y_offset += 22
        
        share_btn = pygame.Rect(125, 500, 150, 40)
        draw_pixel_btn(screen, "SHARE TO US", share_btn, (50, 100, 255))
        
        if shared_msg:
            msg_txt = small_font.render(shared_msg, True, C_GREEN)
            screen.blit(msg_txt, msg_txt.get_rect(center=(SCREEN_WIDTH//2, 480)))

        close_txt = small_font.render("[Click anywhere to Close]", True, (100, 100, 100))
        screen.blit(close_txt, (120, 560))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if share_btn.collidepoint(event.pos):
                    shared_msg = "Memory Saved to Hearts! ❤️"
                else:
                    showing = False
        pygame.display.flip()

# --- 9. Main Loop ---
def main():
    global total_hearts
    bird, pipes, score, state = Bird(), [Pipe(600)], 0, "MENU"
    while True:
        if state == "MENU":
            if BG_IMG: screen.blit(BG_IMG, (0, 0))
            else: screen.fill(C_BG_PINK)
            
            sub = font.render("From Pratik to Vanshika", True, C_BLACK)
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 50))

            t1 = title_font.render("Our Journey :", True, C_DEEP_RED)
            t2 = title_font.render("Love Letters", True, C_DEEP_RED)
            screen.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, 80))
            screen.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, 110))

            h_count = font.render(f"Hearts: {total_hearts} ❤️", True, C_DEEP_RED)
            screen.blit(h_count, (SCREEN_WIDTH//2 - h_count.get_width()//2, 150))
            
            all_unlocked = all(item["unlocked"] for item in GALLERY_ITEMS)
            if all_unlocked:
                love_msg = big_font.render("I LOVE YOU! ❤️", True, (255, 0, 0))
                bg_rect = love_msg.get_rect(center=(SCREEN_WIDTH//2, 185)).inflate(20, 10)
                pygame.draw.rect(screen, C_WHITE, bg_rect)
                pygame.draw.rect(screen, C_BLACK, bg_rect, 2)
                screen.blit(love_msg, love_msg.get_rect(center=(SCREEN_WIDTH//2, 185)))

            play_btn = pygame.Rect(80, 230, 240, 50)
            gal_btn = pygame.Rect(80, 300, 240, 50)
            about_btn = pygame.Rect(80, 370, 240, 50)
            
            draw_pixel_btn(screen, "START FLYING", play_btn, C_DEEP_RED)
            draw_pixel_btn(screen, "MEMORIES", gal_btn, C_BRIGHT_RED)
            draw_pixel_btn(screen, "ABOUT GAME", about_btn, (180, 60, 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.collidepoint(event.pos): 
                        state, bird, pipes, score = "PLAYING", Bird(), [Pipe(600)], 0
                    if gal_btn.collidepoint(event.pos): draw_gallery()
                    if about_btn.collidepoint(event.pos): show_about()
                        
        elif state == "PLAYING":
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: bird.flap()
                if event.type == pygame.MOUSEBUTTONDOWN: bird.flap()

            bird.update()
            
            # Use Processed BG for Gameplay
            if BG_PLAYING_IMG: screen.blit(BG_PLAYING_IMG, (0, 0))
            else: screen.fill(C_BG_PINK)

            for pipe in pipes:
                pipe.update()
                pipe.draw()
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    total_hearts += score
                    save_data(total_hearts, [it["id"] for it in GALLERY_ITEMS if it["unlocked"]])
                    state = "MENU"
                if not pipe.passed and pipe.x < bird.x: 
                    pipe.passed, score = True, score + 1
                    if score_snd: score_snd.play()

            if pipes[-1].x < SCREEN_WIDTH - 220: pipes.append(Pipe(SCREEN_WIDTH))
            if pipes[0].x < -70: pipes.pop(0)
            if bird.y <= 0 or bird.y >= SCREEN_HEIGHT:
                total_hearts += score
                save_data(total_hearts, [it["id"] for it in GALLERY_ITEMS if it["unlocked"]])
                state = "MENU"
            
            bird.draw()
            score_txt = big_font.render(str(score), True, C_WHITE)
            s_rect = score_txt.get_rect(center=(SCREEN_WIDTH//2, 50)).inflate(20, 10)
            draw_pixel_box(screen, s_rect, C_BLACK)
            screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH//2, 50)))
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()