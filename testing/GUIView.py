from tkinter import *  # finicky to use
from tkinter import ttk
from tkinter import messagebox
import logging


from queue import Queue
doLog = False


class GUIView:

    print_Queue = Queue()  # Queue that contains commands
    logger = None
    controller = None
    #master = Tk()  # None

    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        master.title("RIT Formula HIL Testing")
        master.iconbitmap('rit2.ico')
        log_frame = ttk.Frame(master, padding="0 0 40 40")  # master was ttk
        log_frame.grid(row=2, column=1, rowspan=12, columnspan=1)
        id = StringVar()
        msg = StringVar()

        #  creating the elements in the gui
        entry_label = Label(master, text="File Name or Message")
        log_label = Label(master, text="Log:")
        act_label = Label(master, text="Actions")
        entry1 = Entry(master, width=16, textvariable=msg)
        enter_button = Button(master, text="Send", command=lambda: self.send_data(id, msg))
        log_button = Button(master, text="Log Data", command=self.log_data)
        end_button = Button(master, text="End Logging Data", command=self.stopLog)

        #  adding labels to row one
        log_label.grid(row=1, column=0, pady=2)  # log label
        entry_label.grid(row=1, column=1, pady=2)  # File name label
        act_label.grid(row=1, column=2, pady=2)

        #  adding things to row two
        log_button.grid(row=2, column=2, pady=3)
        log_frame.grid(row=2, column=0, rowspan=5, columnspan=1)
        entry1.grid(row=2, column=1, pady=2, stick=(W, E))

        enter_button.grid(row=3, column=1, pady=3)
        end_button.grid(row=3, column=2, pady=12, columnspan=1)

        logger = Text(log_frame, height=20, width=20)
        logger.grid(row=2, column=1, rowspan=5)
        logger.config(state=DISABLED)  # disables the ability to type into it

        for child in master.winfo_children(): child.grid_configure(padx=20, pady=5)

    def log_data(self):
        self.controller.log()
        print("Gonna log stuff")

    def stopLog(self):
        self.controller.cancel_log()

    # the sendData button on the gui starts this message
    # calls the send function in gui controller
    def send_data(self, id, msg):
        snd_msg = id.get() + " " + msg.get().strip()
        self.controller.send(snd_msg)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.end()
            self.master.destroy()

    def handle_print(self):
        while self.print_Queue.qsize():
            try:
                msg = self.print_Queue.get()
                '''
                # Create and configure logger
                logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')
                # Creating an object
                self.logger = logging.getLogger()
                self.logger.info(self, msg)

                '''
                self.logger.config(state=NORMAL)
                self.logger.insert(END, msg)
                self.logger.see(END)
                self.logger.config(state=DISABLED)

            except Queue.empty():  # added self as an extra agrument because it told me to
                pass

    def printMsg(self, msg):
        self.print_Queue.put(msg)

