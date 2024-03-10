import json
import tkinter.messagebox as mb
import customtkinter as CTk

import sys

obj_list = {}
vars_list = {}


def message(text):
    mb.showinfo(title='JCOM', message=str(text))


class App(CTk.CTk):
    app_objets = {}

    def __init__(self, title, width, height):
        super().__init__()
        self.geometry(f"{width}x{height}")
        self.title(title)

    def add(self, name, type, *args):
        global obj_list
        lin = f"obj_list['{name}'] = CTk.{type}(self"
        for e in args:
            lin += f", {e}"

        lin += ")"
        exec(str(lin))

    def do_grid(self, name, column: int, row: int, columnspan: int = None, rowspan: int = None, st: str = "ewns"):
        global obj_list
        exec(
            f"obj_list['{name}'].grid(row={row}, column={column}, padx=10, pady=10, sticky='{st}', columnspan={columnspan}, rowspan={rowspan})")


class Compiler:
    def __init__(self, path, printf=None):
        with open(path, "r") as file:
            self.res = json.load(file)
            if printf is not None:
                print(json.dumps(self.res, indent=2))

    def start(self):
        file = self.res
        settings = file["settings"]
        width = settings['width']
        height = settings['height']
        num = settings['objects']
        ye = settings['info']

        self.appi = App(settings['title'], width=width, height=height)

        if ye == True:
            self.info(settings['name'], settings['title'], width, height)

        objects = []
        for i in range(1, num + 1):
            line = "object" + str(i)
            objects.append(file[line])

        i = 1

        exec("import code", globals())

        for object in objects:
            name = "object" + str(i)
            type = object['type']

            if type == "label":
                type2 = "CTkLabel"
                self.appi.add(name, type2, f"text='{object['text']}'")

            elif type == "button":
                type2 = "CTkButton"
                self.appi.add(name, type2, f"text='{object['text']}'", f"command=code.{object['func']}")  # code.{object['func']}

            elif type == "textbox":
                type2 = "CTkEntry"
                self.appi.add(name, type2, "border_color=('#f9f9fa')",
                              f"show='{object['show']}', placeholder_text='{object['placeholder_text']}'")

            elif type == "textshield":
                type2 = "CTkTextbox"
                self.appi.add(name, type2, "height=100")

            self.appi.do_grid(name, object['column'], object['row'], object['columnspan'], object['rowspan'])

            i += 1

        CTk.set_appearance_mode(settings['theme'])

        self.appi.protocol("WM_DELETE_WINDOW", self.onclosed)
        self.appi.mainloop()

    def onclosed(self):
        sys.exit()

    def info(self, name, title, width, height):
        mb.showinfo(title='JCOM', message=(f"""Info:
    Name: {name}
    Title: {title}
    Width: {width}
    Height: {height}
                                                       """))


# if __name__ == '__main__':
#     c = Compiler("gui.json")
#     c.start()
