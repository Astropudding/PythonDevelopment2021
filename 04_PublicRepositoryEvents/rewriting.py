import tkinter as tk
from tkinter.messagebox import showinfo
import re

def geometry_parse(widget, string_params):

    row_params, col_grav_params = string_params.split(':')
    
    if '/' in col_grav_params:
        col_params, grav_params = col_grav_params.split('/')
    else:
        col_params = col_grav_params
        grav_params = None

    row_col_template = re.compile(r'(\d+)(\.\d+)?(\+\d+)?')
    row_res = row_col_template.match(row_params)
    
    row = int(row_res.group(1))
    row_weight = int(weight.strip('.')) if (weight := row_res.group(2)) is not None else 1
    row_span = int(rowspan.strip('+')) if (rowspan := row_res.group(3)) is not None else 0

    col_res = row_col_template.match(col_params)
    
    col = int(col_res.group(1))
    col_weight = int(weight.strip('.')) if (weight := col_res.group(2)) is not None else 1
    col_span = int(colspan.strip('+')) if (colspan := col_res.group(3)) is not None else 0

    if grav_params is None:
        grav_params = 'NEWS'
    
    widget.master.rowconfigure(row, weight=row_weight)
    widget.master.columnconfigure(col, weight=col_weight)

    widget.grid(row=row, column=col, rowspan=row_span+1, columnspan=col_span+1, sticky=grav_params)


class Application(tk.Frame):
    
    def __init__(self, master=None, title=''):
        super().__init__(master)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.createWidgets()
    
    def __getattr__(self, name):
        
        if name not in dir(self):
            def generate_widget(base_class, geometry, **kwargs):
                widget = self._construct_widget(base_class, geometry, **kwargs)
                setattr(self, name, widget)

            return generate_widget

        return self.__getattribute__(name)


    def _construct_widget(self, base_class, geometry, **kwargs):
        
        class GenWidget(base_class):
            
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
            
        GenWidget.__getattr__ = Application.__getattr__ 
        GenWidget._construct_widget = Application._construct_widget
        widget = GenWidget(self, **kwargs)

        geometry_parse(widget, geometry)

        return widget


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()