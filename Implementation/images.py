import tkinter as tk
from PIL import Image, ImageTk

class ImageDisplayApp:
    def __init__(self, master, image_paths):
        self.master = master
        self.master.title("Image Overlay App")

        # Load images
        self.images = [Image.open(path) for path in image_paths]

        # Resize images to the same dimensions
        width, height = 300, 300
        self.images = [img.resize((width, height), Image.LANCZOS) for img in self.images]

        # Create an empty image with an alpha channel
        self.result_image = Image.new('RGBA', (width * 2, height * 2), (0, 0, 0, 0))

        # Paste images onto the result image, considering alpha channel
        positions = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for img, pos in zip(self.images, positions):
            self.result_image.paste(img, pos, img)

        # Convert the result to Tkinter PhotoImage
        self.tk_image = ImageTk.PhotoImage(self.result_image)

        # Create label to display the overlaid image
        self.label = tk.Label(master, image=self.tk_image)
        self.label.grid(row=0, column=0, padx=5, pady=5)

    def run(self):
        self.master.mainloop()

# Replace the paths with your actual image paths
image_paths = ['0.png', '1.png', '2.png', '3.png']
# Create Tkinter root window
root = tk.Tk()
app = ImageDisplayApp(root, image_paths)
app.run()