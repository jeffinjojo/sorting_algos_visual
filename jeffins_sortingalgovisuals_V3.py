#jeffins_sortingalgovisuals_V3.py Date (V3) last Updated: 06/02/2024
#Creating a sorting algorithm visualiser revision tool to further understaning of different sorting types and help remember definitions for test.
#Designed by Jeffin, with help of Dominic, Ali, Usayd and teaching/online resources.
import pygame
import random
import math
import textwrap

# Initialise Pygame
pygame.init()

# Class to handle all the drawing-related information and configuration
class DrawInformation:
    # Choosing colour scheme for interface
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)  # Blue for main bars
    ORANGE = (255, 165, 0)  # Orange for highlights
    BACKGROUND_COLOR = (230, 230, 250)  # Lavender for the background
    
    #Diff colour gradients for data bars to make the sorting clear
    GRADIENTS = [
        (128, 128, 128),  # Dark grey
        (160, 160, 160),  # Medium grey
        (192, 192, 192)   # Light grey
    ]

    FONT = pygame.font.SysFont('gillsans', 24)  # Font used in buttons and controls
    LARGE_FONT = pygame.font.SysFont('gillsans', 36)  # Larger font for titles
    BUTTON_FONT = pygame.font.SysFont('gillsans', 28)  # Font for the buttons

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Create the Pygame window with the given width and height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm VisualiSer")  # Window title

        # Set up the list and its properties
        self.set_list(lst)

    # Set up the list properties (dimensions and block size)
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # Calculate the block width based on the window size and list length
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        # Starting X position for the first bar
        self.start_x = self.SIDE_PAD // 2

# Function to draw the main UI
def draw(draw_info, algo_name, ascending, sorting):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Render the title with the algorithm name and sorting direction
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    # Render controls at the top
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | S - Stop Sorting | A - Ascend | D - Descend", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 50))

    # Draw algorithm buttons at the top
    draw_buttons(draw_info)

    draw_list(draw_info)
    pygame.display.update()

# Function to draw interactive buttons at the top
def draw_buttons(draw_info):
    # Button positions
    button_names = ["B - Bubble Sort", "I - Insertion Sort", "M - Merge Sort"]
    buttons = []
    button_width = 200
    button_height = 50
    gap = 20
    start_x = (draw_info.width - (button_width * len(button_names) + gap * (len(button_names) - 1))) // 2
    y = 100

    for i, name in enumerate(button_names):
        x = start_x + (button_width + gap) * i
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(draw_info.window, draw_info.BLACK, button_rect)
        text = draw_info.BUTTON_FONT.render(name, 1, draw_info.WHITE)
        draw_info.window.blit(text, (x + (button_width - text.get_width()) / 2, y + (button_height - text.get_height()) / 2))
        buttons.append((button_rect, name))

    return buttons

# Function to show a pop-up message with the definition of the sorting algorithm
def show_popup(draw_info, algo_name):
    definitions = {
        "B - Bubble Sort": "Bubble Sort repeatedly compares adjacent elements and swaps them if they're in the wrong order.",
        "I - Insertion Sort": "Insertion Sort builds the sorted list one item at a time, inserting each element into its correct position.",
        "M - Merge Sort": "Merge Sort divides the list into halves, sorts them, and then merges them back together."
    }
    definition = definitions.get(algo_name, "Definition not available")

    # Pop-up box dimensions
    popup_width = 650
    popup_height = 200
    popup_rect = pygame.Rect(draw_info.width // 2 - popup_width // 2, draw_info.height // 2 - popup_height // 2, popup_width, popup_height)

    # Draw the pop-up box
    pygame.draw.rect(draw_info.window, draw_info.BLACK, popup_rect)
    pygame.draw.rect(draw_info.window, draw_info.WHITE, popup_rect.inflate(-10, -10))  # Inner white box

    # Render the definition text inside the box
    text = draw_info.BUTTON_FONT.render(algo_name, 1, draw_info.BLACK)
    draw_info.window.blit(text, (popup_rect.centerx - text.get_width() // 2, popup_rect.y + 20))

    # Wrap the definition text to fit in the box
    wrapped_text = textwrap.wrap(definition, width=50)
    for i, line in enumerate(wrapped_text):
        definition_text = draw_info.FONT.render(line, 1, draw_info.BLACK)
        draw_info.window.blit(definition_text, (popup_rect.centerx - definition_text.get_width() // 2, popup_rect.y + 80 + i * 30))

    pygame.display.update()

# Function to draw the list of values as bars
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

# Generating a random list of values to be sorted
def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]

# Bubble Sort algorithm (visualised)
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.BLUE, j + 1: draw_info.ORANGE}, True)
                pygame.time.delay(100)
                yield True

    return lst

# Insertion Sort algorithm (visualised)
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.BLUE, i: draw_info.ORANGE}, True)
            pygame.time.delay(100)
            yield True

    return lst

# Merge Sort algorithm (visualised)
def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    return merge_sort_helper(lst, 0, len(lst) - 1, draw_info, ascending)

def merge_sort_helper(lst, left, right, draw_info, ascending):
    if left >= right:
        return

    mid = (left + right) // 2
    yield from merge_sort_helper(lst, left, mid, draw_info, ascending)
    yield from merge_sort_helper(lst, mid + 1, right, draw_info, ascending)
    yield from merge(lst, left, mid, right, draw_info, ascending)

def merge(lst, left, mid, right, draw_info, ascending):
    left_half = lst[left:mid + 1]
    right_half = lst[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half):
        if (left_half[i] <= right_half[j] and ascending) or (left_half[i] >= right_half[j] and not ascending):
            lst[k] = left_half[i]
            i += 1
        else:
            lst[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        lst[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        lst[k] = right_half[j]
        j += 1
        k += 1

    draw_list(draw_info, {i: draw_info.ORANGE for i in range(left, right + 1)}, True)
    pygame.time.delay(100)
    yield True

# Main function to run the visualiser
def main():
    run = True
    clock = pygame.time.Clock()

    n = 50  # Number of elements in the list
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1280, 960, lst)  # Adjust window size
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    buttons = None

    while run:
        clock.tick(60)
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, sorting)
            buttons = draw_buttons(draw_info)

        # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button_rect, name in buttons:
                    if button_rect.collidepoint(pos):
                        show_popup(draw_info, name)
                        pygame.time.wait(5000)  # Shows the pop-up for 5 seconds

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                elif event.key == pygame.K_s and sorting:
                    sorting = False  # Stop sorting
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"
                elif event.key == pygame.K_m and not sorting:
                    sorting_algorithm = merge_sort
                    sorting_algo_name = "Merge Sort"

    pygame.quit()

if __name__ == "__main__":
    main()

#REFERENCES
#https://blackboard.le.ac.uk/ultra/courses/_62373_1/outline/edit/document/_4800147_1?courseId=_62373_1&view=content : UOL Lecture on Sorting Algos
#https://www.youtube.com/watch?v=AY9MnQ4x3zk : Introduction to Pygame module and its features
#https://www.youtube.com/watch?v=twRidO-_vqQ : Tutorial for DSA visualiser in python 