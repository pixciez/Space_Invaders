import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Blue Play Button")

# Function to handle button click
def play_button_click():
    print("Play button clicked!")

# Create a button with the specified properties
play_button = tk.Button(
    root,
    text="Play",
    font=("Helvetica", 16),
    fg="white",
    bg="blue",
    command=play_button_click
)

# Pack the button into the window
play_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
