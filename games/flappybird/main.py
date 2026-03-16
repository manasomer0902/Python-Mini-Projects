
import pygame
import os
import random
import json

pygame.mixer.init()
pygame.font.init()

# Window dimensions
WIDTH, HEIGHT = 500, 800

# Load sounds
start_sound = pygame.mixer.Sound(os.path.join("assets", "start.wav"))   # Game start sound
jump_sound = pygame.mixer.Sound(os.path.join("assets", "jump.wav"))     # Bird jump sound
point_sound = pygame.mixer.Sound(os.path.join("assets", "point.wav"))   # Point sound
hit_sound = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))       # Collision sound
homepage_sound = pygame.mixer.Sound(os.path.join("assets", "homepage.wav"))  # Homepage sound
gameover_sound = pygame.mixer.Sound(os.path.join("assets", "game_over.wav"))  # Game over sound


# Load images
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))]
pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "base.png")))
retry_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "retry.png")))
background_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bg.png")))
homepage_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "homepage.png")),(WIDTH, HEIGHT))
game_over_image = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "gameover.png")))

# Fonts
stat_font = pygame.font.SysFont("comicsans", 30)
final_score_font = pygame.font.SysFont("comicsans", 70)
button_font = pygame.font.SysFont("comicsans", 40)
input_font = pygame.font.SysFont("comicsans", 30)

# Base class
class Base:
    VEL = 5
    WIDTH = base_image.get_width()
    img = base_image

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))

# Pipe class
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, 400)
        self.top = self.height - pipe_image.get_height()
        self.bottom = self.height + self.GAP
        self.pipe_top = pygame.transform.flip(pipe_image, False, True)
        self.pipe_bottom = pipe_image
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def off_screen(self):
        return self.x + pipe_image.get_width() < 0

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top - bird.y)
        bottom_offset = (self.x - bird.x, self.bottom - bird.y)
        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            hit_sound.play()  # Play hit sound
        return t_point or b_point

# Bird class
class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = bird_images[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        jump_sound.play()  # Play jump sound

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = bird_images[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = bird_images[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = bird_images[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = bird_images[1]
        elif self.img_count >= self.ANIMATION_TIME * 4 + 1:
            self.img = bird_images[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = bird_images[1]
            self.img_count = self.ANIMATION_TIME

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
# High Score Functions
def get_high_score_list():
    """Get all high scores from the high_scores.json file."""
    if not os.path.exists("high_scores.json"):
        # If the file doesn't exist, create it with an empty list
        with open("high_scores.json", "w") as file:
            json.dump([], file)
        return []  # Return an empty list if no file exists
    
    # If the file exists, read it and return the high scores
    with open("high_scores.json", "r") as file:
        high_scores = json.load(file)
    
    return sorted(high_scores, key=lambda x: x["score"], reverse=True)  # Sort by score in descending order

def get_high_score():
    """Get the highest score from the high_scores.json file."""
    high_scores = get_high_score_list()
    return high_scores[0]["score"] if high_scores else 0


def set_high_score(player_name, score):
    try:
        with open("high_scores.json", "r") as file:
            high_scores = json.load(file)  # Load the list of high scores
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = []  # Create an empty list if file doesn't exist or is empty    

    # Check if player already has a score in the high scores
    player_found = False
    for entry in high_scores:
        if entry["name"] == player_name:
            entry["score"] = score # Update the score if new score is higher
            player_found = True
            break
        
    # If player isn't in the high scores, add their score to the list
    if not player_found:
        high_scores.append({"name": player_name, "score": score})

    with open("high_scores.json", "w") as file:
        json.dump(high_scores, file, indent=4)  # Save updated high scores list


# Function to display player name input
def get_player_name(window):
    pygame.font.init()
    name = ""
    input_active = True

    while input_active:
        window.fill((255, 255, 255))  # White background
        text = input_font.render("Enter Your Name:", 1, (0, 0, 0))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))

        name_text = input_font.render(name, 1, (0, 0, 255))  # Blue text for name
        window.blit(name_text, (WIDTH//2 - name_text.get_width()//2, HEIGHT//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():  # If Enter is pressed and name is not empty
                    return name
                elif event.key == pygame.K_BACKSPACE:  # Backspace to delete character
                    name = name[:-1]
                else:
                    if len(name) < 12:  # Limit name length to 12 characters
                        name += event.unicode  # Add character to name

 
# Drawing the window
def draw_window(window, bird, pipes, base, score, player_name):
    window.blit(background_image, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    # Score color black
    text = stat_font.render(f"Score: {score}", 1, (0, 0, 0))
    window.blit(text, (WIDTH - 10 - text.get_width(), 10))

     # High Score Display
    high_score = get_high_score()
    high_score_text = stat_font.render(f"High Score: {high_score}", 1, (0, 0, 0))
    window.blit(high_score_text, (10, 10))  # Show at the top-left corner

    # Player Name Display
    name_text = stat_font.render(f"{player_name}", 1, (0, 0, 255))
    window.blit(name_text, (WIDTH // 2 - name_text.get_width() // 5, 10))


    base.draw(window)
    bird.draw(window)
    pygame.display.update()

# Game over function
def game_over(window, score, player_name):
    gameover_sound.play()  # Play game over sound
    """ Clear screen properly and show game over with retry button """
    window.fill((255, 255, 255))  # Clear screen
    window.blit(background_image, (0, 0))

    # Display game over image
    window.blit(game_over_image, (WIDTH // 2 - game_over_image.get_width() // 2, HEIGHT // 4))

    # Final score
    text = final_score_font.render(f"Final Score: {score}", 1, (0, 0, 0))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 200))

    # Display high score
    high_score = get_high_score() # Get the high score 
    high_score_text = final_score_font.render(f"High Score: {high_score}", 1, (0, 0, 0))
    window.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - 120))


    # Retry Image Button
    retry_rect = retry_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))  # Centered
    window.blit(retry_image, retry_rect.topleft)

    pygame.display.update()

    # Wait for retry button click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                return  # Retry the game
            

 # Homepage function
def homepage():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird by Manas")
    
    pygame.mixer.music.load(os.path.join("assets", "homepage.wav"))  # Replace with actual file
    pygame.mixer.music.play(-1)  # Loop homepage music

    player_name = ""  # Initialize player name
    input_active = True  # Flag to check if input is active.

    while input_active:
        window.blit(homepage_image, (0, 0))
        
        # Draw Play Button
        play_text = button_font.render("Play", 1, (255, 255, 255))
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        pygame.draw.rect(window, (0, 0, 0), play_rect.inflate(20, 10))
        window.blit(play_text, play_rect.topleft)
        
        # Draw Score Button
        score_text = button_font.render("High Score", 1, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
        pygame.draw.rect(window, (0, 0, 0), score_rect.inflate(20, 10))
        window.blit(score_text, score_rect.topleft)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    player_name = get_player_name(window)  # Get player name
                    pygame.mixer.music.stop()  # Stop homepage music
                    main(player_name)
                    return  # Start the game
                
                if score_rect.collidepoint(event.pos):
                    display_high_scores(window)

def display_high_scores(window):
    """Function to display high scores in a new screen."""
    window.fill((255, 255, 255))  # Clear the screen

    # Title of the high scores page
    title_text = final_score_font.render("High Scores", 1, (0, 0, 0))
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Load high scores from the JSON file
    high_scores = get_high_score_list()

    # Display high scores
    y_offset = 150  # Starting Y position for the scores
    for index, entry in enumerate(high_scores[:5]):  # Show top 5 high scores
        name_text = stat_font.render(f"{index + 1}. {entry['name']} - {entry['score']}", 1, (0, 0, 0))
        window.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, y_offset))
        y_offset += 40  # Move down for the next score

    pygame.display.update()

    # Wait for user to click to return to the homepage
    waiting_for_return = True
    while waiting_for_return:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_return = False  # Exit this loop and return to homepage
                homepage()

def main(player_name):
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird by Manas")

    start_sound.play()  # Play start sound

    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    score = 0
    high_score = get_high_score()  # Get the high score

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        bird.move()
        base.move()

        if pipes[-1].x < 300:
            pipes.append(Pipe(700))

        for pipe in pipes:
            pipe.move()
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1  
                point_sound.play()

            if pipe.collide(bird) or bird.y + bird.img.get_height() >= HEIGHT:
                game_over(window, score, player_name)

                # High Score Check & Update
                if score > high_score:
                    set_high_score(player_name, score)  # Save new high score
                    high_score = get_high_score()  # Update high score


                # Stop the gameover sound when retrying
                gameover_sound.stop()
                homepage()  # Show homepage again
                main(player_name)

        pipes = [p for p in pipes if not p.off_screen()]
        draw_window(window, bird, pipes, base, score, player_name)

if __name__ == "__main__":
    homepage()  # Show homepage first
    main("")       # Start the game
