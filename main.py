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
    df.to_csv('data.csv', mode='a', header= False, index= False)# Save to CSV file, append New row
    
    print('\n Added successfully')

        

def search(url):

    # Extract form CSV file

    df = pd.read_csv("data.csv",index_col = 0) #using 0th column (Url) as index
    find_password = df['Password'][url] #column id , index of that row; get stored password
    find_username= df['Username'][url] #get stored Username
    
    decrypted_pass = decrypt(find_password) # call decrypt function to decrypt stored password
    df = pd.DataFrame({'Username':[find_username], 'Password':[decrypted_pass],'Url/App name':[url]}) #to print found  data

    return df

   

def edit(url, new_name, new_password):

    df = pd.read_csv("data.csv",index_col = 0) #using 0th column (Url) as index
    
    # Edi row at index 'url'
    df.loc[url] = [new_name, new_password] #replace it with new user data
    df.to_csv('data.csv') #save it
    
    print('\n Edited successfully')



def delete(url):

    df = pd.read_csv("data.csv",index_col = 0) #using 0th column (Url) as index
    
    # Delete row at index 'url'
    df.drop([url],  axis=0, inplace=True)
    df.to_csv('data.csv') #save it
    
    print('\n Deleted successfully')




data_file = os.path.isfile('data.csv') # check whether data file is there or not

if data_file == False : #if not then, create one
    create_csv()  #call function
    
    #First time instructions:
    print("\n Welcome to My Password manager\
           \n\n This password manager uses a Master Password\
           \n to encrypt & decrypt your saved passwords.\
           \n Use any 10 digit Password (only letters & numbers)\
           \n and remember that.\
           \n\n Warning: If you lose your Master Password, then you \
           \n will not be able to recover your saved passwords.\
           \n\n Visit: https://github.com/Abhijeetbyte/MYPmanager.git\
           \n\n Thank You !\n")


         
print('\n Note: Master Password is a user defined value\
       \n needed to encrypt & decrypt data correctly')
Master_pass =(input("\n Enter Master Password : "))

Master_pass = "".join([(str(ord(x)-96) if x.isalpha() else x) for x in list(Master_pass)])
Master_pass = format(Master_pass).replace("-","")
Master_pass = int(Master_pass)
#print(Master_pass, type(Master_pass))





while True :

    try: # try block

        

        os.system('cls')# clear all

        print("\n [1] To save new credential\
            \n [2] To search saved credential\
            \n [3] To edit saved credential\
            \n [4] To delete saved credential")
        
        menu_option = int(input("\n Select the corresponding option & press enter : "))

            
            
            
        if (menu_option == 1):
            
            os.system('cls')# clear all
            
            print("\n"*2," Add new credential \n")
            name = input(" enter name/username, you want to save : ")
            password = input(" enter password, you want to save : ")  # this will be encrypted
            url = input(" enter url or app name, you want to save : ")
            
            #Default duplicate check in DataFrame/CSV file
            df = pd.read_csv('data.csv')
            
            if url in df.values: # check if given URL exists
                print("\n Error: url or app name is already present, try a bit different")
                url = input("\n enter url or app, you want to save : ")
            
            encrypted_pass = encrypt(password) # call encrypt function to encrypt password
            add(name, encrypted_pass, url) # call function to add user data

            
            
        elif menu_option == 2 :

            os.system('cls')# clear all

            print("\n"*2," Search saved credential \n")
            print("\n [1] To see a specific saved credential\
                      \n [2] To see All saved credentials ")
            sub_option = int(input("\n Select the corresponding option & press enter :  "))
            
            if (sub_option == 2): 
             
                #Logic/Contole Str. to decrypt all saved passwords/credentials

                df = pd.read_csv('data.csv')
                df = df.reset_index()  # make sure indexes pair with number of rows

                df2 =pd.DataFrame(columns=['Username','Password','Url/App name']) # empty df to append for loop data
                
                for index, row in df.iterrows(): #iterate over all rows
                  
                  url = (row['Url/App name'])# go through all the rows of URL column ; get urls
                  df1 = search(url) # pass all found urls to search function
                  #df2 = df2.append(df1)
                  df2 = pd.concat([df1, df2], axis=0)
                  
                show_all = df2.to_markdown(index=False) #Pretty Print (Dataframe To Markdown)
                print('\n')
                print(show_all)
            
            else:
                url = input("\n enter URL or App name, you want to search : ")
                show = search(url)# call function to search/extract user data from csv
                show = show.to_markdown(index=False) #Pretty Print (Dataframe To Markdown)
                print('\n')
                print(show)

                

        elif (menu_option == 3):

            os.system('cls')# clear all

            print("\n"*2," Edit saved credential")
            url = input("\n enter URL or App name, you want to edit : ")

            show = search(url)#call fun, to show respective data related to url
            show = df2.to_markdown(index=False) #Pretty Print
            print('\n')
            print(show)
            
            new_name = input("\n enter new name/user name : ")
            new_password = input(" enter new password: ")  # this will be encrypted

            new_password = encrypt(new_password)# call fun, to encrypted
            edit(url, new_name, new_password) #call edit function
            
        
        
        elif (menu_option == 4):

            os.system('cls')# clear all

            print("\n"*2," Delete saved credential \n")
            print("\n [1] To delete a specific saved credential\
                   \n [2] To delete All saved credentials ")
            
            sub_option = int(input("\n Select the corresponding option & press enter :  "))
            
            if (sub_option == 1): 

                url = input("\n enter URL or App name, you want to delete : ")
                
                show = search(url)#call fun, to show respective data related to url
                show = df2.to_markdown(index=False) #Pretty Print
                print('\n')
                print(show)
                delete(url) # call delete function
                
            else:
                print('\n This will delete all saved data')
                conforme = input(" Do you want to continue, enter [y/n]  : ")
                if (conforme == 'y' or conforme == 'Y'):
                    create_csv()# call fun, create new csv (trick)
                    print('\n Deleted successfully')
                    
                   
        print("\n"*2)
        Continue = input(" Press Enter to 'OK' ")

        

    except:  # all error/any error encountered
        print('\n Error: Not found !')
        continue # skip error , restart the loop ( try: block )

    


