from Tkinter import *
from tkFileDialog import *
import pip, platform, os, pkg_resources, imp, random
import subprocess as sub


class Window:
    version = 2.1

    def __init__(self, selected):
        self.master = Tk()
        self.theme = Theme(selected)
        self.master.title('Module Installer')
        self.master.resizable(width=False, height=False)
        self.master.geometry('+%d+%d' % (self.master.winfo_screenwidth() / 3, self.master.winfo_screenheight() / 8))
        self.master.configure(bg=self.theme.bg)

        self.initGui()
        self.displayGui()
        self.configureWidgets()
        self.refresh(None)
        self.master.mainloop()

    def initGui(self):

        # Main Frame
        self.frame_main = Frame(self.master, self.theme.frame)
        self.headline = Label(self.frame_main, self.theme.label, text='Module Name')
        self.button_options = Button(self.frame_main, self.theme.button, text='>>>', width=5, height=1)
        self.entry = Entry(self.frame_main, self.theme.entry, width=40)
        self.button_install = Button(self.frame_main, self.theme.button, text='Install', width=10)
        self.button_browse = Button(self.frame_main, self.theme.button, text='Browse', width=10)
        self.button_upgrade = Button(self.frame_main, self.theme.button, text='Upgrade', width=10)
        self.scroll = Scrollbar(self.frame_main)
        self.entry_search = Entry(self.frame_main, self.theme.entry, width=30)
        self.listbox = Listbox(self.frame_main, width=38, height=15, yscrollcommand=self.scroll.set,
                               selectmode='multiple')
        self.scroll.config(command=self.listbox.yview)
        self.button_refresh = Button(self.frame_main, self.theme.button, width=7, height=1, text='Refresh')
        self.button_all = Button(self.frame_main, self.theme.button, width=10, text="Select All")
        self.button_remove = Button(self.frame_main, self.theme.button, text='Uninstall', width=10)
        self.label_version = Label(self.frame_main, self.theme.label, text=(str(self.version)))
        self.label_seperator = Label(self.frame_main, self.theme.label, text='__' * 25)

        self.var_console = IntVar()
        self.var_console.set(1)

        # Options Frame
        self.frame_options = Frame(self.master, self.theme.frame)
        self.label_options = Label(self.frame_options, self.theme.label, text='Options')
        self.check_console = Checkbutton(self.frame_options, self.theme.button, text='Display Console',
                                         variable=self.var_console,
                                         onvalue=True, offvalue=False, fg='black')

    def displayGui(self):

        # Main Frame
        self.frame_main.grid(row=0, column=0)
        self.button_options.grid(row=0, column=1, padx=5, pady=5, stick=E)
        self.headline.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        self.entry.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.button_install.grid(row=3, column=0, padx=5, pady=5)
        self.button_browse.grid(row=3, column=1, padx=5, pady=5)
        self.label_seperator.grid(row=4, column=0, columnspan=3, stick=W + E)
        self.button_upgrade.grid(row=5, column=0, padx=5, pady=5)
        self.button_remove.grid(row=5, column=1, padx=5, pady=5)
        self.entry_search.grid(row=6, column=0, columnspan=3, stick=E + W, pady=2, padx=5)
        self.listbox.grid(row=7, column=0, columnspan=2, padx=2, pady=2)
        self.scroll.grid(row=7, column=2, stick=N + S + W)
        self.button_refresh.grid(row=8, column=1, stick=W, padx=1, pady=1)
        self.button_all.grid(row=8, column=0, stick=W, padx=1, pady=1)
        self.label_version.grid(row=8, column=1, stick=E)

        # Options Frame
        self.label_options.grid(row=0, column=0)
        self.check_console.grid(row=1, column=0)

    def configureWidgets(self):
        self.button_options.bind('<ButtonRelease-1>', self.optionsMenu)
        self.button_install.bind('<ButtonRelease-1>', self.install)
        self.button_browse.bind('<ButtonRelease-1>', self.browseFile)
        self.button_refresh.bind('<ButtonRelease-1>', self.refresh)
        self.button_remove.bind('<ButtonRelease-1>', self.remove)
        self.button_upgrade.bind('<ButtonRelease-1>', self.upgrade)
        self.button_all.bind('<ButtonRelease-1>', self.selectAll)
        self.entry_search.bind('<KeyRelease>', self.searchListbox)
        self.listbox.bind('<ButtonRelease-3>', self.clearSelection)
        self.master.bind('<Return>', self.install)
        self.master.bind('<Escape>', self.clearEntry)
        self.master.bind('<Control-Key-R>', self.refresh)
        self.master.bind('<Control-Key-r>', self.refresh)

        self.options_on = False

        self.headline['text'] = 'Enter Module Name'
        self.entry.focus()

    def selectAll(self, event):
        if self.button_all["text"] == "Select All":
            self.listbox.select_set(0, END)
            self.button_all.config(text="Deselect")
        else:
            self.listbox.select_clear(0, END)
            self.button_all.config(text="Select All")

    def clearSelection(self, event):
        self.listbox.selection_clear(0, 'end')

    def searchListbox(self, event):
        keyword = self.entry_search.get()
        self.listbox.delete(0, 'end')
        for item in self.installed_packages_list:
            if keyword in item:
                self.listbox.insert('end', item)

    def optionsMenu(self, event):
        if self.options_on:
            self.frame_options.grid_forget()
            self.options_on = False
        else:
            self.frame_options.grid(row=0, column=1)
            self.options_on = True

    def getModName(self):
        try:
            if self.entry.get() not in ['', ' ', '   ']:
                return self.entry.get()
        except:
            return

    def browseFile(self, event):
        filename = askopenfilename(parent=self.master, filetypes=[('whl Files', ('*.whl')), ('All files', ('*'))])
        if filename == '': return
        self.entry.delete(0, 'end')
        self.entry.insert('end', filename)

    def upgrade(self, event):
        done = 1
        try:
            selected = self.listbox.curselection()
            mod_names = [self.listbox.get(mod).split(' == ')[0] for mod in selected]
        except:
            self.headline['text'] = 'Select a module from the list'
            return
        console_on = self.var_console.get()
        for mode in mod_names:
            if len(mode) < 1: return

            if console_on:
                done = sub.call(''.join(('python -m pip install --upgrade "', mode, '"')))
            else:
                done = sub.call(''.join(('python -m pip install --upgrade "', mode, '"')), creationflags=0x08000000)
            if done == 0:
                self.headline["text"] = ' '.join((mod_names[0], "Upgrade Successful"))
                self.master.update()
        self.headline["text"] = "Finished updating"

    def clearEntry(self, event):
        self.entry.delete(0, 'end')
        self.entry.focus()

    def remove(self, event):
        try:
            selected = self.listbox.curselection()
            mod_names = [self.listbox.get(mod).split('  ==  ')[0] for mod in selected]
        except:
            self.headline['text'] = "Select a module from the list"
            return

        console_on = self.var_console.get()

        for mode in mod_names:
            if mode in ['pip', 'setuptools']: continue

            if console_on:
                done = sub.call(''.join(('python -m pip uninstall -y "', mode, '"')))
            else:
                done = sub.call(''.join(('python -m pip uninstall -y "', mode, '"')), creationflags=0x08000000)

            if done == 0:
                self.headline['text'] = 'Module Remove Successful'
            else:
                self.headline['text'] = 'Error while removing module'

        self.refresh(None)

    def refresh(self, event):
        self.headline['text'] = 'Getting Modules'
        self.listbox.delete(0, 'end')
        self.entry_search.delete(0, 'end')
        self.refresh_packages()
        self.installed_packages = pip.get_installed_distributions()
        self.installed_packages_list = sorted(["%s  ==  %s" % (i.key, i.version) for i in self.installed_packages])
        for module in self.installed_packages_list:
            self.listbox.insert('end', module)
        self.headline['text'] = 'Module List Refreshed'

    def install(self, event):

        mod_name = self.getModName()
        if mod_name == None:
            return

        if mod_name.lower() in [item.split(' == ')[0] for item in self.listbox.get(0, 'end')]:
            self.headline['text'] = 'Module Already Installed'
            return
        else:
            self.headline['text'] = 'Module Being Installed'

        console_on = self.var_console.get()

        if platform.system() == 'Windows':
            if console_on:
                done = sub.call(''.join(('python -m pip install "', mod_name, '"')))
            else:
                done = sub.call(''.join(('python -m pip install "', mod_name, '"')), creationflags=0x08000000)
        else:
            done = 1
            self.headline['text'] = 'Operating System is not recognized'
            return

        mod_name = self.getCleanName(mod_name)

        if done == 0:
            self.headline['text'] = mod_name + ' Installed successfully'
            self.listbox.insert(0, mod_name + ' == (refresh)')
        else:
            self.headline['text'] = 'Error while installing ' + mod_name

        self.refresh(None)

    def getCleanName(self, raw):
        if '\\' in raw:
            raw = raw[raw.rfind('\\') + 1:]
        elif '/' in raw:
            raw = raw[raw.rfind('/') + 1:]

        if len(raw) > 14:
            return ''.join((raw[:15], '...'))
        else:
            return raw

    def refresh_packages(self):
        pip.utils.pkg_resources = imp.reload(pip.utils.pkg_resources)


class Theme:
    def __init__(self, selected=0):
        self.themes = [('steel blue', 'white'),
                       ('darkgreen', 'white'),
                       ('darkblue', 'white'),
                       ('darkred', 'white'),
                       ('sienna', 'burlywood')]  # More themes can be added
        self.selected = selected % len(self.themes)
        self.bg = self.themes[selected][0]  # Background
        self.fg = self.themes[selected][1]  # Foreground

        self.button = {'bg': self.bg, 'fg': self.fg, 'activeforeground': self.fg, 'activebackground': self.bg}
        self.label = {'bg': self.bg, 'fg': self.fg}
        self.entry = {'bg': self.fg}
        self.frame = {'bg': self.bg}


def main():
    root = Window(0)


if __name__ == '__main__':
    main()
