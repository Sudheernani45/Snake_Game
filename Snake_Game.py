from tkinter import *
import random
import os

# Constants
GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
HIGH_SCORE_FILE = "highscore.txt"

# Game State
score = 0
direction = 'down'
difficulty_speed = {"Easy": 200, "Medium": 150, "Hard": 100}
SPEED = 150
restart_button = None
quit_button = None
snake = None
food = None

# Load High Score
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read())
    return 0

def save_high_score(new_score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(new_score))

high_score = load_high_score()

# Classes
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = [
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            for x, y in self.coordinates
        ]

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Game Logic
def next_turn(snake, food):
    global score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}  High Score: {high_score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global restart_button, quit_button, high_score

    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 - 50, font=('consolas', 70),
                       text="GAME OVER", fill="red")

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 10, font=('consolas', 30),
                       text=f"Final Score: {score}", fill="white")

    restart_button = Button(window, text="Restart", font=('consolas', 18),
                            command=restart_game, bg="green", fg="white", activebackground="darkgreen")
    restart_button.place(x=GAME_WIDTH//2 - 90, y=GAME_HEIGHT//2 + 60)

    quit_button = Button(window, text="Quit", font=('consolas', 18),
                         command=window.destroy, bg="red", fg="white", activebackground="darkred")
    quit_button.place(x=GAME_WIDTH//2 + 10, y=GAME_HEIGHT//2 + 60)

def restart_game():
    global score, direction, snake, food, restart_button, quit_button

    canvas.delete("all")
    if restart_button:
        restart_button.destroy()
    if quit_button:
        quit_button.destroy()

    score = 0
    direction = 'down'
    label.config(text=f"Score: {score}  High Score: {high_score}")

    snake = Snake()
    food = Food()
    next_turn(snake, food)

def choose_difficulty():
    def set_speed(level):
        global SPEED
        SPEED = difficulty_speed[level]
        diff_window.destroy()
        start_game()

    diff_window = Toplevel()
    diff_window.title("Select Difficulty")
    diff_window.geometry("300x250")
    Label(diff_window, text="Choose Difficulty", font=("consolas", 18)).pack(pady=15)

    Button(diff_window, text="Easy", font=("consolas", 14),
           command=lambda: set_speed("Easy"),
           bg="yellow", fg="black", activebackground="gold").pack(pady=10)

    Button(diff_window, text="Medium", font=("consolas", 14),
           command=lambda: set_speed("Medium"),
           bg="orange", fg="black", activebackground="darkorange").pack(pady=10)

    Button(diff_window, text="Hard", font=("consolas", 14),
           command=lambda: set_speed("Hard"),
           bg="red", fg="white", activebackground="darkred").pack(pady=10)

def start_game():
    global snake, food
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# Setup Window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}  High Score: {high_score}", font=('consolas', 30))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int(screen_width / 2 - GAME_WIDTH / 2)
y = int(screen_height / 2 - GAME_HEIGHT / 2)
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT+50}+{x}+{y}")

# Key bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start with difficulty dialog
choose_difficulty()

window.mainloop()

