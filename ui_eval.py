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
from db_functions import Database
import telegram_api
import configparser
import UI


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app  # save reference to the App instance
        self.db = Database
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.config_telegram = config["TelegramAPI"]
        self.geometry("900x500")
        self.title("Warnmeldungen Evaluieren - Bachelorthesis Marco Matissek")
        # self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # LOGO
        self.headline = customtkinter.CTkLabel(master=self, text="Evaluation",
                                               font=("Arial", 30),
                                               text_color="#4a97cf")
        self.headline.grid(row=0, column=0, padx=20, pady=(20, 20), columnspan=4, sticky="nesw")

        # TODO: Userform erstellen
        # TODO: Senden an einzelpersonen und an Gruppen -> Auswahl über ein Dropdown und Radio-Buttons
        # TODO: Warnmeldung auswählen und noch verändern können
        # TODO: Custom Text senden
        # TODO: Anrede auswählen können
        # TODO: ...

        # Inputs
        ## Variablen
        self.radio_sendto = tkinter.IntVar(0)
        self.radio_anrede = tkinter.IntVar(0)
        self.radio_msg = tkinter.IntVar(0)
        self.check_var = tkinter.StringVar(value="on")

        ### Sektion 1: Senden an
        self.lbl_empf = customtkinter.CTkLabel(self, text="Empfänger", fg_color="#A5A4A5", text_color="white")
        self.lbl_empf.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nesw", columnspan=3)

        self.lbl_sendenan = customtkinter.CTkLabel(self, text="Senden an...")
        self.lbl_sendenan.grid(row=2, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.radiobutton_1 = customtkinter.CTkRadioButton(master=self, text="Einzelperson",
                                                          command=self.radiobutton_sendto_event,
                                                          variable=self.radio_sendto,
                                                          value=1)
        self.radiobutton_1.grid(row=2, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.radiobutton_2 = customtkinter.CTkRadioButton(master=self, text="Gruppe",
                                                          command=self.radiobutton_sendto_event,
                                                          variable=self.radio_sendto,
                                                          value=2)
        self.radiobutton_2.grid(row=2, column=2, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)

        self.cb_users = customtkinter.CTkComboBox(master=self,
                                                  values=['Wähle eine Option'],
                                                  width=250, state="disabled")
        self.cb_users.grid(row=3, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=2)

        ### Sektion 2: Anrede (Persönlichkeit des Bots)
        self.lbl_anrede = customtkinter.CTkLabel(self, text="Persönlichkeit (Anrede)", fg_color="#A5A4A5",
                                                 text_color="white")
        self.lbl_anrede.grid(row=4, column=0, padx=(20, 0), pady=(20, 0), sticky="nesw", columnspan=3)
        self.lbl_sendenan = customtkinter.CTkLabel(self, text="Wähle:")
        self.lbl_sendenan.grid(row=5, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.radiobutton_3 = customtkinter.CTkRadioButton(master=self,
                                                          text="Persönlich (Username) \n(z.B.: Hallo ***,)",
                                                          command=self.radio_anrede_event,
                                                          variable=self.radio_anrede,
                                                          value=1)
        self.radiobutton_3.grid(row=5, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.radiobutton_4 = customtkinter.CTkRadioButton(master=self, text="Allgemein (Anrede vermeiden)",
                                                          command=self.radio_anrede_event,
                                                          variable=self.radio_anrede,
                                                          value=2)
        self.radiobutton_4.grid(row=5, column=2, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)

        ### Sektion 3: Warnmeldung
        # TODO: Aktivieren, ansonsten nur Plaintext senden
        self.lbl_sendmsg = customtkinter.CTkLabel(self, text="Warnmeldung", fg_color="#A5A4A5",
                                                  text_color="white")
        self.lbl_sendmsg.grid(row=6, column=0, padx=(20, 0), pady=(20, 0), sticky="nesw", columnspan=3)
        self.lbl_waehlen = customtkinter.CTkLabel(self, text="Wähle:")
        self.lbl_waehlen.grid(row=7, column=0, padx=(20, 0), pady=(0, 0), sticky="nw")
        self.radiobutton_5 = customtkinter.CTkRadioButton(master=self, text="Warnmeldung",
                                                          command=self.radiobutton_msg_event,
                                                          variable=self.radio_msg,
                                                          value=1)
        self.radiobutton_5.grid(row=7, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        self.radiobutton_6 = customtkinter.CTkRadioButton(master=self, text="Textnachricht",
                                                          command=self.radiobutton_msg_event,
                                                          variable=self.radio_msg,
                                                          value=2)
        self.radiobutton_6.grid(row=7, column=2, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        # Entry
        self.txtb_msg = customtkinter.CTkEntry(master=self,
                                               placeholder_text="Schreibe eine Nachricht...", height=25,
                                               width=500, border_width=2, corner_radius=10)
        self.txtb_msg.grid(row=8, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=3)

        # Warnmeldung
        cat = Database.get_query("warning_information")
        arr_cat = []
        for c in cat:
            current_str = str(c[1].split(".")[0])
            if arr_cat.count(current_str) == 0:
                arr_cat.append(str(c[1].split(".")[0]))

        self.cb_filter = customtkinter.CTkComboBox(master=self,
                                                   values=arr_cat,
                                                   width=150, state="normal",
                                                   command=self.cb_filter_event)
        self.cb_filter.grid(row=8, column=0, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=1)

        self.cb_warnmeldung = customtkinter.CTkComboBox(master=self,
                                                        values=['Wähle eine Option'],
                                                        width=500, state="disabled")
        self.cb_warnmeldung.grid(row=8, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=2)

        self.btn_edit = customtkinter.CTkButton(master=self, fg_color="transparent",
                                                border_width=2,
                                                text_color=("gray10", "#DCE4EE"),
                                                command=lambda: app.call_edit_warning(
                                                    self.cb_warnmeldung.get().split(":")[0],
                                                    self.cb_warnmeldung.get().split("Version:")[1]),
                                                text="Bearbeiten")
        self.btn_edit.grid(row=10, column=2, padx=(20, 0), pady=(20, 20), sticky="nw")

        self.checkbox = customtkinter.CTkCheckBox(master=self, text="Neuste Version", command=self.checkbox_event,
                                                  variable=self.check_var, onvalue="on", offvalue="off")
        self.checkbox.grid(row=9, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=1)
        ### Sektion 4: Buttons
        self.btn_send = customtkinter.CTkButton(master=self, fg_color="transparent",
                                                border_width=2,
                                                text_color=("gray10", "#DCE4EE"),
                                                command=self.send_warning,
                                                text="Senden")
        self.btn_send.grid(row=10, column=2, padx=(20, 0), pady=(20, 20), sticky="se")

        # Init
        self.radiobutton_1.select()
        self.radiobutton_1.invoke()

        self.radiobutton_4.select()
        self.radiobutton_4.invoke()

        self.radiobutton_5.select()
        self.radiobutton_5.invoke()

    def radio_anrede_event(self):
        pass
        # print(self.radio_anrede.get())

    def checkbox_event(self):
        pass
        # print("checkbox toggled, current value:", self.check_var.get())

    def cb_filter_event(self, choice):
        results = Database.get_query("warning_information", "wid like '{}%'".format(choice))
        arr = []
        for result in results:
            arr.append(str(result[1]) + ": " + str(result[8]) + "| Version: " + str(result[2]))

        self.cb_warnmeldung.configure(values=arr, state="normal")

    def radiobutton_sendto_event(self):
        self.cb_users.configure(state="normal")

        if (self.radio_sendto.get() == 1):
            results = Database.get_query("users")
            ar = []
            for result in results:
                ar.append(str(result[1]) + ": " + str(result[2]) + " (" + str(result[5]) + ")")
        elif (self.radio_sendto.get() == 2):
            results = Database.get_query("user_groups")
            ar = []
            for result in results:
                ar.append(str(result[0]) + ": " + str(result[2]) + " (Nr: " + str(result[1]) + ")")
        else:
            ar = ["Error 404"]
            self.cb_users.configure(state="disabled")

        self.cb_users.configure(values=ar)
        # print("radiobutton toggled, current value:", self.radio_sendto.get())

    def radiobutton_msg_event(self):
        var_selected = self.radio_msg.get()

        if var_selected == 1:
            """
                Warnmeldung
            """
            self.cb_warnmeldung.configure(state="normal")
            self.txtb_msg.configure(state="disabled")
            self.btn_edit.grid(row=9, column=2, padx=(20, 0), pady=(20, 20), sticky="nw")
            self.cb_warnmeldung.grid(row=8, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=2)
            self.cb_filter.grid(row=8, column=0, padx=(20, 0), pady=(0, 0), sticky="nw", columnspan=1)
            self.txtb_msg.grid_forget()

            results = Database.get_query("warning_information")
            arr = []
            for result in results:
                arr.append(str(result[1]) + ": " + str(result[8]) + "| Version: " + str(result[2]))

            self.cb_warnmeldung.configure(values=arr, state="normal")

        elif var_selected == 2:
            """
                Textnachricht
            """
            self.txtb_msg.configure(state="normal")
            self.btn_edit.grid_forget()
            self.cb_warnmeldung.grid_forget()
            self.cb_filter.grid_forget()
            self.cb_warnmeldung.configure(state="disabled")
            self.txtb_msg.grid(row=8, column=1, padx=(20, 0), pady=(5, 0), sticky="nw", columnspan=2)
        else:
            self.txtb_msg.configure(state="disabled")
            self.cb_warnmeldung.configure(state="disabled")
            print("Error: MSG-Type unbekannt. Funktion: radiobutton_msg_event")

    def send_warning(self):
        user = []

        if self.radio_sendto.get() == 1:
            str_usn = self.cb_users.get().split(": ")[1]
            username = str_usn.split("(")[0]

            user.append((username[0:-1], str_usn.split("(")[1][0:-1]))
        elif self.radio_sendto.get() == 2:
            group = self.cb_users.get().split(":")[0]
            # group = group[0:-1]

            result = Database.get_query("users", "group_id={}".format(group))
            for res in result:
                user.append((res[2], str(res[5])))

        else:
            print("Error: Person/Gruppe nicht erkannt.")

        # print(user)

        tb = telegram_api.TelegramBot(self.config_telegram["KEY"], self)
        for u in user:

            if self.radio_anrede.get() == 2:  # Anrede vermeiden
                personal_anrede = None
            elif self.radio_anrede.get() == 1:  # Persönliche Anrede
                personal_anrede = u[0]
            else:
                personal_anrede = None  # Anrede vermeiden, wenn nichts gesetzt wurde

            # print(u[1])
            if self.txtb_msg.cget("state") == "normal":
                tb.send_message(u[1], self.txtb_msg.get())

            elif self.cb_warnmeldung.cget("state") == "normal":
                # print(personal_anrede)
                if self.checkbox.get() == "on":
                    tb.send_warnings(self.cb_warnmeldung.get().split(":")[0], "", u[1], personal_anrede)
                else:
                    tb.send_warnings(self.cb_warnmeldung.get().split(":")[0],
                                     self.cb_warnmeldung.get().split("Version: ")[1], u[1], personal_anrede)
