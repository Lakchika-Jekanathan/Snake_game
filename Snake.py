import tkinter
import random

# Constants
rows = 25
cols = 25
tile_size = 25

window_width = tile_size * rows
window_height = tile_size * cols

# Tile class for Snake and Food
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Initialize window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=window_width, height=window_height)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Snake starting position and food
snake = [Tile(5 * tile_size, 5 * tile_size)]  # A list to represent the snake's body
food = Tile(random.randint(0, cols - 1) * tile_size, random.randint(0, rows - 1) * tile_size)
velocityX = 0
velocityY = 0
snake_length = 1
score = 0

# Direction control
def change_direction(e):
    global velocityX, velocityY

    if e.keysym == "Up" and velocityY == 0:
        velocityX, velocityY = 0, -tile_size
    elif e.keysym == "Down" and velocityY == 0:
        velocityX, velocityY = 0, tile_size
    elif e.keysym == "Left" and velocityX == 0:
        velocityX, velocityY = -tile_size, 0
    elif e.keysym == "Right" and velocityX == 0:
        velocityX, velocityY = tile_size, 0

# Game Over when snake hits the wall or itself
def check_collision():
    head = snake[0]
    # Wall collision
    if head.x < 0 or head.x >= window_width or head.y < 0 or head.y >= window_height:
        return True
    # Self collision
    for segment in snake[1:]:
        if head.x == segment.x and head.y == segment.y:
            return True
    return False

# Check if snake eats food
def check_food():
    global snake_length, food, score
    head = snake[0]
    if head.x == food.x and head.y == food.y:
        snake_length += 1  # Increase snake length
        score += 50  # Increase score by 50 points
        # Spawn new food at a random location
        food = Tile(random.randint(0, cols - 1) * tile_size, random.randint(0, rows - 1) * tile_size)

# Draw everything on the canvas
def draw():
    global snake

    if check_collision():
        canvas.create_text(window_width // 2, window_height // 2, fill="white", font="Arial 20 bold", text="Game Over")
        canvas.create_text(window_width // 2, window_height // 2 + 30, fill="white", font="Arial 15 bold", text=f"Score: {score}")
        return

    # Move the snake by inserting new head and removing the tail
    head = Tile(snake[0].x + velocityX, snake[0].y + velocityY)
    snake = [head] + snake[:snake_length - 1]  # Add new head, and keep the body according to snake_length

    check_food()

    # Clear canvas
    canvas.delete("all")

    # Draw snake
    for segment in snake:
        canvas.create_rectangle(segment.x, segment.y, segment.x + tile_size, segment.y + tile_size, fill="green")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + tile_size, food.y + tile_size, fill="cyan")

    # Display score
    canvas.create_text(50, 10, fill="white", font="Arial 10 bold", text=f"Score: {score}")

    window.after(100, draw)

# Start drawing
draw()

# Bind key events to change direction
window.bind("<KeyPress>", change_direction)
window.mainloop()
