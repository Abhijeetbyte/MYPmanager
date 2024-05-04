import customtkinter
import pandas as pd
import os
from tkinter import StringVar
import tkinter.messagebox

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
       
        # configure window
        self.title("MYP manager")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create side frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # create welcome frame
        self.welcome_frame = customtkinter.CTkFrame(self)
        self.welcome_frame.grid(row=1, column=1, sticky="ns")
        self.welcome_label = customtkinter.CTkLabel(self.welcome_frame,  justify="left", text="\n Welcome ! \n\n THIS APPLICATION USES A MASTER PASSWORD\
                    \n TO ENCRYPT & DECRYPT YOUR DATA.\
                    \n USE ANY ALPHANUMERIC PASSWORD (RECOMMENDED)\
                    \n AND REMEMBER THAT.\
                    \n\n WARNING: IF YOU LOSE YOUR MASTER PASSWORD, THEN YOU\
                    \n WILL NOT BE ABLE TO RECOVER YOUR SAVED PASSWORDS.\
                    \n\n VISIT: https://github.com/Abhijeetbyte/MYPmanager", font=customtkinter.CTkFont(size=14))
        self.welcome_label.grid(row=0, column=0, padx=(20,0), pady=(20, 30))
        self.welcome_button = customtkinter.CTkButton(self.welcome_frame, text="Next", command=self.welcome_button_event, width=200)
        self.welcome_button.grid(row=3, column=0, padx=30, pady=(15, 15))
    
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.grid(row=1, column=1, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="MYP manager\n\n",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=150, pady=(50, 100))
        self.password_entry = customtkinter.CTkEntry(master=self.login_frame, width=300,height=40,border_width=1, show="*", placeholder_text="Master Password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_label2 = customtkinter.CTkLabel(self.login_frame, text="( Must have a minimum of 8 characters )")
        self.login_label2.grid(row=3, column=0, padx=20, pady=(5, 5))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Submit", command=self.login_button_event, width=200)
        self.login_button.grid(row=4, column=0, padx=30, pady=(30, 30))
        

        # create sidebar frame with widgets and buttons
        self.sidebar_button_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_button_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_button_frame, text="Select Option: ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_button_frame, text="Add New", command=self.add_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_button_frame,text="Search", command=self.search_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_button_frame, text="Edit", command=self.edit_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_button_frame, text="Delete", command=self.delete_button_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_button_frame, text="Back", command=self.back_button_event)
        self.sidebar_button_4.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_button_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_button_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        
        # create main entry and button
        self.entry_frame = customtkinter.CTkFrame(self,width=250)
        self.entry_frame.grid(row=0, column=1,padx=(20,0),pady=(20,0), sticky="nsew")
        
        self.entry_label = customtkinter.CTkLabel(self.entry_frame, text="Enter your credentials: ", font=customtkinter.CTkFont(size=14))
        self.entry_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.entry_name = customtkinter.CTkEntry(master=self.entry_frame,width=350,height=40,border_width=1, placeholder_text="Enter App Name/ URL")
        self.entry_name.grid(row=1, column=0, padx=20, pady=(5, 5))
        
        self.entry_uname = customtkinter.CTkEntry(master=self.entry_frame, width=350,height=40,border_width=1,placeholder_text="Enter Username")
        self.entry_uname.grid(row=2, column=0,  padx=20, pady=(5, 5))
        
        self.entry_password = customtkinter.CTkEntry(master=self.entry_frame,width=350,height=40,border_width=1, show="*", placeholder_text="Enter Password")
        self.entry_password.grid(row=3, column=0,  padx=20, pady=(5, 5))
        
        self.entry_button_1 = customtkinter.CTkButton(self.entry_frame, text="Submit", command=self.entry_button_event)
        self.entry_button_1.grid(row=4, column=0, padx=30, pady=(10, 10))



##        # create tabview
##        self.tabview = customtkinter.CTkTabview(self, width=250)
##        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
##        self.tabview.add("CTkTabview")
##        self.tabview.add("Tab 2")
##        self.tabview.add("Tab 3")
##        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
##        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
##
##        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
##                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
##        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
##        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
##                                                    values=["Value 1", "Value 2", "Value Long....."])
##        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
##        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
##                                                           command=self.open_input_dialog_event)
##        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
##        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
##        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)


        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")




        data_file = os.path.isfile('data.csv')  # check whether data file is there or not
        if not data_file:  # if csv not found
            self.create_csv()  # call function and create csv
            # Initially show only the welcome frame
            print("Welcome \n")
            self.login_frame.grid_forget()
            self.sidebar_button_frame.grid_forget()
            self.main_button_1.grid_forget()
            self.entry.grid_forget()
            self.textbox.grid_forget()

        else :
            # Initially show only the login frame
            print("Login \n")
            self.login_frame.grid(row=1, column=1, sticky="ns")  # show login frame
            self.welcome_frame.grid_forget()
            self.sidebar_button_frame.grid_forget()
            self.entry_frame.grid_forget()
            self.textbox.grid_forget()
            
            

        # set default values
        self.appearance_mode_optionemenu.set("Light")
        #self.optionmenu_1.set("CTkOptionmenu")
        #self.combobox_1.set("CTkComboBox")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        

    def welcome_button_event(self):
         print("Next button pressed\n") 
         self.welcome_frame.grid_forget() # forget frame
         self.sidebar_button_frame.grid_forget()
         self.entry.grid_forget()
         self.textbox.grid_forget()
         self.login_frame.grid(row=1, column=1, sticky="ns")  # show login frame
   

         
    def create_csv(self):
        data = {'Url/App name': [], 'Username': [], 'Password': []}  # empty value dict
        df = pd.DataFrame(data)  # create new pandas DataFrame
        df.to_csv('data.csv', index=False)  # Write DataFrame to a new CSV file

        print("CSV created\n")
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        print("Appearance changed :" , new_appearance_mode)
        customtkinter.set_appearance_mode(new_appearance_mode)



    def login_button_event(self):
        masterpasswordVariable = self.password_entry.get()
        print(masterpasswordVariable,"\n")
        print("Login button pressed\n")
        self.login_frame.grid_forget()  # remove login frame
        self.sidebar_button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")# show frame
        self.entry_frame.grid(row=0, column=1,padx=(20,0),pady=(20,0), sticky="nsew")
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
       
   
    def back_button_event(self):
        print("Back button pressed \n")
        self.welcome_frame.grid_forget()# forget frame
        self.sidebar_button_frame.grid_forget()
        self.entry_frame.grid_forget()
        self.textbox.grid_forget()
        self.login_frame.grid(row=1, column=1, sticky="ns")  # show login frame

        
    def add_button_event(self):
        print("Add button pressed\n")
        
    def search_button_event(self):
        print("Search button pressed\n")
        
    def edit_button_event(self):
        print("Edit button pressed\n")

    def delete_button_event(self):
        print("Delete button pressed\n")

    def entry_button_event(self):
        print("Entry button pressed\n")
        nameVariable = self.entry_name.get()
        unameVariable = self.entry_uname.get()
        passwordVariable = self.entry_password.get()
        print(nameVariable,',',unameVariable,',', passwordVariable)
        
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
