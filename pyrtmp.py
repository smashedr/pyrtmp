#!/usr/bin/env python3
import tkinter as tk
import webbrowser
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import subprocess as sp
import os

HELP = """\
1. Select a video.
2. Enter the rtmp destination.
3. Click Start."""


class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a menu
        menu = tk.Menu(root)
        root.config(menu=menu)

        # add a file menu
        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Start Stream", command=self.start_stream)
        filemenu.add_command(label="End Stream", command=self.end_stream)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        # add a help menu
        helpmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Help", command=self.show_help)
        helpmenu.add_command(label="About", command=self.show_about)

        # create a prompt, an input box, an output label and button
        self.txtfile = tk.Label(self, text="File")
        self.e_file = tk.Entry(self)
        self.browse = tk.Button(self, text="Browse", command=self.load_file)
        self.txtstream = tk.Label(self, text="Stream")
        self.e_stream = tk.Entry(self)
        self.txtkbps = tk.Label(self, text="Kbps")
        self.e_kbps = tk.Entry(self)
        self.e_kbps.insert(tk.END, '3500')
        self.txtstatus = tk.Label(self, text="Status")
        self.output = tk.Label(self, text='')
        self.quit = tk.Button(self, text='Quit', command=root.quit)
        self.start = tk.Button(self, text='Start', command=self.start_stream)
        self.end = tk.Button(self, text='End', command=self.end_stream)

        # lay the widgets out on the screen.
        self.txtfile.grid(row=0)
        self.e_file.grid(row=0, column=1)
        self.browse.grid(row=0, column=3)
        self.txtstream.grid(row=1)
        self.e_stream.grid(row=1, column=1)
        self.txtkbps.grid(row=2)
        self.e_kbps.grid(row=2, column=1)
        self.txtstatus.grid(row=3)
        self.output.grid(row=3, column=1)
        self.quit.grid(row=4, column=1, sticky=tk.W, pady=4)
        self.start.grid(row=4, column=1, pady=4)
        self.end.grid(row=4, column=1, sticky=tk.E,  pady=4)

        self.update_status('Idle.')

    def start_stream(self):
        cmd = 'ffmpeg -re -i %s -vcodec libx264 -profile:v main -preset:v veryfast -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 3500k -maxrate %sk -bufsize 3500k -sws_flags lanczos+accurate_rnd -strict -2 -acodec aac -b:a 160k -ar 48000 -ac 2 -f flv %s' % (self.e_file.get(), self.e_kbps.get(), self.e_stream.get())
        cmd_list = cmd.split(' ')
        sp.Popen(cmd_list)
        self.update_status('STREAMING...')

    def end_stream(self):
        os.system('taskkill /f /im ffmpeg.exe')
        self.update_status('Idle.')

    def load_file(self):
        self.filename = askopenfilename(filetypes=(
            ("Video files", "*.mkv;*.flv;*.mp4;*.avi;*.mov"),
            ("All files", "*.*"),
        ))
        if self.filename:
            try:
                self.e_file.delete(0, 'end')
                self.e_file.insert(tk.END, self.filename)
            except Exception as error:
                print(error)
                showerror("Open Source File", "Failed to read file\n'%s'" % self.filename)
            return

    def update_status(self, new_status='Unavailable'):
        self.output.configure(text=new_status)

    def show_help(self):
        t = tk.Toplevel(self)
        t.geometry("260x140")
        t.wm_title("Help")
        l = tk.Label(t, text=HELP)
        l.pack(side="top", fill='both', expand=True)
        b = tk.Button(t, text='Close', command=t.destroy)
        b.pack(side="bottom", pady=5)

    def show_about(self):
        t = tk.Toplevel(self)
        t.geometry("260x180")
        t.wm_title("About")
        l = tk.Label(t, text="PyRTMP\n\nPowered By:")
        l.pack(side="top")
        p = tk.Label(t, text="www.streams.pw", fg="blue", cursor="hand2")
        p.pack(side="top")
        p.bind("<Button-1>", self.show_streams)
        a = tk.Label(t, text="Written By:\nShane Rice")
        a.pack(side="top", pady=10)
        b = tk.Button(t, text='Close', command=t.destroy)
        b.pack(side="bottom", pady=5)

    def show_streams(self, event):
        webbrowser.open_new(r"http://www.streams.pw")

if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry("540x260")
    root.wm_title("PyRTMP")
    PyRTMP = Window(root)
    PyRTMP.pack(fill='both', expand=True)
    root.mainloop()
