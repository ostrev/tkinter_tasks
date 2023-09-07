from tkinter import *
from tkinter import ttk, simpledialog
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter


class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1920x1080')
        self.root.title("Image Viewer")

        self.filters_mapping = {
            "BLUR": ImageFilter.BLUR,
            "CONTOUR": ImageFilter.CONTOUR,
            "EMBOSS": ImageFilter.EMBOSS,
            "SMOOTH": ImageFilter.SMOOTH_MORE,
        }

        self.frame_button = Frame(root)
        self.frame_button.pack(side=TOP, fill=X)

        self.load_button = ttk.Button(self.frame_button, text="Load Image", command=self.load_image)
        self.load_button.pack(side=LEFT)

        self.rotate_button = ttk.Button(self.frame_button, text="Rotate CCW", command=lambda: self.rotate_image('+'))
        self.rotate_button.pack(side=LEFT)

        self.rotate_button = ttk.Button(self.frame_button, text="Rotate CW", command=lambda: self.rotate_image('-'))
        self.rotate_button.pack(side=LEFT)

        self.blur_button = ttk.Button(self.frame_button, text="Blur", command=lambda: self.filters("BLUR"))
        self.blur_button.pack(side=LEFT)

        self.contour_button = ttk.Button(self.frame_button, text="Contour", command=lambda: self.filters("CONTOUR"))
        self.contour_button.pack(side=LEFT)

        self.emboss_button = ttk.Button(self.frame_button, text="Emboss", command=lambda: self.filters("EMBOSS"))
        self.emboss_button.pack(side=LEFT)

        self.smooth_button = ttk.Button(self.frame_button, text="Smooth", command=lambda: self.filters("SMOOTH"))
        self.smooth_button.pack(side=LEFT)

        self.flip_button = ttk.Button(self.frame_button, text="Flip", command=self.flip_image)
        self.flip_button.pack(side=LEFT)

        self.resize_button = ttk.Button(self.frame_button, text="Resize", command=self.prompt_for_resize)
        self.resize_button.pack(side=LEFT)

        self.reset_button = ttk.Button(self.frame_button, text="Reset", command=self.reset)
        self.reset_button.pack(side=LEFT)

        self.undo_button = ttk.Button(self.frame_button, text="Undo", command=self.undo)
        self.undo_button.pack(side=LEFT)

        self.save_button = ttk.Button(self.frame_button, text="Save", command=self.save_image)
        self.save_button.pack(side=LEFT)

        self.info_label = Label(root, text="Image Info:")
        self.info_label.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.image_history = []
        self.current_image_index = -1

        self.image = None
        self.photo = None
        self.displayed_image = None
        self.image_width = 0
        self.image_height = 0

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if file_path:
            self.display_image(file_path)
            self.display_image_info(file_path)

    def display_image(self, file_path):
        if self.current_image_index < len(self.image_history) - 1:
            self.image_history = self.image_history[:self.current_image_index + 1]

        self.image = Image.open(file_path)
        self.image.thumbnail((1000, 1000))

        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo

        self.displayed_image = self.image
        self.image_width, self.image_height = self.displayed_image.size

        self.image_history.append(self.displayed_image)
        self.current_image_index += 1

    def display_image_info(self, file_path):
        self.image = Image.open(file_path)
        info = (f"Name: {self.image.filename}\n"
                f"Size: {self.image.size}\n"
                f"Format: {self.image.format}\n"
                f"Mode: {self.image.mode}")
        self.info_label.config(text=info)

    def rotate_image(self, direction):
        if self.displayed_image:
            angle = f"{direction}90"
            self.displayed_image = self.displayed_image.rotate(int(angle), expand=True)
            self.photo = ImageTk.PhotoImage(self.displayed_image)
            self.image_label.config(image=self.photo)
            self.image_width, self.image_height = self.displayed_image.size

            self.image_label.config(width=self.image_width, height=self.image_height)

            self.image_history.append(self.displayed_image)
            self.current_image_index += 1

    def filters(self, filter_name):
        if self.displayed_image:
            image_filter = self.filters_mapping[filter_name]
            filtered_image = self.displayed_image.filter(image_filter)

            self.image_history.append(filtered_image)
            self.current_image_index += 1

            self.photo = ImageTk.PhotoImage(filtered_image)

            self.image_label.config(image=self.photo)

            self.image_width, self.image_height = filtered_image.size
            self.image_label.config(width=self.image_width, height=self.image_height)

    def reset(self):
        if self.image_history:
            self.displayed_image = self.image_history[0]
            self.photo = ImageTk.PhotoImage(self.displayed_image)
            self.image_label.config(image=self.photo)
            self.image_width, self.image_height = self.displayed_image.size
            self.image_label.config(width=self.image_width, height=self.image_height)
            self.current_image_index = 0

    def undo(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            previous_image = self.image_history[self.current_image_index]
            self.displayed_image = previous_image

            self.photo = ImageTk.PhotoImage(previous_image)
            self.image_label.config(image=self.photo)

            self.image_width, self.image_height = previous_image.size
            self.image_label.config(width=self.image_width, height=self.image_height)

    def flip_image(self):
        if self.displayed_image:
            self.displayed_image = self.displayed_image.transpose(Image.FLIP_LEFT_RIGHT)
            # for transpose(Image.FLIP_TOP_BOTTOM) can use rotate button and flip
            self.photo = ImageTk.PhotoImage(self.displayed_image)
            self.image_label.config(image=self.photo)
            self.image_width, self.image_height = self.displayed_image.size

            self.image_label.config(width=self.image_width, height=self.image_height)

            self.image_history.append(self.displayed_image)
            self.current_image_index += 1

    def resize_image(self, width, height):
        if self.displayed_image:
            self.displayed_image = self.displayed_image.resize((width, height))

            self.photo = ImageTk.PhotoImage(self.displayed_image)
            self.image_label.config(image=self.photo)
            self.image_width, self.image_height = self.displayed_image.size

            self.image_label.config(width=self.image_width, height=self.image_height)

            self.image_history.append(self.displayed_image)
            self.current_image_index += 1

    def prompt_for_resize(self):
        root = Tk()
        root.withdraw()
        width = simpledialog.askinteger("Resize Image", "Enter width:")
        height = simpledialog.askinteger("Resize Image", "Enter height:")

        if width is not None and height is not None:
            self.resize_image(width, height)
        else:
            return None

    def save_image(self):
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])

        if file_path:
            self.displayed_image.save(file_path)


if __name__ == "__main__":
    main_root = Tk()
    app = ImageViewerApp(main_root)
    main_root.mainloop()
