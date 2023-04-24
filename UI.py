import configparser
import datetime
import os
import threading
import time
import re
import io
import tkinter
from io import BytesIO
from tkinter import messagebox
import urllib

import customtkinter

from PIL import Image, ImageTk
import sqlite3

from users import Users
from user_group import UserGroup
from db_functions import Database
import telegram_api

import ui_eval as uie  # Window Evaluierung

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
var_info = "TEST"

class App(customtkinter.CTk):
    def __init__(self, token):
        super().__init__()
        self.toplevel_window = None
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config_db = config["Datenbank"]
        self.config_telegram = config["TelegramAPI"]

        tb = telegram_api.TelegramBot(token, self)

        # configure window
        # self.title("[PEASEC WARNBOT] Administrations-Panel")
        self.geometry(f"{1100}x{580}")
        self.title("PEASEC Warnbot - Bachelorthesis Marco Matissek")
        # self.geometry("1050x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")),
                                                 # "CustomTkinter_logo_single.png")),
                                                 size=(40, 40))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                                       size=(500, 150))
        self.banner_home = customtkinter.CTkImage(Image.open(os.path.join("images/PEASEC_WARNBOT.png")),
                                                  size=(600, 150))
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
        self.navigation_frame.grid_rowconfigure(10, weight=1)

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

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Evaluierung",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.data_image, anchor="w",
                                                      command=self.open_toplevel)
        self.frame_4_button.grid(row=2, column=0, sticky="ew")

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Warnmeldungen",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=12, weight="bold"))
        self.navigation_frame_label.grid(row=3, column=0, padx=5, pady=(20, 0), sticky="sw")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Warnungen verwalten",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.report_image, anchor="w",
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=4, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Erstellen Custom Warnung",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.collection_image, anchor="w",
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=5, column=0, sticky="ew")

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Benutzerverwaltung",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=12, weight="bold"))
        self.navigation_frame_label.grid(row=6, column=0, padx=5, pady=(20, 0), sticky="sw")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Benutzer",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_5_button_event)
        self.frame_5_button.grid(row=7, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Gruppen",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_6_button_event)
        self.frame_6_button.grid(row=8, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

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

        # text_var = tkinter.StringVar(value="Anzahl User: " + str(count2))
        self.home_label_dbInfo = customtkinter.CTkLabel(self.home_frame, anchor="ne", justify="left",
                                                        text="tmp\nTemp2")  # text="Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))
        self.home_label_dbInfo.grid(row=0, column=3, padx=0, pady=0)

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
                                                                   image=self.banner_home)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=0, pady=0, columnspan=3)

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
        self.second_frame.grid_columnconfigure(1, weight=1)
        self.second_frame.grid_columnconfigure((2, 3), weight=0)
        # self.second_frame.grid_rowconfigure((9, 10), weight=0)
        ## LOGO
        # self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="",
        #                                                             image=self.large_test_image)
        # self.second_frame_large_image_label.grid(row=0, column=0, padx=0, pady=0, columnspan=3)
        self.second_frame.label = customtkinter.CTkLabel(master=self.second_frame, text="WARNMELDUNGEN OVERVIEW",
                                                         font=("Arial", 30),
                                                         text_color="#4a97cf")
        self.second_frame.label.grid(row=0, column=0, padx=20, pady=(20, 20), columnspan=4, sticky="nesw")
        ## Dropdown
        results = []
        versions = []
        conn = sqlite3.connect(self.config_db['PATH'])
        c = conn.cursor()
        c.execute("SELECT DISTINCT(warnings.wid), warnings.title_de, warnings.last_update, warning_information.wid "
                  "FROM warnings INNER JOIN warning_information WHERE warnings.wid = warning_information.wid GROUP "
                  "BY warnings.wid, warnings.title_de ORDER BY warnings.ID DESC")
        res_values = c.fetchall()
        print(len(res_values))
        for i in res_values:
            results.append(str(i[2]) + ": " + str(i[1]) + " (" + str(i[0]) + ")")

        self.combobox_warnungen = customtkinter.CTkComboBox(master=self.second_frame, values=results,
                                                            command=self.combobox_callback_warnings, width=500)
        self.combobox_warnungen.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nw", columnspan=2)

        self.combobox_version = customtkinter.CTkComboBox(master=self.second_frame, values=[], width=50,
                                                          command=lambda value: self.combobox_callback_warnings(
                                                              self.combobox_warnungen.get(), value))
        self.combobox_version.grid(row=1, column=3, padx=(0, 0), pady=(0, 0), sticky="ne", columnspan=1)
        # self.combobox_warnungen.set("option 2")  # set initial value

        self.second_title = customtkinter.CTkEntry(master=self.second_frame,
                                                   placeholder_text="Wähle eine Warnmeldung aus",
                                                   width=500,
                                                   height=25,
                                                   border_width=2,
                                                   corner_radius=10)
        self.second_title.grid(row=2, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=2)

        self.second_desc = customtkinter.CTkTextbox(self.second_frame, width=300, state='normal')
        self.second_desc.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew", columnspan=2)
        self.second_desc.insert("0.0", "Wähle eine Warnung aus!")

        ## Bild und Bildbeschriftung
        self.second_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "platzhalter.png")).resize((256, 256)),
            dark_image=Image.open(os.path.join(image_path, "platzhalter.png")).resize((256, 256)), size=(256, 256))
        self.second_imgframe = customtkinter.CTkLabel(self.second_frame, text="", image=self.second_img)
        self.second_imgframe.grid(row=4, column=3, padx=0, pady=0)
        self.img_description = customtkinter.CTkLabel(self.second_frame, text="second_img Beschriftung",
                                                      fg_color="#4a97cf")
        self.img_description.grid(row=4, column=3, padx=(0, 0), pady=(236, 0), sticky="nesw")

        self.second_codeiiimg = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "platzhalter.png")).resize((256, 256)),
            dark_image=Image.open(os.path.join(image_path, "platzhalter.png")).resize((256, 256)), size=(20, 20))
        self.second_codeImg = customtkinter.CTkLabel(self.second_frame, text="", image=self.second_codeiiimg)
        self.second_codeImg.grid(row=2, column=3, padx=0, pady=0, sticky="nw")
        self.second_codeImglabel = customtkinter.CTkLabel(self.second_frame, text="Event: n/A")
        self.second_codeImglabel.grid(row=2, column=3, padx=(25, 0), pady=(0, 0), sticky="nw")

        ## Labels
        self.second_label = customtkinter.CTkLabel(self.second_frame, text="Wähle Warnung:")
        self.second_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.second_label_version = customtkinter.CTkLabel(self.second_frame, text="Version:")
        self.second_label_version.grid(row=1, column=3, padx=(0, 55), pady=(0, 0), sticky="ne")
        self.second_label = customtkinter.CTkLabel(self.second_frame, text="Titel:")
        self.second_label.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.second_label = customtkinter.CTkLabel(self.second_frame, text="Beschreibung:")
        self.second_label.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.second_label = customtkinter.CTkLabel(self.second_frame, text="Bild:")
        self.second_label.grid(row=3, column=3, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.second_label_Type = customtkinter.CTkLabel(self.second_frame, text="Type:")
        self.second_label_Type.grid(row=5, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.second_label_Scope = customtkinter.CTkLabel(self.second_frame, text="Scope:")
        self.second_label_Scope.grid(row=5, column=1, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.second_label_Web = customtkinter.CTkLabel(self.second_frame, text="Web:")
        self.second_label_Web.grid(row=6, column=0, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=2)

        self.second_label_Effectiv = customtkinter.CTkLabel(self.second_frame,
                                                            text="Effective: \t\t Onset: \t\t Expires:")
        self.second_label_Effectiv.grid(row=7, column=0, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=4)

        ## Buttons
        self.second_frame_button_goto = customtkinter.CTkButton(self.second_frame, corner_radius=10, height=40,
                                                                border_spacing=10, text="Aufrufen",
                                                                fg_color="#51abcb", text_color=("gray10", "gray90"),
                                                                hover_color=("#a8d5e5", "#92cbdf"),
                                                                anchor="w",
                                                                state="normal",
                                                                )  # command=lambda: self.del_group(self.gr_txtb_nr.get()))
        self.second_frame_button_goto.grid(row=8, column=3, sticky="ne", padx=(0, 20), columnspan=1)

        """
        Button um Warnmeldungen direkt versenden zu können! Nutzer wird in send_warning hinterlegt
        self.second_frame_button_send = customtkinter.CTkButton(self.second_frame, corner_radius=10, height=40,
                                                                border_spacing=10, text="Senden an mich",
                                                                fg_color="#51abcb", text_color=("gray10", "gray90"),
                                                                hover_color=("#a8d5e5", "#92cbdf"),
                                                                anchor="w",
                                                                state="normal",
                                                                command=self.send_warning)
        self.second_frame_button_send.grid(row=8, column=2, sticky="ne", padx=(0, 20), columnspan=1)"""

        """
            Create Custom Warnung
        """
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(1, weight=1)
        self.third_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.third_frame.grid_rowconfigure((9, 10), weight=0)

        ## LOGO
        self.third_frame.label = customtkinter.CTkLabel(master=self.third_frame, text="CUSTOM WARNMELDUNG",
                                                        font=("Arial", 30),
                                                        text_color="#4a97cf")
        self.third_frame.label.grid(row=0, column=0, padx=20, pady=(20, 20), columnspan=4, sticky="nesw")

        ## Inputs
        self.third_frame_ID = customtkinter.CTkEntry(master=self.third_frame, placeholder_text="custom.000000",
                                                     height=25, width=500, border_width=2, corner_radius=10)
        self.third_frame_ID.grid(row=1, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=3)

        self.third_frame_event = customtkinter.CTkEntry(master=self.third_frame,
                                                        placeholder_text="Warnmeldung", height=25,
                                                        width=250, border_width=2, corner_radius=10)
        self.third_frame_event.grid(row=7, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_expires = customtkinter.CTkEntry(master=self.third_frame,
                                                          placeholder_text="01.01.1991 12:00:00", height=25,
                                                          width=250, border_width=2, corner_radius=10)
        self.third_frame_expires.grid(row=8, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_effective = customtkinter.CTkEntry(master=self.third_frame,
                                                            placeholder_text="01.01.1991 12:00:00", height=25,
                                                            width=250, border_width=2, corner_radius=10)
        self.third_frame_effective.grid(row=9, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_Title = customtkinter.CTkEntry(master=self.third_frame,
                                                        placeholder_text="Titel der Warnmeldung",
                                                        height=25,
                                                        width=500,
                                                        border_width=2,
                                                        corner_radius=10)
        self.third_frame_Title.grid(row=2, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=3)

        # Textboxen
        self.third_frame_desc = customtkinter.CTkTextbox(self.third_frame, state='normal', height=100, border_width=2)
        self.third_frame_desc.grid(row=3, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew", columnspan=1, rowspan=2)
        self.third_frame_instuc = customtkinter.CTkTextbox(self.third_frame, state='normal', height=100, border_width=2)
        self.third_frame_instuc.grid(row=5, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew", columnspan=1, rowspan=2)

        ## Linke Seite
        self.third_frame_img = customtkinter.CTkEntry(master=self.third_frame,
                                                      placeholder_text="URL zum Bild", height=25,
                                                      width=250, border_width=2, corner_radius=10)
        self.third_frame_img.grid(row=3, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_imgc = customtkinter.CTkEntry(master=self.third_frame,
                                                       placeholder_text="URL zum Bild", height=25,
                                                       width=250, border_width=2, corner_radius=10)
        self.third_frame_imgc.grid(row=4, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_web = customtkinter.CTkEntry(master=self.third_frame,
                                                      placeholder_text="URL zur Webseite", height=25,
                                                      width=250, border_width=2, corner_radius=10)
        self.third_frame_web.grid(row=5, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_Sender = customtkinter.CTkEntry(master=self.third_frame,
                                                         placeholder_text="Name des Senders", height=25,
                                                         width=250, border_width=2, corner_radius=10)
        self.third_frame_Sender.grid(row=6, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_Status = customtkinter.CTkEntry(master=self.third_frame,
                                                         placeholder_text="Actual", height=25,
                                                         width=250, border_width=2, corner_radius=10)
        self.third_frame_Status.grid(row=7, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_area = customtkinter.CTkEntry(master=self.third_frame,
                                                       placeholder_text="Stadt Darmstadt, ....", height=25,
                                                       width=250, border_width=2, corner_radius=10)
        self.third_frame_area.grid(row=8, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_urgancy = customtkinter.CTkComboBox(master=self.third_frame,
                                                             values=['Immediate', 'Unknown'],
                                                             width=250)
        self.third_frame_urgancy.grid(row=9, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_severity = customtkinter.CTkComboBox(master=self.third_frame,
                                                              values=['Minor', 'Severe', 'Moderate'],
                                                              width=250)
        self.third_frame_severity.grid(row=10, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.third_frame_certainty = customtkinter.CTkComboBox(master=self.third_frame,
                                                               values=['Observed', 'Likely', 'Unknown'],
                                                               width=250)
        self.third_frame_certainty.grid(row=11, column=3, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)

        ## Labels
        self.third_frame_lbl_ID = customtkinter.CTkLabel(self.third_frame, text="WarnungsID:")
        self.third_frame_lbl_ID.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_lbl_title = customtkinter.CTkLabel(self.third_frame, text="Titel:")
        self.third_frame_lbl_title.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_lbl_descr = customtkinter.CTkLabel(self.third_frame, text="Beschreibung:")
        self.third_frame_lbl_descr.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_Verhalten = customtkinter.CTkLabel(self.third_frame, text="Verhalten:")
        self.third_frame_Verhalten.grid(row=5, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.third_frame_Event = customtkinter.CTkLabel(self.third_frame, text="Event:")
        self.third_frame_Event.grid(row=7, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.third_frame_Expires = customtkinter.CTkLabel(self.third_frame, text="Expires:")
        self.third_frame_Expires.grid(row=8, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_Effective = customtkinter.CTkLabel(self.third_frame, text="Effective:")
        self.third_frame_Effective.grid(row=9, column=0, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=4)

        self.third_frame_lbl_img = customtkinter.CTkLabel(self.third_frame, text="Bild (Meldung):")
        self.third_frame_lbl_img.grid(row=3, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_lbl_img = customtkinter.CTkLabel(self.third_frame, text="Bild (Code):")
        self.third_frame_lbl_img.grid(row=4, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.third_frame_Web = customtkinter.CTkLabel(self.third_frame, text="Web:")
        self.third_frame_Web.grid(row=5, column=2, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=2)
        self.third_frame_sender = customtkinter.CTkLabel(self.third_frame, text="Sender (Name):")
        self.third_frame_sender.grid(row=6, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_status = customtkinter.CTkLabel(self.third_frame, text="Status:")
        self.third_frame_status.grid(row=7, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_Area = customtkinter.CTkLabel(self.third_frame, text="Area:")
        self.third_frame_Area.grid(row=8, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.third_frame_Urgancy = customtkinter.CTkLabel(self.third_frame, text="Urgancy:")
        self.third_frame_Urgancy.grid(row=9, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_Severity = customtkinter.CTkLabel(self.third_frame, text="Severity:")
        self.third_frame_Severity.grid(row=10, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.third_frame_Certainty = customtkinter.CTkLabel(self.third_frame, text="Certainty:")
        self.third_frame_Certainty.grid(row=11, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        self.third_frame_tmpVar = customtkinter.CTkLabel(self.third_frame, text="1")
        self.third_frame_tmpVar.grid(row=10, column=1, padx=(20, 0), pady=(0, 0), sticky="nw")

        ## Buttons
        self.third_frame_btn_save = customtkinter.CTkButton(master=self.third_frame, fg_color="transparent",
                                                            border_width=2,
                                                            text_color=("gray10", "#DCE4EE"),
                                                            command=self.save_new_warning,
                                                            text="Speichern")
        self.third_frame_btn_save.grid(row=13, column=3, padx=(20, 20), pady=(20, 20), sticky="se")
        self.third_frame_btn_save = customtkinter.CTkButton(master=self.third_frame, fg_color="transparent",
                                                            border_width=2,
                                                            text_color=("gray10", "#DCE4EE"),
                                                            command=lambda: self.save_new_warning(True),
                                                            text="Deaktivieren")
        self.third_frame_btn_save.grid(row=13, column=2, padx=(20, 0), pady=(20, 20), sticky="se")

        """
            Not USED
        """
        self.four_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.four_frame.grid(row=4, column=0, padx=20, pady=10)

        """
            Verwaltung Benutzer
        """
        self.five_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.five_frame.grid_columnconfigure(1, weight=1)
        self.five_frame.grid_columnconfigure((3, 4), weight=0)
        self.five_frame.grid_rowconfigure((7, 8), weight=0)
        ## LOGO
        self.five_frame.label = customtkinter.CTkLabel(master=self.five_frame, text="BENUTZERVERWALTUNG",
                                                       font=("Arial", 30),
                                                       text_color="#4a97cf")
        self.five_frame.label.grid(row=0, column=0, padx=20, pady=(20, 20), columnspan=6, sticky="nesw")

        ## Select User
        u = Users(0)
        self.combobox_users = customtkinter.CTkComboBox(master=self.five_frame, values=u.get_all_users(),
                                                        command=self.combobox_callback_users, width=600)
        self.combobox_users.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nw", columnspan=1)

        ## Textboxen usw
        self.txtb_id = customtkinter.CTkEntry(master=self.five_frame,
                                              placeholder_text="Wähle einen User",
                                              width=200,
                                              height=25,
                                              border_width=2,
                                              corner_radius=10)
        self.txtb_id.grid(row=2, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.txtb_Name = customtkinter.CTkEntry(master=self.five_frame,
                                                placeholder_text="Wähle einen User",
                                                width=200,
                                                height=25,
                                                border_width=2,
                                                corner_radius=10)
        self.txtb_Name.grid(row=2, column=3, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.txtb_ChatID = customtkinter.CTkEntry(master=self.five_frame,
                                                  placeholder_text="Wähle einen User",
                                                  width=200,
                                                  height=25,
                                                  border_width=2,
                                                  corner_radius=10)
        self.txtb_ChatID.grid(row=3, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.txtb_UID = customtkinter.CTkEntry(master=self.five_frame,
                                               placeholder_text="Wähle einen User",
                                               width=200,
                                               height=25,
                                               border_width=2,
                                               corner_radius=10)
        self.txtb_UID.grid(row=3, column=3, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.txtb_lang = customtkinter.CTkEntry(master=self.five_frame,
                                                placeholder_text="Wähle einen User",
                                                width=200,
                                                height=25,
                                                border_width=2,
                                                corner_radius=10)
        self.txtb_lang.grid(row=4, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.txtb_group = customtkinter.CTkComboBox(master=self.five_frame, values=UserGroup().get_all_groups(),
                                                    width=200)
        self.txtb_group.grid(row=4, column=3, padx=(0, 0), pady=(0, 0), sticky="nw", columnspan=1)

        self.txtb_wartungstypen = customtkinter.CTkEntry(master=self.five_frame,
                                                placeholder_text="Wähle einen User",
                                                width=200,
                                                height=25,
                                                border_width=2,
                                                corner_radius=10)
        self.txtb_wartungstypen.grid(row=5, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.txtb_location = customtkinter.CTkEntry(master=self.five_frame,
                                                         placeholder_text="Wähle einen User",
                                                         width=200,
                                                         height=25,
                                                         border_width=2,
                                                         corner_radius=10)
        self.txtb_location.grid(row=5, column=3, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        ## Buttons
        self.five_frame_button_del = customtkinter.CTkButton(self.five_frame, corner_radius=10, height=40,
                                                             border_spacing=10, text="Benutzer löschen",
                                                             fg_color="#E64422", text_color=("gray10", "gray90"),
                                                             hover_color=("#E64422", "#E56D54"),
                                                             anchor="w",
                                                             state="disabled",
                                                             command=lambda: self.del_user(u.get_all_users()))
        self.five_frame_button_del.grid(row=9, column=3, sticky="nw", padx=(10, 0), columnspan=2)

        self.five_frame_button_edit = customtkinter.CTkButton(self.five_frame, corner_radius=10, height=40,
                                                              border_spacing=10, text="Benutzer bearbeiten",
                                                              fg_color="#69AF3F", text_color=("gray10", "gray90"),
                                                              hover_color=("#69AF3F", "#8BE554"),
                                                              anchor="w",
                                                              command=self.edit_user, state="disabled")
        self.five_frame_button_edit.grid(row=9, column=0, sticky="ne", columnspan=2)

        ## Labels
        self.five_frame.second_label = customtkinter.CTkLabel(self.five_frame, text="Wähle User:")
        self.five_frame.second_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_ID = customtkinter.CTkLabel(self.five_frame, text="ID:")
        self.five_frame.lbl_ID.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_Name = customtkinter.CTkLabel(self.five_frame, text="Name:")
        self.five_frame.lbl_Name.grid(row=2, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_ChatID = customtkinter.CTkLabel(self.five_frame, text="ChatID:")
        self.five_frame.lbl_ChatID.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_UID = customtkinter.CTkLabel(self.five_frame, text="UID:")
        self.five_frame.lbl_UID.grid(row=3, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_lang = customtkinter.CTkLabel(self.five_frame, text="Sprache:")
        self.five_frame.lbl_lang.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_group = customtkinter.CTkLabel(self.five_frame, text="Gruppe:")
        self.five_frame.lbl_group.grid(row=4, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_warnings = customtkinter.CTkLabel(self.five_frame, text="Wartungsarten:")
        self.five_frame.lbl_warnings.grid(row=5, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.five_frame.lbl_warnings = customtkinter.CTkLabel(self.five_frame, text="Standort:")
        self.five_frame.lbl_warnings.grid(row=5, column=2, padx=(20, 0), pady=(0, 0), sticky="nw")

        """
            Gruppen Frame
        """
        self.six_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.six_frame.grid(row=4, column=0, padx=20, pady=10)

        self.six_frame.grid_columnconfigure(1, weight=1)
        self.six_frame.grid_columnconfigure((0, 1), weight=0)
        self.six_frame.grid_rowconfigure((7, 8), weight=0)

        ## LOGO
        self.six_frame.label = customtkinter.CTkLabel(master=self.six_frame, text="GRUPPENVERWALTUNG",
                                                      font=("Arial", 30),
                                                      text_color="#4a97cf")
        self.six_frame.label.grid(row=0, column=0, padx=20, pady=(20, 20), columnspan=6, sticky="nesw")

        ## Select User
        self.gr_combobox_groups = customtkinter.CTkComboBox(master=self.six_frame, values=[],
                                                            command=self.combobox_callback_userGroup, width=600)
        self.gr_combobox_groups.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nw", columnspan=1)

        ## Textboxen usw
        self.gr_txtb_id = customtkinter.CTkEntry(master=self.six_frame,
                                                 placeholder_text="Wähle eine Gruppe",
                                                 width=200,
                                                 height=25,
                                                 border_width=2,
                                                 corner_radius=10)
        self.gr_txtb_id.grid(row=2, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.gr_txtb_nr = customtkinter.CTkEntry(master=self.six_frame,
                                                 placeholder_text="Wähle eine Gruppe",
                                                 width=200,
                                                 height=25,
                                                 border_width=2,
                                                 corner_radius=10)
        self.gr_txtb_nr.grid(row=3, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.gr_txtb_descr = customtkinter.CTkEntry(master=self.six_frame,
                                                    placeholder_text="Wähle eine Gruppe",
                                                    width=500,
                                                    height=25,
                                                    border_width=2,
                                                    corner_radius=10)
        self.gr_txtb_descr.grid(row=4, column=1, padx=(0, 0), pady=(5, 0), sticky="nw", columnspan=3)

        self.gr_textbox_users = customtkinter.CTkTextbox(self.six_frame, width=200, state='disabled', border_width=2)
        self.gr_textbox_users.grid(row=5, column=1, padx=(0, 0), pady=(5, 10), sticky="nsew", columnspan=2)

        ## Buttons
        self.six_frame_button_del = customtkinter.CTkButton(self.six_frame, corner_radius=10, height=40,
                                                            border_spacing=10, text="Gruppe löschen",
                                                            fg_color="#E64422", text_color=("gray10", "gray90"),
                                                            hover_color=("#E64422", "#E56D54"),
                                                            anchor="w",
                                                            state="disabled",
                                                            command=lambda: self.del_group(self.gr_txtb_nr.get()))
        self.six_frame_button_del.grid(row=7, column=1, sticky="ne", padx=(0, 0), columnspan=1)

        self.six_frame_button_edit = customtkinter.CTkButton(self.six_frame, corner_radius=10, height=40,
                                                             border_spacing=10, text="Speichern",
                                                             fg_color="#69AF3F", text_color=("gray10", "gray90"),
                                                             hover_color=("#69AF3F", "#8BE554"),
                                                             anchor="w",
                                                             command=lambda: self.save_group(self.gr_txtb_nr.get(),
                                                                                             self.gr_txtb_descr.get()),
                                                             state="disabled")
        self.six_frame_button_edit.grid(row=7, column=2, padx=(10, 0), sticky="nw", columnspan=1)

        self.six_frame_button_new = customtkinter.CTkButton(self.six_frame, corner_radius=10, height=40,
                                                            border_spacing=10, text="(+) Neue Gruppe",
                                                            fg_color="#69AF3F", text_color=("gray10", "gray90"),
                                                            hover_color=("#69AF3F", "#8BE554"),
                                                            anchor="w",
                                                            command=lambda: self.new_group(self.txtb_group.get(),
                                                                                           self.gr_txtb_descr.get()),
                                                            state="normal")
        self.six_frame_button_new.grid(row=0, column=2, padx=(0, 0), sticky="ne", columnspan=1)

        ## Labels
        self.six_frame.second_label = customtkinter.CTkLabel(self.six_frame, text="Wähle Gruppe:")
        self.six_frame.second_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.six_frame.lbl_ID = customtkinter.CTkLabel(self.six_frame, text="ID:")
        self.six_frame.lbl_ID.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.six_frame.lbl_gruppennr = customtkinter.CTkLabel(self.six_frame, text="Gruppennr:")
        self.six_frame.lbl_gruppennr.grid(row=3, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.six_frame.lbl_Beschreibung = customtkinter.CTkLabel(self.six_frame, text="Beschreibung:")
        self.six_frame.lbl_Beschreibung.grid(row=4, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.six_frame.lbl_users = customtkinter.CTkLabel(self.six_frame, text="User in Gruppe:")
        self.six_frame.lbl_users.grid(row=5, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        """
            Default
        """
        # select default frame
        self.select_frame_by_name("home")

        # initiale Funktionen die ausgeführt werden sollen
        self.get_dbInfo()

        # self.four_frame.grid_columnconfigure(1, weight=1)
        # self.four_frame.grid_columnconfigure((2, 3), weight=0)
        # self.four_frame.grid_rowconfigure((0, 1, 2), weight=1)

    def select_frame_by_name(self, name):
        """
        Wählt das Frame aus, nach übermittlung des Namen.
        :param name:
        :return:
        """
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")

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

        if name == "frame_5":
            self.five_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.five_frame.grid_forget()

        if name == "frame_6":
            self.six_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.six_frame.grid_forget()

    def home_button_event(self):
        """
        Öffnet die Startseite (home)
        :return:
        """
        self.get_dbInfo()
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        """
        Öffnet die Warnmeldungen UI und lädt alle Inhalte
        :return:
        """
        results = []
        conn = sqlite3.connect(self.config_db['PATH'])
        c = conn.cursor()
        c.execute("SELECT DISTINCT(warnings.wid), warnings.title_de, warnings.last_update, warning_information.wid "
                  "FROM warnings INNER JOIN warning_information WHERE warnings.wid = warning_information.wid GROUP "
                  "BY warnings.wid, warnings.title_de ORDER BY warnings.ID DESC")
        res_values = c.fetchall()
        print(len(res_values))
        for i in res_values:
            results.append(str(i[2]) + ": " + str(i[1]) + " (" + str(i[0]) + ")")

        self.combobox_warnungen.configure(values=results)
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        """
        Öffnet Frame 3 : Custom Warnungen
        :return:
        """
        self.clear_frame_3()
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        """
        Öffnet Frame 4: Not used
        :return:
        """
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        """
            Öffnet Frame 5: Verwaltung User
        :return:
        """
        u = Users(0)
        print(len(u.get_all_users()))
        self.combobox_users.configure(values=u.get_all_users())

        self.select_frame_by_name("frame_5")

    def frame_6_button_event(self):
        """
            Frame 6, für die UserGruppen
        :return:
        """
        ug = UserGroup()
        self.gr_combobox_groups.configure(values=ug.get_all_groups())
        self.gr_combobox_groups.set(ug.get_all_groups()[0])
        self.select_frame_by_name("frame_6")

    # def change_appearance_mode_event(self, new_appearance_mode):
    #    customtkinter.set_appearance_mode(new_appearance_mode)
    def open_toplevel(self):
        """
        Öffnet die Evaluation-Userform
        :return:
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = uie.ToplevelWindow(self, self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def fill_values(self):
        """
        Ruft die WarnIDs von warnings auf und gibt diese aus
        :return:
        """
        results = []
        conn = sqlite3.connect(self.config_db['PATH'])
        c = conn.cursor()
        c.execute("SELECT wid FROM warnings")
        res_values = c.fetchall()

        for i in res_values:
            print(i)

        # return result

    def combobox_callback_userGroup(self, choice):
        """
            Zeigt alle USer in einer Gruppe an
        :param choice:
        :return:
        """
        if choice == "n/A":
            return None

        ## Setze alles auf Leer beim wechsel
        self.gr_txtb_id.configure(state="normal")
        self.gr_textbox_users.configure(state="normal")

        self.gr_txtb_nr.delete(0, customtkinter.END)
        self.gr_txtb_descr.delete(0, customtkinter.END)
        self.gr_textbox_users.delete("0.0", customtkinter.END)
        self.gr_txtb_id.delete(0, customtkinter.END)

        ## Daten aus der DB einlesen
        substring = choice.split(":", 1)[0]
        results = Database.get_query("user_groups", "ID=" + str(substring))
        result = results[0]

        gr_users = Database.get_query("users", "group_id={}".format(substring))
        print(gr_users)
        if len(gr_users) > 0:
            str_gr_users = ""
            for e in gr_users:
                # Ausgabe der User als String pro Zeile und mit TABULATOR als Trenner
                str_gr_users = str_gr_users + str(e[0]) + "\t\t" + str(e[1]) + "\t\t" + str(e[2]) + "\t\t" + str(
                    e[3]) + "\t\t" + str(e[4]) + "\t\t" + str(e[5]) + "\n"
        else:
            # Falls keine User in der Gruppe sind.
            str_gr_users = "\nKeine User in dieser Gruppe vorhanden..."
            # print("dddd" + str(gr_users))

        ## Daten einfügen
        self.gr_txtb_nr.insert(0, str(result[1]))
        self.gr_txtb_descr.insert(0, str(result[2]))
        self.gr_textbox_users.insert("0.0", "ID\t\tUID\t\tName\t\tSprache\t\twarnings\t\tChatID" + "\n" +
                                     "-------------------------------------------------------------------------------"
                                     "-------------------------------------------------------------------------------"
                                     "-------------\n" + str_gr_users)
        # self.gr_textbox_users.insert(0, "UID\tName\tChatID")
        self.gr_txtb_id.insert(0, str(result[0]))

        self.gr_txtb_id.configure(state="disabled")
        self.gr_textbox_users.configure(state="disabled")

    def save_group(self, gnr, descr):
        """
        Gruppe speichern
        :param gnr:
        :param descr:
        :return:
        """
        ug = UserGroup()
        ug.edit_group(gnr, descr)

    def del_group(self, gid):
        """
        Gruppe löschen
        :param gid:
        :return:
        """
        ug = UserGroup()
        ug.del_group(gid)

    def new_group(self, gnr, descr):
        """
        Neue Usergruppe erstellen - UI Einstellungen
        :param gnr:
        :param descr:
        :return:
        """
        ug = UserGroup()
        self.gr_txtb_id.configure(state="normal")
        self.gr_txtb_id.delete(0, customtkinter.END)
        self.gr_txtb_id.insert(0, "Wird automatisch vergeben...")
        self.gr_txtb_id.configure(state="disabled")
        self.gr_combobox_groups.configure(state="disabled")
        self.gr_textbox_users.configure(state="normal")
        self.gr_textbox_users.delete("0.0", customtkinter.END)
        self.gr_txtb_nr.delete(0, customtkinter.END)
        self.gr_txtb_descr.delete(0, customtkinter.END)
        self.gr_textbox_users.configure(state="disabled")
        self.six_frame_button_edit.configure(state="normal", text="Speichern", command=self.transmit_group)
        self.six_frame_button_del.configure(state="normal", text="Abbrechen", command=self.new_group_cancel)
        self.six_frame_button_new.grid_forget()

    def transmit_group(self):
        """
        Usergruppe erstellen - DB eintragen
        :return:
        """
        ug = UserGroup()
        feedback = ug.create_group(self.gr_txtb_nr.get(), self.gr_txtb_descr.get())
        print(feedback)
        # Setze alles zum ursprung
        if feedback:
            messagebox.showinfo("Erfolgreich!", "Gruppe wurde erfolgreich angelegt!")
            self.new_group_cancel()
            self.frame_6_button_event()
        else:
            messagebox.showerror("Fehler", "GruppenNr ist bereits in verwendung! Bitte andere wählen.")

    def new_group_cancel(self):
        """
        Neue Gruppe anlegen - Abbrechen
        :return:
        """
        self.gr_txtb_nr.delete(0, customtkinter.END)
        self.gr_txtb_descr.delete(0, customtkinter.END)
        self.gr_textbox_users.delete(0, customtkinter.END)
        self.gr_txtb_id.delete(0, customtkinter.END)

        self.six_frame_button_new.grid(row=0, column=2, padx=(0, 0), sticky="ne", columnspan=1)
        self.six_frame_button_edit.configure(state="disabled", text="Speichern")
        self.six_frame_button_del.configure(state="disabled", text="Gruppe löschen",
                                            command=lambda: self.del_group(self.gr_txtb_nr.get()))
        self.gr_txtb_id.configure(state="normal")
        self.gr_combobox_groups.configure(state="normal")
        self.gr_txtb_id.delete(0, customtkinter.END)
        self.gr_txtb_id.configure(placeholder_text="Wähle eine Gruppe")

    def del_user(self, data):
        """
        user löschen
        :param data:
        :return:
        """
        u = Users(self.txtb_UID.get())
        u.del_user(self.txtb_id.get())
        self.combobox_users.set(data[0])
        self.combobox_callback_users(self.combobox_users.get())

    def edit_user(self):
        """
        User bearbeiten in der DB speichern
        :return:
        """
        uid = self.txtb_UID.get()
        state = self.five_frame_button_edit.cget("text")

        u = Users(uid)

        if (state == "Benutzer bearbeiten"):
            print(uid)
            ## Buttons ändern
            self.five_frame_button_edit.configure(text="Speichern")
            self.five_frame_button_del.configure(state="disabled", fg_color="gray30")

            ## Sperre der Felder entfernen
            self.combobox_users.configure(state="disabled")
            self.txtb_Name.configure(state="normal")
            self.txtb_lang.configure(state="normal")
            self.txtb_location.configure(state="normal")
            self.txtb_group.configure(state="normal")
            self.txtb_wartungstypen.configure(state="normal")

        else:
            ## Setze alles auf disable
            self.combobox_users.configure(state="normal")
            self.txtb_Name.configure(state="disabled")
            self.txtb_lang.configure(state="disabled")
            self.txtb_location.configure(state="disabled")
            self.txtb_group.configure(state="disabled")
            self.txtb_wartungstypen.configure(state="disabled")

            ## Aktionen
            data = [None] * 8                           # Plätze im Array zur Übermittlung aller Infos
            data[0] = int(self.txtb_id.get())
            data[1] = self.txtb_Name.get()
            data[2] = self.txtb_lang.get()
            data[3] = None  # self.txtb_warnings.get()
            substring_gnr = self.txtb_group.get().split(":", 1)[0]
            data[4] = substring_gnr
            data[5] = self.txtb_wartungstypen.get()
            data[6] = self.txtb_location.get()

            u.edit_user(data)

            ## Buttons ändern
            self.five_frame_button_edit.configure(text="Benutzer bearbeiten")
            self.five_frame_button_del.configure(state="normal", fg_color="#E64422")

            ## reload
            self.combobox_callback_users(self.combobox_users.get())

    def combobox_callback_users(self, choice):
        """
        Aktion für einen neue USER auswählen. UI wird geleert und neu befüllt
        :param choice:
        :return:
        """
        ## Setze alles auf enable
        self.txtb_id.configure(state="normal")
        self.txtb_Name.configure(state="normal")
        self.txtb_ChatID.configure(state="normal")
        self.txtb_UID.configure(state="normal")
        self.txtb_lang.configure(state="normal")
        self.txtb_group.configure(state="normal")
        self.five_frame_button_del.configure(state="normal")
        self.five_frame_button_edit.configure(state="normal")
        self.txtb_wartungstypen.configure(state="normal")
        self.txtb_location.configure(state="normal")

        self.txtb_id.delete(0, customtkinter.END)
        self.txtb_Name.delete(0, customtkinter.END)
        self.txtb_ChatID.delete(0, customtkinter.END)
        self.txtb_UID.delete(0, customtkinter.END)
        self.txtb_lang.delete(0, customtkinter.END)
        self.txtb_location.delete(0, customtkinter.END)
        self.txtb_wartungstypen.delete(0, customtkinter.END)

        # self.txtb_group.delete(0, customtkinter.END)

        ## Daten aus der DB einlesen
        substring = choice.split(":", 1)[0]
        results = Database.get_query("users", "ID=" + str(substring))
        result = results[0]

        ## Daten einfügen
        self.txtb_id.insert(0, str(result[0]))
        self.txtb_Name.insert(0, str(result[2]))
        self.txtb_ChatID.insert(0, str(result[5]))
        self.txtb_UID.insert(0, str(result[1]))
        self.txtb_lang.insert(0, str(result[3]))
        self.txtb_wartungstypen.insert(0, str(result[4]))
        self.txtb_location.insert(0, str(result[7]))
        self.txtb_group.set(str(result[6]))

        ## Setze alles auf disable
        self.txtb_id.configure(state="disabled")
        self.txtb_Name.configure(state="disabled")
        self.txtb_ChatID.configure(state="disabled")
        self.txtb_UID.configure(state="disabled")
        self.txtb_lang.configure(state="disabled")
        self.txtb_group.configure(state="disabled")
        self.txtb_wartungstypen.configure(state="disabled")
        self.txtb_location.configure(state="disabled")
        # print(results)

    def combobox_callback_warnings(self, choice, ver=None):
        """
        WARNMELDUNGEN
        Funktion um die Userform zu füllen, mit den Informationen der aktuellen Meldung!
        :param choice:
        :return:
        """
        # Definiere einen Regex, um den Text innerhalb der letzten Klammern zu finden
        regex = r"\(([^()]+)\)[^()]*$"

        # Suchen des Regex innerhalb des Textes
        match = re.search(regex, choice)

        # Überprüfen, ob ein Treffer gefunden wurde
        if match:
            # Extrahiere den Text aus dem Treffer
            text_in_klammern = match.group(1)

        versionen = []
        if ver == None:
            val = Database.get_query("warning_information", "wid = '{}'".format(text_in_klammern))

            for i in val:
                versionen.append(str(i[2]))
        else:
            val = Database.get_query("warning_information", "wid = '{}' AND version={}".format(text_in_klammern, ver))
            versionen = self.combobox_version.cget("values")

        print(versionen)

        # Reset der Elemente auf Werkeinstellung
        # Bilder auf Platzhalter und Texte leeren
        self.second_codeiiimg.configure(
            light_image=Image.open(os.path.join("Test/test_images/platzhalter.png")).resize((256, 256)),
            dark_image=Image.open(os.path.join("Test/test_images/platzhalter.png")).resize((256, 256)))
        self.second_img.configure(
            light_image=Image.open(os.path.join("Test/test_images/platzhalter.png")).resize((256, 256)),
            dark_image=Image.open(os.path.join("Test/test_images/platzhalter.png")).resize((256, 256)))

        self.second_desc.delete("0.0", customtkinter.END)
        self.second_title.delete(0, customtkinter.END)
        self.second_desc.insert("0.0", val[0][9])
        self.second_title.insert(0, val[0][8])
        if val[0][7] == "":
            self.img_description.configure(text="n/A")
        else:
            self.img_description.configure(text=val[0][7])

        self.second_label_Type.configure(text="Type: " + val[0][5])
        self.second_label_Scope.configure(text="Scope: " + val[0][6])
        self.second_label_Web.configure(text="Web: " + val[0][10])
        self.second_label_Effectiv.configure(
            text="Effective: " + val[0][18] + "\t Onset: " + val[0][19] + "\t Expires: " + val[0][20])

        # Check, ob eine URL hinterlegt wurde.
        if str(val[0][13]) != "":
            self.second_img.configure(light_image=self.pull_img_url(str(val[0][13])),
                                      dark_image=self.pull_img_url(str(val[0][13])))

        if str(val[0][12]) != "":
            self.second_codeiiimg.configure(light_image=self.pull_img_url(str(val[0][12])),
                                            dark_image=self.pull_img_url(str(val[0][12])))

        self.second_codeImglabel.configure(text="Event: " + val[0][14])
        self.second_frame_button_goto.configure(
            command=lambda: self.call_edit_warning(val[0][1], self.combobox_version.get()))
        self.combobox_version.configure(values=versionen)
        if ver is None:
            self.combobox_version.set(versionen[0])
        else:
            self.combobox_version.set(ver)

    def call_edit_warning(self, wid, ver):
        """
        Warnmeldung bearbeiten und in der Userform aufrufen.
        :param wid:
        :param ver:
        :return:
        """
        db = Database()
        results = db.get_query("warning_information", "wid='{}' AND version={}".format(wid, ver))
        result = results[0]
        self.clear_frame_3()

        self.third_frame_ID.insert(0, str(result[1]))
        self.third_frame_event.insert(0, str(result[14]))
        self.third_frame_expires.insert(0, str(result[20]))
        self.third_frame_effective.insert(0, str(result[18]))
        self.third_frame_Title.insert(0, str(result[8]))
        self.third_frame_desc.insert("0.0", str(result[9]))
        self.third_frame_instuc.insert("0.0", str(result[21]))
        self.third_frame_img.insert(0, str(result[13]))
        self.third_frame_imgc.insert(0, str(result[12]))
        self.third_frame_web.insert(0, str(result[10]))
        self.third_frame_Sender.insert(0, str(result[7]))
        self.third_frame_Status.insert(0, str(result[4]))
        self.third_frame_area.insert(0, str(result[11]))
        self.third_frame_urgancy.set(str(result[15]))
        self.third_frame_severity.set(str(result[16]))
        self.third_frame_certainty.set(str(result[17]))

        self.third_frame_tmpVar.configure(text=ver)

        self.third_frame_ID.configure(state="disabled")

        self.select_frame_by_name("frame_3")  # Öffne das Frame "Warnmeldung erstellen"

    def clear_frame_3(self):
        """
        Leere Userform 3
        :return:
        """
        self.third_frame_ID.configure(state="normal")
        
        self.third_frame_ID.delete(0, customtkinter.END)
        self.third_frame_event.delete(0, customtkinter.END)
        self.third_frame_expires.delete(0, customtkinter.END)
        self.third_frame_effective.delete(0, customtkinter.END)
        self.third_frame_Title.delete(0, customtkinter.END)
        self.third_frame_desc.delete("0.0", customtkinter.END)
        self.third_frame_instuc.delete("0.0", customtkinter.END)
        self.third_frame_img.delete(0, customtkinter.END)
        self.third_frame_imgc.delete(0, customtkinter.END)
        self.third_frame_web.delete(0, customtkinter.END)
        self.third_frame_Sender.delete(0, customtkinter.END)
        self.third_frame_Status.delete(0, customtkinter.END)
        self.third_frame_area.delete(0, customtkinter.END)

        self.third_frame_img.configure(placeholder_text="URL zum Bild")
        self.third_frame_imgc.configure(placeholder_text="URL zum Bild")
        self.third_frame_web.configure(placeholder_text="URL zur Webseite")
        self.third_frame_Sender.configure(placeholder_text="Name des Senders")
        self.third_frame_Status.configure(placeholder_text="Actual")
        self.third_frame_area.configure(placeholder_text="Stadt Darmstadt, ....")


    def save_new_warning(self, cancel_wid=None):
        """
        Speicher die neue Warnung in der DB ab.
        :param cancel_wid: Ob die Meldung deaktiviert wurde
        :return:
        """
        status = self.third_frame_ID.cget(
            "state")  # Rufe den Status ab von WID. Wenn disabled, dann updaten und sonst neu erstellen
        # Rufe alle Variablen ab
        var_wid = self.third_frame_ID.get()
        var_event = self.third_frame_event.get()
        var_expires = self.third_frame_expires.get()
        var_effective = self.third_frame_effective.get()
        var_title = self.third_frame_Title.get()
        var_descr = self.third_frame_desc.get("0.0", customtkinter.END)
        var_instruction = self.third_frame_instuc.get("0.0", customtkinter.END)
        var_img = self.third_frame_img.get()
        var_imgc = self.third_frame_imgc.get()
        var_web = self.third_frame_web.get()
        var_sender = self.third_frame_Sender.get()
        var_status = self.third_frame_Status.get()
        var_area = self.third_frame_area.get()
        var_urgancy = self.third_frame_urgancy.get()
        var_severity = self.third_frame_severity.get()
        var_certainty = self.third_frame_certainty.get()
        var_version = self.third_frame_tmpVar.cget("text")
        var_currentDateTime = str(datetime.datetime.now())[0:19]

        if cancel_wid:
            query = "UPDATE warnings SET type = 'Cancel', version={}, last_update='{}' WHERE wid='{}'".format(
                int(var_version) + 1, var_currentDateTime, var_wid)
            Database.execute_db(query, self.config_db['PATH'])

            query = "INSERT INTO warning_information (wid,version,sender,status,msgType,scope,senderName,headline," \
                    "text,web,areaDesc,codeIMG,image,event,urgency,severity,certainty,DateEffective,DateOnset," \
                    "DateExpires,instruction) VALUES(" \
                    "'{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                    "'{}','{}')".format(var_wid, int(var_version) + 1, "Custom", var_status, "Cancel", "Public",
                                        var_sender, var_title,
                                        var_descr, var_web, var_area, var_imgc, var_img, var_event, var_urgancy,
                                        var_severity, var_certainty, var_effective, var_currentDateTime, var_expires,
                                        var_instruction)
            Database.execute_db(query, self.config_db['PATH'])

            messagebox.showwarning("STATUS: Cancel", "Warnmeldung wurde aufgehoben!")
            self.clear_frame_3()
            simulate_choice = str(var_currentDateTime) + ": " + var_title + " (" + var_wid + ")"
            self.combobox_callback_warnings(simulate_choice, int(var_version) + 1)
            self.frame_2_button_event()
        elif status == "normal":

            query = "INSERT INTO warning_information (wid,version,sender,status,msgType,scope,senderName,headline," \
                    "text,web,areaDesc,codeIMG,image,event,urgency,severity,certainty,DateEffective,DateOnset," \
                    "DateExpires,instruction) VALUES(" \
                    "'{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                    "'{}','{}')".format(var_wid, 1, "Custom", var_status, "Alert", "Public", var_sender, var_title,
                                        var_descr, var_web, var_area, var_imgc, var_img, var_event, var_urgancy,
                                        var_severity, var_certainty, var_effective, var_currentDateTime, var_expires,
                                        var_instruction)
            success = Database.execute_db(query, self.config_db['PATH'])

            query = "INSERT INTO warnings (wid,title_de,title_en,version,severity,type,source,descr,last_update)" \
                    "VALUES ('{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(var_wid, var_title, "None", 1,
                                                                                 var_severity,
                                                                                 "Alert", "custom", var_descr,
                                                                                 var_currentDateTime)
            Database.execute_db(query, self.config_db['PATH'])
            if success:
                messagebox.showinfo("Erfolgeich!", "Warnmeldung wurde erfolgreich angelegt. WID: " + var_wid)
                self.clear_frame_3()

        elif status == "disabled":
            query = "INSERT INTO warning_information (wid,version,sender,status,msgType,scope,senderName,headline," \
                    "text,web,areaDesc,codeIMG,image,event,urgency,severity,certainty,DateEffective,DateOnset," \
                    "DateExpires,instruction) VALUES(" \
                    "'{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                    "'{}','{}')".format(var_wid, int(var_version) + 1, "Custom", var_status, "Update", "Public",
                                        var_sender, var_title,
                                        var_descr, var_web, var_area, var_imgc, var_img, var_event, var_urgancy,
                                        var_severity, var_certainty, var_effective, var_currentDateTime, var_expires,
                                        var_instruction)
            success = Database.execute_db(query, self.config_db['PATH'])
        else:
            messagebox.showerror("Fehler",
                                 "Status kann nicht ermittelt werden! Sie müssen den Vorgang neu durchführen.")

    def pull_img_url(self, url):
        """
        Rufe die Bilder aus der Warnmeldung ab.
        :param url:
        :return:
        """
        if url == 'None':
            return Image.open(os.path.join("Test/test_images/platzhalter.png")).resize((256, 256))

        response = urllib.request.urlopen(url)
        img_data = response.read()

        # Create a PIL Image object from the image data
        pil_image = Image.open(io.BytesIO(img_data))
        pil_image = pil_image.resize((256, 256))
        return pil_image

    def open_input_dialog_event(self):
        """
        Dialogbox -> ENTWURF
        :return:
        """
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Ändert den Darstellungsmodus
        :param new_appearance_mode:
        :return:
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        """
        Ändert die Auflösung (Zoom)
        :param new_scaling:
        :return:
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        """
        TEST Botton
        :return:
        """
        prev = self.home_textbox_updates.get("0.0", "end")
        print(len(prev))
        print(self.home_textbox_updates.get("0.0", "end"))
        self.insert_update("Test")

    def insert_update(self, text: str):
        """
        Fügt Updates in die Textbox auf der Startseite ein.
        :param text:
        :return:
        """
        # self.textbox.delete("0.0", "end")  # delete all text
        # self.textbox.delete("0.0", "end")
        self.home_textbox_updates.configure(state="normal")
        # self.textbox_updates.insert(customtkinter.END, text + "\n")
        self.home_textbox_updates.insert("0.0", text + "\n")
        self.home_textbox_updates.configure(state="disabled")

    def insert_send_msg(self, text: str):
        """
        Fügt die ankommenden Nachrichten in die textbox_sendmsg auf dem Home-Bildschirm
        :param text:
        :return:
        """
        self.home_textbox_sendmsg.configure(state="normal")
        self.home_textbox_sendmsg.insert("0.0", text + "\n")
        self.home_textbox_sendmsg.configure(state="disabled")

    def replace_tags(self, text):
        """
        Ersetzt die Zeichenfolge im text, die von Telegram nicht erkannt werden
        :param text:
        :return: string
        """
        # Ersetze <br/> durch \n
        text = text.replace('\\', '')
        text = text.replace("<br/>", "\n")

        # Ersetze <i> durch *
        text = text.replace("<p>", "\n\n")

        # Ersetze li
        text = text.replace("<li>", "-")
        text = text.replace("</li>", "\n")
        # Lösche
        text = text.replace("</p>", "")
        text = text.replace("</ul>", "")
        text = text.replace("<ul>", "")

        return text

    def send_warning(self):
        """
        Funktion für das Testen wärend der Entwicklungsphase.
        :return:
        """
        regex = r"\(([^()]+)\)[^()]*$"

        # Suchen des Regex innerhalb des Textes
        match = re.search(regex, self.combobox_warnungen.get())

        # Überprüfen, ob ein Treffer gefunden wurde
        if match:
            # Extrahiere den Text aus dem Treffer
            text_in_klammern = match.group(1)
        wid = text_in_klammern
        user = ""           # ChatID hinterlegen
        tb = telegram_api.TelegramBot(self.config_telegram['KEY'], self)
        tb.send_warnings(wid, "", user)

    def send_all_fnc(self):
        """
        Sendet Nachrichten an ALLE Nutzer vom Bot
        Kann auf bestimmte Nutzer limitiert werden.
        :return:
        """
        txt = self.home_entry.get()
        print(str(txt))
        txt = self.replace_tags(txt)
        tb = telegram_api.TelegramBot(self.config_telegram['KEY'], self)
        tb.send_multiple_message(txt)

        self.home_entry.delete(0, len(txt))

    def get_dbInfo(self):
        global var_info
        conn = sqlite3.connect(self.config_db['PATH'])
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM warnings")
        warnings = c.fetchone()[0]
        c.execute("SELECT COUNT(Distinct(wid)) FROM warnings")
        warnings2 = c.fetchone()[0]
        c.execute("SELECT COUNT(Distinct(wid)) FROM warnings WHERE wid like '%custom%'")
        warnings3 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM warnings")
        warnings = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users")
        count2 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM user_groups")
        count3 = c.fetchone()[0]
        self.home_label_dbInfo.configure(
            text="STATISTIK\n \nAnzahl User:\t" + str(count2) + "\n\nAnzahl Warnings:\t" + str(warnings) +
                 "\n      Alerts:\t\t" + str(warnings2) +
                 "\n      Updates:\t" + str(warnings - warnings2) +
                 "\n      Custom:\t" + str(warnings3) +
                 "\n\nAnzahl Gruppen:\t" + str(count3))

        # threading.Timer(10, self.get_dbInfo).start()
        # self.home_label = customtkinter.CTkLabel(self.home_frame, anchor="ne", justify="left", text="Anzahl User: " + str(count2) + "\nAnzahl Warnings: " + str(count))


# if __name__ == "__main__":
# def start(self):
#    app = App()
#    app.mainloop()

"""if __name__ == "__main__":
    app = App("BOT_KEY")
    app.mainloop()"""
