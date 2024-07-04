import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import csv
import os
import sys
import glob
import time
import random

INDEX_DIR_PATH = './index_file'
DATA_DIR_PATH = './stylizations'
OUPUT_DIR_PATH = './output'

class ImageRaterApp:
    def __init__(self, root, **kwargs):
        self.root = root
        if 'mode' in kwargs.keys():
            self.mode = kwargs['mode'].split('=')[1]
        else:
            self.mode = 'prod'
        self.root.title("Image Rater")
        self.root.bind("<Destroy>", self.on_destroy)
        self.ouput_file = None
        self.image_list = []
        self.image_index = 0
        self.ratings = []
        self.root.bind('<Key>', self.key_press)
        self.root.geometry("1920x1080")
        
        self.root.attributes('-fullscreen', True)
        # self.root.bind('<Configure>', self.resize_image)
        self.space_under_image = 60
        self.root.update()
        self.check_output_directory()
        self.load_index_files()
        # Set up GUI elements
        self.setup_gui()
        # Load images
        self.load_index()
        # self.load_output()
        self.load_index_pointer()
        self.display_image()
    def check_output_directory(self):
        if not os.path.exists(OUPUT_DIR_PATH):
            os.makedirs(OUPUT_DIR_PATH)
    def load_index_files(self):
        """
        Load from index files directory file paths
        """

        if not os.path.exists(INDEX_DIR_PATH):
            os.makedirs(INDEX_DIR_PATH)
        self.index_file_paths = glob.glob(INDEX_DIR_PATH + '/*')

    def load_data_files(self):
        """
        Load from data path directory file paths
        """

        if not os.path.exists(DATA_DIR_PATH):
            os.makedirs(DATA_DIR_PATH)
        self.data_file_paths = glob.glob(DATA_DIR_PATH + '/**/*.jpg', recursive=True)

    def select_item(self):
        """
        Special button method for selecting index file if there are several
        index files in index files directory.
        """

        selected = self.listbox.curselection()
        if selected:
            self.selected_index = selected[0] #Not good deision
            print(f"Selected index file: {self.selected_index}")
            self.selector_window.destroy()
        else:
            print("No file selected")

    def load_index_from_file(self, index_file_path):
        """
        Load data files path from index file.
        """

        with open(index_file_path, 'r') as f:
            data = f.read() 
            lines = data.split("\n") 
            self.ouput_filename = lines[0]
            self.indecies = lines[1:-1]

    def shuffle_data_files(self):
        """
        Shuffles data files path for creating index file.
        """
        #TODO Should be carefully debugged
        content_indecies = []
        content_dict = {}
        for i, path in enumerate(self.data_file_paths):
            file_name = os.path.basename(path)
            splitted_ = file_name.split('_')
            content_id = splitted_[1]
            style_id = file_name.split('style_')[1].split('_')[0]
            size = splitted_[-1]
            if content_id not in content_dict.keys():
                content_indecies.append(content_id)
                content_dict[content_id] = []
            content_dict[content_id].append({'style_id': style_id, 'size': size, 'index': i}) #NOTE could be optimized
        random.shuffle(content_indecies)
        self.shuffled_data_file_paths = []
        for content_id in content_indecies:
            content_list = content_dict[content_id]
            random.shuffle(content_list)
            for content_image in content_list:
                self.shuffled_data_file_paths.append(self.data_file_paths[content_image['index']])
    def create_index_file(self):
        """
        Creates new index file from all files in data directory
        """

        self.load_data_files()
        self.shuffle_data_files()
        index_file_path = os.path.join(INDEX_DIR_PATH, f'index_file_{time.strftime("%Y%m%d-%H%M%S")}.txt')
        ouput_file_path = os.path.join(OUPUT_DIR_PATH, f'output_file_{time.strftime("%Y%m%d-%H%M%S")}.csv')
        with open(ouput_file_path, "w+") as cs:
            pass 
        with open(index_file_path, 'w+') as f:
            f.write(f"{ouput_file_path}\n")
            for file_path in self.shuffled_data_file_paths:
                # print(file_path)
                f.write(f"{file_path}\n")
        
        return index_file_path

    def load_index(self):
        """
        Load index from index files paths, choosing depending on content in index directory
        """

        if len(self.index_file_paths) > 1: 
            self.selector_window = tk.Toplevel(self.root)
            self.selector_window.title("Index file selection")
            
            self.label = tk.Label(self.selector_window, text="Select an index file from the list:")
            self.label.pack(pady=10)
            
            self.listbox = tk.Listbox(self.selector_window)
            self.listbox.pack(pady=10)
            
            for item in self.index_file_paths:
                self.listbox.insert(tk.END, item)
            
            self.select_button = tk.Button(self.selector_window, text="Select", command=self.select_item)
            self.select_button.pack(pady=10)
            self.load_index_from_file(self.index_file_paths[self.selected_index])

        elif len(self.index_file_paths) == 0:
            self.index_file_paths.append(self.create_index_file())
            self.load_index_from_file(self.index_file_paths[0])
        else:
            self.load_index_from_file(self.index_file_paths[0])

    # def load_output(self):
    #     """
    #     Loads output file data
    #     """
        # self.output_file =  open(self.ouput_filename, mode='a', newline='')
        # self.output_writer = csv.writer(self.output_file)

    def load_index_pointer(self):
        """
        Loads pointer in index
        """
        self.index_pointer = 0
        with open(self.ouput_filename, 'r+') as f:
            for row in csv.reader(f):
                self.index_pointer += 1

    def setup_gui(self):
        self.close_button = tk.Button(self.root, text="Close", command=self.root.destroy)
        self.close_button.place(relx=1.0, x=-10, y=10, anchor='ne')

        self.counter_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.counter_label.pack(anchor=tk.NW, padx=10, pady=10)
        
        # self.rating_label = tk.Label(self.root, text="", font=("Helvetica", 55), fg="red")
        # self.rating_label.pack(expand = True)

        self.image_label = tk.Label(self.root, text="", font=("Helvetica", 150), fg="red", compound='center')
        self.image_label.pack()
        
        
        
        # self.canvas = tk.Canvas(root)
        # self.canvas.pack(pady=20)

        # self.rating_text = self.canvas.create_text(
        #     200, 200, text="", font=("Helvetica", 55), fill="red"
        # )
        # self.buttons = []
        # for i in range(10):
        #     button = tk.Button(self.buttons_frame, text=str(i), command=lambda i=i: self.submit_rating(i),
        #                        width=5, height=2, font=("Helvetica", 14))
        #     button.grid(row=0, column=i, padx=5, pady=5)
        #     self.buttons.append(button)


    def display_image(self):
        # print(self.index_pointer, self.indecies)
        if self.index_pointer < len(self.indecies):
            image_path = self.indecies[self.index_pointer]
            img = Image.open(image_path)
            window_height, window_width = self.root.winfo_height()- self.space_under_image, self.root.winfo_width()
            # print(window_height, window_width)
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height

            if window_width / window_height > aspect_ratio:
                new_height = window_height
                new_width = int(window_height * aspect_ratio)
            else:
                new_width = window_width
                new_height = int(window_width / aspect_ratio)

            img = img.resize((new_width,new_height), Image.LANCZOS)
            # Display the image on the canvas
            img_tk = ImageTk.PhotoImage(img)
            # self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=img_tk)
            self.image_label.config(image=img_tk)
            self.image_label.config(text='')
            self.image_label.image = img_tk
            self.update_counter()
        else:
            messagebox.showinfo("Done", "You have rated all images.")
            self.root.quit()

    # def resize_image(self, img):
    #     image_path = self.indecies[self.index_pointer]
    #     img = Image.open(image_path)
    #     window_width = event.width
    #     window_height = event.height - self.space_under_image
    #     original_width, original_height = img.size
    #     aspect_ratio = original_width / original_height

    #     if window_width / window_height > aspect_ratio:
    #         new_height = window_height
    #         new_width = int(window_height * aspect_ratio)
    #     else:
    #         new_width = window_width
    #         new_height = int(window_width / aspect_ratio)
    #     print(new_width, new_height)
    #     resized_image = img.resize((new_width, new_height), Image.LANCZOS)
    #     img_tk = ImageTk.PhotoImage(resized_image)
    #     self.canvas.itemconfig(self.image_id, image=img_tk)
    #     self.canvas.coords(self.image_id, (window_width - new_width) // 2, (window_height - new_height) // 2)


    

    def submit_rating(self, rating):
        with open(self.ouput_filename, mode='a', newline='') as output_file:
            self.output_writer = csv.writer(output_file)
            self.output_writer.writerow([os.path.basename(self.indecies[self.index_pointer]), rating if rating != 0 else 10])

        self.index_pointer += 1
        self.display_rating_message(rating)
        self.root.after(800, self.display_image)

    def display_rating_message(self, rating):
        self.image_label.config(text=str(rating if rating != 0 else 10 ))

    def update_counter(self):
        self.counter_label.config(text=f"Image {self.index_pointer + 1} of {len(self.indecies)}", font=("Helvetica", 20))

    def key_press(self, event):
        if event.char.isdigit():
            rating = int(event.char)
            if 0 <= rating <= 9:
                self.submit_rating(rating)

    def on_destroy(self, event):
        if event.widget.winfo_parent() == "":
            pass
            # if self.ouput_file is not None:
            #     self.output_file.close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRaterApp(root)
    root.mainloop()
