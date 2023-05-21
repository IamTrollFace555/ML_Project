import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageDraw

from preprocess import preprocess_image
from predict import setup, make_prediction

WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class WhiteBoard:

    def __init__(self, master):
        self.old_y = None
        self.old_x = None
        self.master = master
        self.master.title("WhiteBoard")
        self.master.resizable(False, False)

        # Set ttkbootstrap Style
        self.style = Style(theme="pulse")

        # Create canvas
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.configure(bg="black")
        self.canvas.pack()

        # Create PIL canvas to use in parallel
        self.img_pil = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
        self.cv_pil = ImageDraw.Draw(self.img_pil)

        # Create Buttons
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(side="top", pady=10)

        self.predictions_box = tk.Label()

        # # Button configuration
        # button_config = {
        #     "black": ("dark.TButton", lambda: self.change_color("black")),
        #     "red": ("danger.TButton", lambda: self.change_color("red")),
        #     "blue": ("info.TButton", lambda: self.change_color("blue")),
        #     "green": ("success.TButton", lambda: self.change_color("green")),
        #     "clear": ("light.TButton", self.clear_canvas)
        # }

        # Button configuration
        button_config = {
            "clear": ("light.TButton", self.clear_canvas),
            "save": ("light.TButton", self.save_image),
            "predict": ("light.TButton", self.predict)
        }

        # Add buttons to the button frame
        for color, (style, command) in button_config.items():
            ttk.Button(self.button_frame, text=color.capitalize(),
                       command=command, style=style).pack(side="left", padx=5, pady=5)

        # Initialize drawing variables
        self.draw_color = "white"
        self.line_width = 35
        self.old_x, self.old_y = None, None

        # Add event listeners
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)

    # Save starting point of line
    def start_line(self, event):
        self.old_x, self.old_y = event.x, event.y

    # Draw line from starting point to current point and then update starting point
    def draw_line(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=self.draw_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)

            self.cv_pil.line((self.old_x, self.old_y, event.x, event.y),
                             fill=self.draw_color, width=self.line_width)
            self.old_x, self.old_y = event.x, event.y

    # Update current drawing color
    def change_color(self, new_color):
        self.draw_color = new_color

    # Delete all objects on canvas
    def clear_canvas(self):
        self.canvas.delete("all")
        self.img_pil = Image.new("RGB", (WIDTH, HEIGHT), BLACK)
        self.cv_pil = ImageDraw.Draw(self.img_pil)

    def save_image(self):
        filename = "user_image.jpg"
        self.img_pil.save(filename)

    def predict(self):

        pred_dict = {0: "Clock",
                     1: "Boomerang",
                     2: "Airplane",
                     3: "Snail",
                     4: "Parachute",
                     5: "Tree",
                     6: "Fish",
                     7: "Diamond",
                     8: "Helicopter",
                     9: "T-Shirt"}

        np_img = preprocess_image()
        np_img = np_img.reshape(784)
        prediction, probabilities = make_prediction(np_img, convolutional=True)

        print("Prediction: ", pred_dict[prediction.item()])
        print("Probabilities: ", probabilities)


if __name__ == "__main__":
    setup(convolutional=True)
    root = tk.Tk()
    whiteboard = WhiteBoard(root)
    root.mainloop()
