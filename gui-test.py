from Tkinter import *

## I have a working ComboBox which is editable and
## has a button around here some where. I'll keep
## looking for that. In the mean time, this Entry
## subclass shares a StringVar with the menu item
## that are created form input list(s) to achive a
## simple ChoiceBox.

class ChoiceBox(Entry):
    """ComboBox(parent, itemList=[], *args, kwargs)
       A simple ChoiceBox with checked menu items
       itemList may be a mix of list of strings and lists of tuples of (label, list of strings)
       for one level of sub menu items. *args and kwargs are passed to the Entry widget."""

    def __init__(self, parent, itemList=[], *args, **kwargs):
        Entry.__init__(self, parent, *args, **kwargs)

        self.pyvar = pyvar = StringVar(self)    # this is the sharing mechanism
        self.config(textvariable=pyvar)         # add the StringVar to self.

        self.popup = popup = Menu(self, tearoff=0)
        self.bind("<Button-1>", self.mousedown, add="+")

        for item in itemList:
            if type(item) == tuple:
                submenu = self.GetSubMenu(item[0])
                for subitem in item[1]:
                    self.AddCBMenuItem(submenu, subitem)
            else:
                self.AddCBMenuItem(popup, item)

    def GetSubMenu(self, label):
        menu = Menu(self, tearoff=0)
        self.popup.add_cascade(menu=menu, label=label)
        return menu

    def AddCBMenuItem(self, menu, label):
        menu.add_checkbutton(label=label,
                             command=self.MenuSelect,
                             variable=self.pyvar,   # add the StringVar to a menu.
                             onvalue=label, offvalue='')

    def mousedown(self, event):
        x = event.x_root - event.x
        y = event.y_root -  event.y
        self.popup.post(x, y)
        return 'break'

    def get(self):
        return self.pyvar.get()

    def clear(self):
        self.pyvar.set('')

    def MenuSelect(self):
        pass


##        cb = ChoiceBox(root, [('test', ['one', 'two', 'three'])])

        cb.pack()
        root.mainloop()



root = Tk(className="mysmartprice Price Accuracy Check")

label1 = Label(text="Select the store you want to run accuracy test on: ")
label2 = Label(text="Result: ")
cb = ChoiceBox(root, ['jabong', 'shopclues', 'flipkart'])

label1.grid(row=0)
cb.grid(row=0, column=1)

label2.grid(row=1)



root.mainloop()
