import pandas as pd
import os.path
import tabulate #arrange (data) in tabular form.


alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

print("""\n
 ╔╦╗╦ ╦╔═╗┌┬┐┌─┐┌┐┌┌┐┌┌─┐┌─┐┌─┐┬─┐
 ║║║╚╦╝╠═╝│││├─┤││││││├┤ │ ┬├┤ ├┬┘
 ╩ ╩ ╩ ╩  ┴ ┴┴ ┴┘└┘┘└┘└─┘└─┘└─┘┴└─
\n""")



def encrypt(password):

  # Encrypt password string with master password
  
  enc_password = ""
  for char in password:
    if char in alpha:
      newpos = (alpha.find(char) + Master_pass) % 62
      enc_password += alpha[newpos]
    else:
      enc_password += char

  return enc_password




def decrypt(find_password):


  # Decrypt the encrypted password string with master password

  dec_password = ""
  for char in find_password:
    if char in alpha:
      newpos = (alpha.find(char) - Master_pass) % 62
      dec_password += alpha[newpos]
    else:
      dec_password += char

  return dec_password



def create_csv():   
  
    data={'Url/App name':[], 'Username':[], 'Password':[]} #empty value dict
    df = pd.DataFrame(data) # create new pandas DataFrame
    df.to_csv('data.csv', index=False) # Write DataFrame to a new CSV file

    

def add(name, encrypted_pass, url ):
        
    user_data = {'Url/App name':[url], 'Username':[name], 'Password':[encrypted_pass]} #will save in same order (,) to csv file
    
    df = pd.DataFrame(user_data) # pack user data into data frame
    df.to_csv('data.csv', mode='a', header= False, index=False)# Save to CSV file, append New row
    
    print('\n Added successfully')

   

def search(url=''):

    # Extract form CSV file

    df = pd.read_csv('data.csv')
    
    dfS = df[df['Url/App name'].str.contains(url, na=False, case=False)] # pass a string (word) to search like or related words in dataframe
    dfS.head()                                                           # if on argument were pass (url='') ,then it will fetch entire dataframe
    #print(dfS)
    
    index_d = dfS.index.values #take default index
    
    #Logic/Sontrol str. to decrypt all found passwords

    password =[] #empty list to store decrypted password from for loop data
    dfS = dfS.reset_index()  # make sure indexes pair with number of row

    for index, row in dfS.iterrows(): #iterate over all rows
      
      find_password = dfS.loc[index,'Password']# go through all the rows of Password column ; get passwords
      dec_password= decrypt(find_password) #decrypt that
      password.append(dec_password)
    
    dfS = dfS.set_index(index_d) #set to default/original index for reference
    dfS['Password'] = password #update password column with decrypted passwords
  
    return dfS
    
   
  
def edit(index, new_name, new_password):

    df = pd.read_csv("data.csv") #using 0th column (Url) as index
    
    # Edit row at given 'index'
    
    df.loc[index,['Username', 'Password']] = [new_name, new_password] #replace it with new user data
    df.to_csv('data.csv', index=False) #save it

    print('\n Edited successfully')



def delete(index):

    df = pd.read_csv("data.csv")
    
    # Delete row at given 'index'
    
    df.drop([index],  axis=0, inplace=True)
    df.to_csv('data.csv', index=False) #save it
    
    print('\n Deleted successfully')



def backup():

    df = pd.read_csv("data.csv") #read the orignal file
    dp= os.getcwd() # get the default path, initial directory
    os.chdir("..") #change the current working directory, one dir back 
    cp= os.getcwd() #get the current path
    cp = cp + "\MYPmanager_Backup\data.csv" #add FolderName & FileName to obtained path
    
    if os.path.isdir('MYPmanager_Backup')== False: # If 'BackupMYPmanager' not exists

       os.makedirs('MYPmanager_Backup')# Create one, for back up
     
    df.to_csv(cp , index=False)#save a copy of same, cp = path
    os.chdir(dp) #Restoring the default path


    
data_file = os.path.isfile('data.csv') # check whether data file is there or not

if data_file == False : #if not then, create one
    create_csv()  #call function
    
    #First time instructions:
    print("\n Welcome to My Password manager\
           \n\n This application uses a Master Password\
           \n to encrypt & decrypt your data.\
           \n Use any 10 characters password (only letters & numbers)\
           \n and remember that.\
           \n\n Warning: If you lose your Master Password, then you \
           \n will not be able to recover your saved passwords.\
           \n\n Visit: https://github.com/Abhijeetbyte/MYPmanager\
           \n\n Thank You !\n")


         
print('\n Note: Master Password is a user defined value\
       \n needed to encrypt & decrypt data correctly')
while True:
    
    try:
        
        Master_pass =(input("\n Enter Master Password : "))

        Master_pass = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(Master_pass)])
        Master_pass = format(Master_pass).replace("-","")
        Master_pass = int(Master_pass)
        #print(Master_pass, type(Master_pass))
        break # if everything is fine; exit loop

    except:
        print('\n Warning: Master Password consists of letters and numbers only')
        
        


while True :

    try: # try block

        

        os.system('cls')# clear all

        print("\n [1] To save new credential\
            \n [2] To search saved credential\
            \n [3] To edit saved credential\
            \n [4] To delete saved credential\n")
        
        menu_option = int(input(" Select the corresponding option & press enter : "))

            
            
            
        if (menu_option == 1):
            
            os.system('cls')# clear all
            
            print("\n"*2," Add new credential \n")
            name = input(" enter name/username, you want to save : ")
            password = input(" enter password, you want to save : ")  # this will be encrypted
            url = input(" enter url or app name, you want to save : ")
            
            if (name == ''): #if found empty, replace it by 'Unavailable' label
                name='Unavailable'
            if (password ==''):
                password='Unavailable'
            if (url ==''):
                while (url ==''):
                    print('\n Warning: please enter a url or app name')
                    url = input("\n enter url or app, you want to save : ")
        
            encrypted_pass = encrypt(password) # call encrypt function to encrypt password
            add(name, encrypted_pass, url) # call function to add user data

            
            
        elif menu_option == 2 :

            os.system('cls')# clear all

            print("\n"*2," Search saved credential \n")
            print("\n [1] To see a specific saved credential\
                      \n [2] To see All saved credentials ")
            sub_option = int(input("\n Select the corresponding option & press enter :  "))
            
            if (sub_option == 1):
                
                url = input("\n enter URL or App name, you want to search : ")
                show = search(url)# call function to search/extract user data from csv
                show = show.to_markdown(tablefmt="orgtbl", index=False) #Pretty Print (Dataframe To Markdown)
                print('\n')
                print(show)
             
            else:
                show = search()# call function with no argument
                show = show.to_markdown(tablefmt="orgtbl", index=False) #Pretty Print (Dataframe To Markdown)
                print('\n')
                print(show)

                

        elif (menu_option == 3):

            os.system('cls')# clear all

            print("\n"*2," Edit saved credential")
            url = input("\n enter URL or App name, you want to edit : ")

            show = search(url)#call fun, to show respective data related to url
            show_md = show.to_markdown(tablefmt="orgtbl", index=False) #Pretty Print
            print('\n')
            print(show_md)
            print('\n'*2)

            if (len(show) > 1): #multiple credentials found, len = rows
                index = int(input(" Select the corresponding index value : "))
            else:
                index= show.index.values #take default index
                index = int(index)

            new_name = input("\n enter new name/user name : ")
            new_password = input(" enter new password: ")  # this will be encrypted
            
            
            #Exception----------------------

            if (new_name == ''): #if found empty, take old data
                old_name= show.loc[index, 'Username'] #column id , index of that row; get old Username
                new_name = old_name
                
            if (new_password ==''):
                old_password = show.loc[index, 'Password'] #get old password
                new_password= old_password

            new_password = encrypt(new_password)# call fun, to encrypted
            edit(index, new_name, new_password) #call edit function
            
        
        
        elif (menu_option == 4):

            os.system('cls')# clear all

            print("\n"*2," Delete saved credential \n")
            url = input("\n enter URL or App name, you want to delete : ")
            
            show = search(url)#call fun, to show respective data related to url
            show_md = show.to_markdown(tablefmt="orgtbl", index=False) #Pretty Print
            print('\n')
            print(show_md)
            print('\n'*2)

            if (len(show) > 1): #multiple credentials found, len = rows
                index = int(input(" Select the corresponding index value : "))
            else:
                index= show.index.values #take default index
                index = int(index)
                
            confirm = input("\n Do you want to continue, enter [y/n]  : ")
            
            if (confirm == 'y' or confirm == 'Y'):
                delete(index) # call delete function
                    
                   
        print("\n"*2)
        Continue = input(" Press Enter to 'OK' ")
        backup() # Back up the changes made

        

    except:  # all error/any error encountered
        print('\n Error: Not found !')
        continue # skip error , restart the loop ( try: block )

    
