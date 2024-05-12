import pandas as pd
import os
import string
import tabulate # pretty print, optional dependency
import customtkinter
from tkinter import StringVar
import tkinter.messagebox


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


ALPHABET = string.ascii_letters + string.digits
     

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

        # create footer frame 
        self.footer_frame = customtkinter.CTkFrame(self, height=25,corner_radius=0, fg_color="#007ACC")
        self.footer_frame.grid(row=3, column=1,padx=0, pady=(5, 0), sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)# center, fill space
        self.footer_label = customtkinter.CTkLabel( master=self.footer_frame, text="Developed by Abhijeetbyte © 2024",text_color=("#FFFFFF"),font=customtkinter.CTkFont(size=12),justify="center" )
        self.footer_label.grid(row=0, column=0,sticky="nsew")

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
        self.masterpassword_entry = customtkinter.CTkEntry(master=self.login_frame, width=300,height=40,border_width=1, show="*", placeholder_text=" ENTER MASTER PASSWORD")
        self.masterpassword_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
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
        
        self.entry_label = customtkinter.CTkLabel(self.entry_frame, text="Add your credentials: ", font=customtkinter.CTkFont(size=16))
        self.entry_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.entry_name = customtkinter.CTkEntry(master=self.entry_frame,width=350,height=40,border_width=1, placeholder_text="ENTER URL OR APP NAME, YOU WANT TO SAVE")
        self.entry_name.grid(row=1, column=0, padx=20, pady=(5, 5))
        
        self.entry_uname = customtkinter.CTkEntry(master=self.entry_frame, width=350,height=40,border_width=1,placeholder_text="ENTER NAME/USERNAME, YOU WANT TO SAVE")
        self.entry_uname.grid(row=2, column=0,  padx=20, pady=(5, 5))
        
        self.entry_password = customtkinter.CTkEntry(master=self.entry_frame,width=350,height=40,border_width=1, show="*", placeholder_text="ENTER PASSWORD, YOU WANT TO SAVE")
        self.entry_password.grid(row=3, column=0,  padx=20, pady=(5, 5))
        
        self.entry_button = customtkinter.CTkButton(self.entry_frame, text="Submit", command=self.entry_button_event)
        self.entry_button.grid(row=4, column=0, padx=30, pady=(10, 10))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=400,
                                                border_width=1,
                                                border_color="#007ACC",
                                                scrollbar_button_color="#007ACC",
                                                wrap="word",
                                                font=("Courier", 16)) #Monospaced font
        self.textbox.grid(row=1, column=1,padx=(20, 0), pady=(20, 0), sticky="nsew")



    
        # set default values
        self.appearance_mode_optionemenu.set("Light")
        self.textBox(text='') # text box (clear)
       
        
    
        data_file = os.path.isfile('data.csv')#check whether data file is there or not
        if not data_file:  # if csv not found
            self.create_csv()  # call function and create csv
            self.welcome_event()# start with welcome frame
           
        else :
            self.login_event()#start with login frame

            

    operationMenu = 1 #global, varible to hold operation code
        

    def welcome_event(self):
         #Show only the welcome frame, by removing everything else
         print("Welcome \n")
         self.login_frame.grid_forget()
         self.sidebar_button_frame.grid_forget()
         self.entry_frame.grid_forget()
         self.textbox.grid_forget()

    def login_event(self):
        # Show only the login frame
        print("Login \n")
        self.welcome_frame.grid_forget()# forget frame
        self.sidebar_button_frame.grid_forget()# forget frame
        self.entry_frame.grid_forget()# forget frame
        self.textbox.grid_forget()# forget frame
        self.login_frame.grid(row=1, column=1, sticky="ns")  # show login frame
        

    def main_event(self):
        self.welcome_frame.grid_forget()# forget frame (make sure)
        self.login_frame.grid_forget()  # forget frame (make sure)
        self.sidebar_button_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")# show frame
        self.entry_frame.grid(row=0, column=1,padx=(20,0),pady=(20,0), sticky="nsew")# show frame
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")# show frame
        
        
    def welcome_button_event(self):
         print("Next button pressed\n") 
         self.login_event()
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        print("Appearance changed :" , new_appearance_mode)
        customtkinter.set_appearance_mode(new_appearance_mode)

    def login_button_event(self):
        print("Login button pressed\n")
        master_pass = self.masterpassword_entry.get() #fetch from entry box
        print(master_pass,'\n')
        if len(master_pass) >= 8: #if sucessfull, then move to main window
            self.main_event()#call main window function
            return master_pass
        else:
            self.login_event() #do not preceded
            self.masterpassword_entry.delete(0,'end') #clear entry field 
            print("WARNING: Master password must be at least 8 characters long\n")
            #pass
        
    def back_button_event(self):
        print("Back button pressed\n")
        self.login_event() # call function to start with login window
        #clear entry field (make sure)
        self.masterpassword_entry.delete(0,'end') #clear
        self.entry_uname.delete(0,'end')
        self.entry_name.delete(0,'end')
        self.entry_password.delete(0,'end')
        self.textBox(text='') # text box (clear)

    def add_button_event(self):
        print("Add button pressed\n")      
        self.entry_label.configure(text="Add your credentials: ")#label
        self.entry_password.grid(row=3, column=0,  padx=20, pady=(5, 5))# add (make sure)
        self.entry_uname.grid(row=2, column=0,  padx=20, pady=(5, 5))# add
        self.entry_name.configure(placeholder_text="ENTER URL OR APP NAME, YOU WANT TO SAVE")# configure the placeholder text (make sure)
        self.entry_uname.configure(placeholder_text="ENTER NAME/USERNAME, YOU WANT TO SAVE")# (make sure)
        self.entry_password.configure(placeholder_text="ENTER PASSWORD, YOU WANT TO SAVE")  # (make sure)
        self.operationMenu = 1 # varible to hold operation code
        self.textBox(text='') # clear box
        
    def search_button_event(self):
        print("Search button pressed\n")
        self.entry_label.configure(text="Search your credentials: ")#label
        self.entry_uname.grid_forget()# remove
        self.entry_password.grid_forget()# remove
        self.entry_name.configure(placeholder_text="ENTER URL OR APP NAME, YOU WANT TO SEARCH")# configure the placeholder text
        self.operationMenu = 2
        print("HINT: Clicking the submit button will show all saved credentials.\n")
        self.textBox("HINT: Clicking the submit button will show all saved credentials")
                
        
    def edit_button_event(self):
        print("Edit button pressed\n")
        self.entry_label.configure(text="Edit your credentials: ")#label
        self.entry_uname.grid_forget()#remove
        self.entry_password.grid_forget()#remove
        self.entry_name.configure(placeholder_text="ENTER URL OR APP NAME, YOU WANT TO EDIT")# configure the placeholder text
        self.operationMenu = 3
        print("HINT: Clicking the submit button will show all saved credentials.\n")
        self.textBox("HINT: Clicking the submit button will show all saved credentials")

    def delete_button_event(self):
        print("Delete button pressed\n")
        self.entry_label.configure(text="Delete your credentials: ")#label
        self.entry_uname.grid_forget()#remove
        self.entry_password.grid_forget()#remove
        self.entry_name.configure(placeholder_text="ENTER URL OR APP NAME, YOU WANT TO DELETE")# configure the placeholder text
        self.operationMenu = 4

        


    #---------------------------------------------------------------------------

    def textBox(self, text):
         self.textbox.delete("0.0", "end")  # delete all text
         self.textbox.insert("0.0",text)

            
    def create_csv(self):
        data = {'Url/App name': [], 'Username': [], 'Password': []} # empty value dict
        df = pd.DataFrame(data)  # create new pandas DataFrame
        df.to_csv('data.csv', index=False)  # Write DataFrame to a new CSV file
        print("CSV created\n")


    def encrypt(self, password, master_pass):
        iteration_count = len(master_pass)
        
        # Encrypt password string with master password
        encrypted_password = ""
        
        for i in range(len(password)):
            shift = (ord(master_pass[i % len(master_pass)]) + i) % len(ALPHABET)
            if password[i] in ALPHABET:
                new_pos = (ALPHABET.find(password[i]) + shift) % len(ALPHABET)
                encrypted_password += ALPHABET[new_pos]
            else:
                encrypted_password += password[i]
        
        return encrypted_password

    
    
    def decrypt(self, encrypted_password, master_pass):
        iteration_count = len(master_pass)

        # Decrypt the encrypted password string with master password
        decrypted_password = ""
        
        for i in range(len(encrypted_password)):
            shift = (ord(master_pass[i % len(master_pass)]) + i) % len(ALPHABET)
            if encrypted_password[i] in ALPHABET:
                new_pos = (ALPHABET.find(encrypted_password[i]) - shift) % len(ALPHABET)
                decrypted_password += ALPHABET[new_pos]
            else:
                decrypted_password += encrypted_password[i]
        
        return decrypted_password

            

    def add(self, name, encrypted_pass, url):
        user_data = {'Url/App name': [url], 'Username': [name],'Password': [encrypted_pass]}# will save in same order (,) to csv file
        df = pd.DataFrame(user_data)  # pack user data into data frame
        df.to_csv('data.csv', mode='a', header=False, index=False)# save to CSV file, append new row
        self.textBox("Credentials Added Successfully.\n")




    def search(self, master_pass, url=''):
        # Extract form CSV file
        df = pd.read_csv('data.csv')

        dfS = df[df['Url/App name'].str.contains(url, na=False, case=False)]  # pass a string (word) to search like or related words in dataframe
        # if on argument were pass (url='') ,then it will fetch entire dataframe
        # print(dfS)
        index_d = dfS.index.values  # take default index

        # Logic/Sontrol str. to decrypt all found passwords
        password = []  # empty list to store decrypted password from for loop data
        dfS = dfS.reset_index()  # make sure indexes pair with number of row
        for index, row in dfS.iterrows():  # iterate over all rows

            found_password = dfS.loc[index, 'Password']  # go through all the rows of Password column ; get passwords
            dec_password = self.decrypt(found_password,  master_pass)  # decrypt that
            password.append(dec_password)

        dfS = dfS.set_index(index_d)  # set to default/original index for reference
        dfS['Password'] = password  # update password column with decrypted passwords

        return dfS








        

    def entry_button_event(self):
        print("Entry button pressed\n")
        print("Operation Menu : ", self.operationMenu)# operation code



        if (self.operationMenu == 1):
            print("Operation : Add\n")
            nameVariable = self.entry_name.get() # fetch entry box inputs
            unameVariable = self.entry_uname.get()
            passwordVariable = self.entry_password.get()
            print(nameVariable,',',unameVariable,',', passwordVariable)
            masterpassVariable = self.login_button_event() #fetch
            print(masterpassVariable)
            
            if (unameVariable == ''):  # if found empty, replace it by 'Unavailable' label
                unameVariable = 'UNAVAILABLE'
            if (passwordVariable == ''):
                passwordVariable = 'UNAVAILABLE'
            if (nameVariable == ''): # URL/App name
                print("WARNING: URL or App Name cannot be empty.\n")
                self.textBox("WARNING : URL or App Name cannot be empty.")
            else:
                encrypted_pass = self.encrypt(passwordVariable, masterpassVariable)# call encrypt function to encrypt password
                self.add(unameVariable, encrypted_pass, nameVariable)# call function to add user data
                #clear entry box
                self.entry_uname.delete(0,'end')
                self.entry_name.delete(0,'end')
                self.entry_password.delete(0,'end')

                


        elif (self.operationMenu == 2):
            print("Operation : Search\n")
            nameVariable = self.entry_name.get() # fetch entry box inputs
            print(nameVariable)
            masterpassVariable = self.login_button_event() #fetch
            print(masterpassVariable)
            show_result = self.search(masterpassVariable,nameVariable)# call function
            show_tabulate = tabulate.tabulate(show_result, headers='keys', tablefmt='pipe', showindex=False)#Pretty Print
            self.textBox(show_tabulate) # print in textbox area
            #print(show_tabulate)
            #clear entry box
            self.entry_name.delete(0,'end')




        elif (self.operationMenu == 3):
            print("Operation: Edit\n")
            nameVariable = self.entry_name.get()  # fetch entry box input
            print("Entry input: ", nameVariable, '\n')
            masterpassVariable = self.login_button_event()  # fetch
            print("Master Pass: ", masterpassVariable, '\n')
            
            show_result = self.search(masterpassVariable, nameVariable)  # call search function
            show_tabulate = tabulate.tabulate(show_result, headers='keys', tablefmt='pipe', showindex=False)  # Pretty Print
            self.textBox(show_tabulate)  # print in textbox area
            self.entry_name.delete(0, 'end')  # clear entry box

           


               



    


if __name__ == "__main__":
    app = App()
    app.mainloop()
