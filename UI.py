import os
import threading
import time
import tkinter
import tkinter.messagebox
import customtkinter

from PIL import Image
import sqlite3

import telegram_api

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
var_info = "TEST"

class App(customtkinter.CTk):
    def __init__(self, token):
        super().__init__()

        tb = telegram_api.TelegramBot(token, self)

        #self.get_dbInfo()

        # configure window
        #self.title("[PEASEC WARNBOT] Administrations-Panel")
        self.geometry(f"{1100}x{580}")
        self.title("PEASEC Warnbot - Bachelorthesis Marco Matissek")
        #self.geometry("1050x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Test/test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")),
                                                 # "CustomTkinter_logo_single.png")),
                                                 size=(40, 40))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 150))
        self.gradient_jpg = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bg_gradient.jpg")),
                                                   size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.behavior_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "behavior_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "behavior_light.png")),
            size=(20, 20))
        self.collection_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "collection_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "collection_light.png")),
            size=(20, 20))
        self.report_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "report_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "report_light.png")),
            size=(20, 20))
        self.data_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "data_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "data_light.png")),
            size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  PEASEC WARNBOT",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Warnungen verwalten",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.report_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Evaluierung",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.data_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Erstellen Custom Warnung",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.collection_image, anchor="w",
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        """
            Home Frame
        """

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_columnconfigure((2, 3), weight=0)
        self.home_frame.grid_rowconfigure((0, 1, 2), weight=1)


        # self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Anzahl Warnings: " + str(count))
        # self.home_frame_large_image_label.grid(row=1, column=3, padx=0, pady=0)

        #text_var = tkinter.StringVar(value="Anzahl User: " + str(count2))
        self.home_label = customtkinter.CTkLabel(self.home_frame, anchor="ne", justify="left", text="tmp\nTemp2")#text="Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))
        self.home_label.grid(row=0, column=3, padx=0, pady=0)

        # create main entry and button

        self.home_entry = customtkinter.CTkEntry(self.home_frame, placeholder_text="Deine Nachricht...")
        self.home_entry.grid(row=3, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.home_main_button_1 = customtkinter.CTkButton(master=self.home_frame, fg_color="transparent",
                                                          border_width=2,
                                                          text_color=("gray10", "#DCE4EE"), command=self.send_all_fnc,
                                                          text="Absenden")
        self.home_main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.home_textbox_updates = customtkinter.CTkTextbox(self.home_frame, width=300, state='disabled')
        self.home_textbox_updates.grid(row=1, column=0, padx=(20, 0), pady=(40, 0), sticky="nsew")

        self.home_textbox_sendmsg = customtkinter.CTkTextbox(self.home_frame, width=300, state='disabled')
        self.home_textbox_sendmsg.grid(row=1, column=2, padx=(20, 0), pady=(40, 0), sticky="nsew")

        # create Label
        self.home_label = customtkinter.CTkLabel(self.home_frame, text="Incoming Messages")
        self.home_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.home_label2 = customtkinter.CTkLabel(self.home_frame, text="Outgoing Messages")
        self.home_label2.grid(row=1, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="",
                                                                   image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, columnspan=3)

        """
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)
        """

        """
            Warnungen Frame
        """
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
                                                                     image=self.large_test_image)
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        """
            Evaluierung Frame
        """
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid(row=4, column=0, padx=20, pady=10)
        """
            Create Custom Warnung
        """
        self.four_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.four_frame.grid(row=4, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")

        #self.four_frame.grid_columnconfigure(1, weight=1)
        #self.four_frame.grid_columnconfigure((2, 3), weight=0)
        #self.four_frame.grid_rowconfigure((0, 1, 2), weight=1)



    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

        if name == "frame_4":
            self.four_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.four_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    #def change_appearance_mode_event(self, new_appearance_mode):
    #    customtkinter.set_appearance_mode(new_appearance_mode)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        prev = self.home_textbox_updates.get("0.0", "end")
        print(len(prev))
        print(self.home_textbox_updates.get("0.0", "end"))
        self.insert_update("Test")

    def insert_update(self, text: str):
        # self.textbox.delete("0.0", "end")  # delete all text
        # self.textbox.delete("0.0", "end")
        self.home_textbox_updates.configure(state="normal")
        # self.textbox_updates.insert(customtkinter.END, text + "\n")
        self.home_textbox_updates.insert("0.0", text + "\n")
        self.home_textbox_updates.configure(state="disabled")

    def insert_send_msg(self, text: str):
        self.home_textbox_sendmsg.configure(state="normal")
        self.home_textbox_sendmsg.insert("0.0", text + "\n")
        self.home_textbox_sendmsg.configure(state="disabled")

    def send_all_fnc(self):

        txt = self.home_entry.get()
        print(str(txt))     

        tb = telegram_api.TelegramBot("5979163637:AAFsR0MwfvPb9FwB2oPQKPQJlnkmkcZmKmg", self)
        tb.send_multiple_message(txt)

        self.home_entry.delete(0, len(txt))

    def get_dbInfo(self):
        global var_info
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM warnings")
        count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users")
        count2 = c.fetchone()[0]
        print("Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))
        self.home_label.config(text="Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))

        #threading.Timer(10, self.get_dbInfo).start()
        #self.home_label = customtkinter.CTkLabel(self.home_frame, anchor="ne", justify="left", text="Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))

"""
# if __name__ == "__main__":
    def start(self):
        app = App()
        app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
"""