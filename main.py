import pandas as pd
import os
import os.path
from pwinput import pwinput
import string
import tabulate  # pretty print, optional dependency

ALPHABET = string.ascii_letters + string.digits

os.system('color')


class textcolor:
    # Ansi color codes

    TITLE = '\033[31m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def clear():
    # Set function clear depending on OS

    # for windows
    if os.name == 'nt':
        os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')

def get_master_password():
    while True:
        master_pass = pwinput(prompt="\n Enter master password\n( Must have a minimum of 8 characters ):  ", mask="*")
        print("")
        if len(master_pass) >= 8:
            break
        else:
            print(textcolor.WARNING + '\n WARNING: Master password should be at least 8 characters long.' + textcolor.ENDC)
    return master_pass


def encrypt(password, master_pass):
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


def decrypt(encrypted_password, master_pass):
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


def create_csv():
    data = {'Url/App name': [], 'Username': [], 'Password': []}  # empty value dict
    df = pd.DataFrame(data)  # create new pandas DataFrame
    df.to_csv('data.csv', index=False)  # Write DataFrame to a new CSV file


def add(name, encrypted_pass, url):
    user_data = {'Url/App name': [url], 'Username': [name],
                 'Password': [encrypted_pass]}  # will save in same order (,) to csv file

    df = pd.DataFrame(user_data)  # pack user data into data frame
    df.to_csv('data.csv', mode='a', header=False, index=False)  # Save to CSV file, append New row

    print(textcolor.OKGREEN + '\n' * 2 + ' ADDED SUCCESSFULLY' + textcolor.ENDC)


def search(url=''):
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

        find_password = dfS.loc[index, 'Password']  # go through all the rows of Password column ; get passwords
        dec_password = decrypt(find_password, master_password)  # decrypt that
        password.append(dec_password)

    dfS = dfS.set_index(index_d)  # set to default/original index for reference
    dfS['Password'] = password  # update password column with decrypted passwords

    return dfS


def edit(index, new_name, new_password):
    df = pd.read_csv("data.csv")  # using 0th column (Url) as index

    # Edit row at given 'index'

    df.loc[index, ['Username', 'Password']] = [new_name, new_password]  # replace it with new user data
    df.to_csv('data.csv', index=False)  # save it

    print(textcolor.OKGREEN + '\n' * 2 + ' EDITED SUCCESSFULLY' + textcolor.ENDC)


def delete(index):
    df = pd.read_csv("data.csv")

    # Delete row at given 'index'

    df.drop([index], axis=0, inplace=True)
    df.to_csv('data.csv', index=False)  # save it

    print(textcolor.OKGREEN + '\n' * 2 + ' DELETED SUCCESSFULLY' + textcolor.ENDC)


def backup():
    df = pd.read_csv("data.csv")  # read the orignal file
    dp = os.getcwd()  # get the default path, initial directory
    os.chdir("..")  # change the current working directory, one dir back
    cp = os.getcwd()  # get the current path
    cp = cp + "\MYPmanager_Backup\data.csv"  # add FolderName & FileName to obtained path

    if not os.path.isdir('MYPmanager_Backup'):  # If 'BackupMYPmanager' not exists

        os.makedirs('MYPmanager_Backup')  # Create one, for back up

    df.to_csv(cp, index=False)  # save a copy of same, cp = path
    os.chdir(dp)  # Restoring the default path



print(textcolor.TITLE + """\n

  __  ____   _____                                   
 |  \/  \ \ / / _ \_ __  __ _ _ _  __ _ __ _ ___ _ _ 
 | |\/| |\ V /|  _/ '  \/ _` | ' \/ _` / _` / -_) '_|
 |_|  |_| |_| |_| |_|_|_\__,_|_||_\__,_\__, \___|_|  
                                       |___/         


""" + textcolor.ENDC)


data_file = os.path.isfile('data.csv')  # check whether data file is there or not

if not data_file:  # if not then, create one
    
    create_csv()  # call function

    # First time instructions:
    print(textcolor.BOLD + "\n WELCOME TO MY PASSWORD MANAGER" + textcolor.ENDC)

    print("\n THIS APPLICATION USES A MASTER PASSWORD\
           \n TO ENCRYPT & DECRYPT YOUR DATA.\
           \n USE ANY ALPHANUMERIC PASSWORD (RECOMMENDED)\
           \n AND REMEMBER THAT.\
           \n\n WARNING: IF YOU LOSE YOUR MASTER PASSWORD, THEN YOU\
           \n WILL NOT BE ABLE TO RECOVER YOUR SAVED PASSWORDS.\
           \n\n VISIT: https://github.com/Abhijeetbyte/MYPmanager")

print('\n\n NOTE: MASTER PASSWORD IS A USER DEFINED VALUE\
       \n NEEDED TO ENCRYPT & DECRYPT DATA CORRECTLY.')


while True:

    try:

        master_password = get_master_password()
        break  # if everything is fine; exit loop

    except:
        print(textcolor.WARNING + '\n WARNING: MASTER PASSWORD CONSISTS OF LETTERS & NUMBERS ONLY.' + textcolor.ENDC)


while True:

    try:  # try block

        clear()  # clear all

        print(textcolor.BOLD + "\n" + " " * 50 + "MENU" + textcolor.ENDC)

        print("\n" * 3 + " [01] ADD NEW CREDENTIAL\
            \n\n [02] SEARCH CREDENTIAL\
            \n\n [03] EDIT CREDENTIAL\
            \n\n [04] DELETE CREDENTIAL")

        menu_option = int(input("\n" * 3 + " SELECT AN OPTION & PRESS ENTER : "))

        

        if (menu_option == 1):

            clear()  # clear all

            print(textcolor.BOLD + "\n" * 2, "ADD NEW CREDENTIAL\n" + textcolor.ENDC)
            name = input("\n ENTER NAME/USERNAME, YOU WANT TO SAVE: ")
            password = pwinput(prompt ="\n ENTER PASSWORD, YOU WANT TO SAVE: ", mask="*") # this will be encrypted
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO SAVE: ")

            if (name == ''):  # if found empty, replace it by 'Unavailable' label
                name = 'UNAVAILABLE'
            if (password == ''):
                password = 'UNAVAILABLE'
            if (url == ''):
                while (url == ''):
                    print(textcolor.WARNING + '\n WARNING: PLEASE ENTER A URL OR APP NAME: ' + textcolor.ENDC)
                    url = input("\n ENTER URL OR APP NAME, YOU WANT TO SAVE: ")

            encrypted_pass = encrypt(password, master_password)  # call encrypt function to encrypt password
            add(name, encrypted_pass, url)  # call function to add user data



        elif menu_option == 2:

            clear()  # clear all

            print(textcolor.BOLD + "\n" * 2, "SEARCH CREDENTIAL \n" + textcolor.ENDC)
            print("\n [01] SEE A SPECIFIC SAVED CREDENTIAL\
                      \n\n [02] SEE ALL SAVED CREDENTIALS")
            sub_option = int(input("\n" * 3 + " SELECT AN OPTION & PRESS ENTER : "))

            if (sub_option == 1):
                url = input("\n ENTER URL OR APP NAME, YOU WANT TO SEARCH: ")
                show_result = search(url)  # call function to search/extract user data from csv
                show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)  # Pretty Print (Dataframe to Markdown/String)
                print('\n')
                print(show_in_md)

            if (sub_option == 2):
                show_result = search()  # call function with no argument
                show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)
                print('\n')
                print(show_in_md)



        elif (menu_option == 3):

            clear()  # clear all

            print(textcolor.BOLD + "\n" * 2, "EDIT CREDENTIAL" + textcolor.ENDC)
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO EDIT: ")

            show_result = search(url)  # call fun, to show respective data related to url
            show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False) 
            print('\n')
            print(show_in_md)
            print('\n' * 2)

            if (len(show_result) > 1):  # multiple credentials found, len = rows
                index = int(input("\n SELECT AN INDEX VALUE & PRESS ENTER : "))
            else:
                index = show_result.index.values  # take default index
                index = int(index)

            new_name = input("\n ENTER NEW NAME/USERNAME: ")
            new_password = pwinput(prompt ="\n ENTER NEW PASSWORD : ", mask="*") # this will be encrypted

            # Exception----------------------

            if (new_name == ''):  # if found empty, take old data
                old_name = show_result.loc[index, 'Username']  # column id , index of that row; get old Username
                new_name = old_name

            if (new_password == ''):
                old_password = show_result.loc[index, 'Password']  # get old password
                new_password = old_password

            new_password = encrypt(new_password, master_password)  # call fun, to encrypted
            edit(index, new_name, new_password)  # call edit function



        elif (menu_option == 4):

            clear()  # clear all

            print(textcolor.BOLD + "\n" * 2, "DELETE CRDENTIAL \n" + textcolor.ENDC)
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO DELETE: ")

            show_result = search(url)  # call fun, to show respective data related to url
            show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)  
            print('\n')
            print(show_in_md)
            print('\n' * 2)

            if (len(show_result) > 1):  # multiple credentials found, len = rows
                index = int(input("\n SELECT AN INDEX VALUE & PRESS ENTER : "))
            else:
                index = show_result.index.values  # take default index
                index = int(index)

            confirm = input("\n DO YOU WANT TO CONTINUE, ENTER [Y/N] : ")

            if (confirm == 'y' or confirm == 'Y'):
                delete(index)  # call delete function

        print("\n" * 2)
        Continue = input("\n PRESS ENTER TO 'OK' ")
        backup()  # Back up the changes made



    except:  # all error/any error encountered
        print(textcolor.FAIL + '\n ERROR: NOT FOUND !' + textcolor.ENDC)
        print("\n" * 2)
        Continue = input("\n PRESS ENTER TO 'OK' ")
        continue  # skip error , restart the loop ( try: block )
