from tkinter import *
import write
import speak
import recognize

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "Pink"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        # text = Text(self.window)
        
        # text.tag_config("Assistant", background="yellow", foreground="yellow")
        # text.tag_config("start", background="black", foreground="green")
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=670, height=650, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=3, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.08, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressedW)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressedW(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.0268, relwidth=0.22)

        # voice button
        speak_button = Button(bottom_label, text="Speak", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressedS(None))
        speak_button.place(relx=0.77, rely=0.035, relheight=0.0268, relwidth=0.22)

        # gesture button
        speak_button = Button(bottom_label, text="Gesture", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressedG(None))
        speak_button.place(relx=0.77, rely=0.0614, relheight=0.0268, relwidth=0.22)
     
    def _on_enter_pressedW(self, event):
        msg = self.msg_entry.get()
        write.start(self,msg)
        # self._insert_message(msg, "You")
        # self._insert_message(result, "Assistant")

    def _on_enter_pressedS(self, event):
        # msg = self.msg_entry.get()
        result=speak.start(self)
        # self._insert_message(msg, "You")
        self._insert_message(result, "Assistant")  

    def _on_enter_pressedG(self, event):
        # msg = self.msg_entry.get()
        recognize.run()
        # self._insert_message(msg, "You")
        # self._insert_message(result, "Assistant")         
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()