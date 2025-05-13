
import tkinter as tk
from tkinter import font

root = tk.Tk()

# Load the custom font
custom_font = font.Font(family='Press Start 2P', size=12)

label = tk.Label(root, text="Hello, World!", font=custom_font)
label.pack()

root.mainloop()


'''
import pygame
pygame.init()

# Load the custom font
font_path = 'fonts/PressStart2P-Regular.ttf'  # Ensure this path is correct
custom_font = pygame.font.Font(font_path, 24)

screen = pygame.display.set_mode((800, 600))
text_surface = custom_font.render('Hello, World!', True, (255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(text_surface, (100, 100))
    pygame.display.flip()

pygame.quit()

'''
