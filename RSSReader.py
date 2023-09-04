from tkinter import ttk
from tkinter import *
import requests


class ReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSS Reader")

        custom_font = ('Helvetica', 16)
        padding = 10

        self.label = Label(root, text='Titles', font=custom_font)
        self.label.pack(fill=BOTH, expand=True, padx=padding, pady=padding)
        self.listbox = Listbox(root)
        self.listbox.pack(fill=BOTH, expand=True, padx=padding, pady=padding)

        self.listbox.bind("<<ListboxSelect>>", self.show_content)

        self.label_text = Label(root, text='Description', font=custom_font)
        self.label_text.pack(fill=BOTH, expand=True, padx=padding, pady=padding)

        self.text = Text(root)
        self.text.pack(fill=BOTH, expand=True, padx=padding, pady=padding)

        self.update_button = ttk.Button(root, text="Update", command=self.update_list)
        self.update_button.pack(padx=padding, pady=padding)

        self.update_list()

    def update_list(self):
        self.listbox.delete(0, END)
        response = requests.get("https://rss.slashdot.org/Slashdot/slashdotMain")
        rss_content = response.text

        items = rss_content.split("<item rdf:about=")
        for i, item in enumerate(items[1:]):
            title = item.split("<title>")[1].split("</title>")[0]
            self.listbox.insert(END, title)
            if i % 2 == 0:
                self.listbox.itemconfig(i, {'bg': 'light gray'})

    def show_content(self, event):
        selected_item_index = self.listbox.curselection()[0]
        response = requests.get("https://rss.slashdot.org/Slashdot/slashdotMain")
        rss_content = response.text
        items = rss_content.split("<item rdf:about=")
        selected_item = items[selected_item_index + 1]
        title = selected_item.split("<title>")[1].split("</title>")[0]
        description = selected_item.split("<description>")[1].split("&lt;")[0]
        self.text.delete("1.0", END)
        self.text.insert(END, f"Title: {title}\n\n{description}")


if __name__ == "__main__":
    main_root = Tk()
    app = ReaderApp(main_root)
    main_root.mainloop()
