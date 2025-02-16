# Author: Thomas Preston

import tkinter as tk
from PIL import ImageTk, Image
from os import path
import logging
from socket import gethostname, gethostbyname

class Window():
    def __init__(self):
        self.window_width = 800
        self.window_height = 500
        self.window_x = 200
        self.window_y = 100

        self.background_colour = "#303030"

        scriptDir = path.dirname(path.abspath(__file__))
        logging.basicConfig(filename=f"{scriptDir}\\..\\logs\\client-{gethostname()}.log", 
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('client:window')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Init ran sucessfully")
        self.logger.debug(f"This client is {gethostname()} [{gethostbyname(gethostname())}]")

        self.discard = "Club2"
        self.hand = ["Club3", "Club4", "Club5", "Club6", "Club7", "Club8", "Club9"]
        

    def createWindow(self):
        self.window = tk.Tk()
        self.window.geometry("{0}x{1}+{2}+{3}".format(self.window_width, self.window_height, self.window_x, self.window_y))
        self.window.title("Higher Or Lower")
        self.window.resizable(True, True)
        self.window.configure(bg = self.background_colour)
        self.logger.info("Window Created")

    def draw(self):
        # Configure the rows: make the top row twice the height of the others
        self.window.grid_rowconfigure(0, weight=2)  # Row 0 (top row) will be taller
        self.window.grid_rowconfigure(1, weight=1)  # Row 1 (middle row)
        self.window.grid_rowconfigure(2, weight=1)  # Row 2 (bottom row)

        # Create a 4x3 grid of labels (buttons or other widgets can also be used)
        # for row in range(3):
        #     for col in range(4):
        #         label = tk.Label(self.window, text=f"R{row}C{col}", relief="solid", width=10, height=3)
        #         label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for col in range(4):
            self.window.grid_columnconfigure(col, weight=1)

        self.logger.info("Rows Setup")

        try: 
            scriptDir = path.dirname(path.abspath(__file__))
            unturned = tk.PhotoImage(file=f"{scriptDir}\\..\\assets\\Deck\\Back.png")
            discard = tk.PhotoImage(file=f"{scriptDir}\\..\\assets\\Deck\\{self.discard}.png")
            handImages = []
            for card in self.hand:
                handImages.append(self.crop_image(f"{scriptDir}\\..\\assets\\Deck\\{card}.png"))
        except Exception as e:
            print(e)

        buttonU = tk.Button(self.window, image=unturned, 
                           command = lambda x = "Clicked": print(x), 
                           bg = self.background_colour,
                           fg = self.background_colour,
                           activebackground = self.background_colour,
                           activeforeground = self.background_colour,
                           highlightbackground = self.background_colour,
                           highlightcolor = self.background_colour,
                           highlightthickness = 0,
                           relief = "flat", 
                           bd = 0)
        buttonU.grid(row = 0, column = 1)
        buttonU.image=unturned

        buttonD = tk.Button(self.window, image=discard, 
                           command = lambda x = "Clicked": print(x), 
                           bg = self.background_colour,
                           fg = self.background_colour,
                           activebackground = self.background_colour,
                           activeforeground = self.background_colour,
                           highlightbackground = self.background_colour,
                           highlightcolor = self.background_colour,
                           highlightthickness = 0,
                           relief = "flat", 
                           bd = 0)
        buttonD.grid(row = 0, column = 2)
        buttonD.image=discard

        handButtons = []
        row=1
        column=0
        for image in handImages:
            buttonH = tk.Button(self.window, image=image, 
                           command = lambda x = "Clicked": print(x), 
                           bg = self.background_colour,
                           fg = self.background_colour,
                           activebackground = self.background_colour,
                           activeforeground = self.background_colour,
                           highlightbackground = self.background_colour,
                           highlightcolor = self.background_colour,
                           highlightthickness = 0,
                           relief = "flat", 
                           bd = 0)
            buttonH.grid(row = row, column = column)
            buttonH.image=image

            handButtons.append(buttonH)

            column += 1
            if column > 3:
                column = 0
                row += 1
            
    def crop_image(self, image_path, crop_fraction=0.5):
        # Open the image using Pillow
        image = Image.open(image_path)
        
        # Get the dimensions of the image
        width, height = image.size
        
        # Calculate the height of the top 10% of the image
        top_height = int(height * crop_fraction)
        
        # Crop the image (left, upper, right, lower)
        cropped_image = image.crop((0, 0, width, top_height))
        
        # Convert the image to a Tkinter-compatible format
        return ImageTk.PhotoImage(cropped_image)

if __name__ == "__main__":
    win = Window()
    win.createWindow()
    win.draw()
    win.window.mainloop()