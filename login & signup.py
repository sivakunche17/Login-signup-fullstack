

userdata = {}
from getpass import getpass 

def signup():
    print("\n--- SIGN UP ---")

    while True:
        user_name = input("Enter your user name: ")

        if user_name in userdata:
            print("\nUser name already Exists!")
        else:
            upper = False
            number = False

            for characters in user_name:
                if characters.isupper():
                    upper = True
                if characters.isdigit():
                    number = True
            if 8<= len(user_name) <=12 and upper and number:
                break
            else:
                print("\nUsername must have: ")
                print("Atleast 8-12 Characters")
                print("Atleast 1 Upper case")
                print("Atleast 1 Number")
    while True:
        user_password =input("Enter your password: ")

        Upper = False
        Number = False

        for Characters in user_password:
            if Characters.isupper():
                Upper = True
            if Characters.isdigit():
                Number = True
        if 6<= len(user_password) <=8 and Upper and Number:
            break
        else:
            print("\nPassword must have:")
            print("Atleast 6-8 Characters")
            print("Atleast 1 Upper case")
            print("Atleast 1 digit")
    while True:
        confirm_password = getpass("Enter your password again to Confirm: ")
        if user_password == confirm_password:
            break
        else:
            print("Password don't match")

    userdata[user_name] = user_password
    print("\nSignup Successful")


def dashboard(user_name, login_password):
    while True:
        print("-----------------------------")
        print("USER DASHBOARD")
        print("1. View profile")
        print("2. Change password")
        print("3. Logout")
        print("-----------------------------")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            print("----- PROFILE -----")
            print("User name: ",user_name)

        elif choice == "2":
            print("----- Change Password -----")

            while True:
                password = input("Enter your Current password: ")
                if password == login_password:

                    while True:
                        new_password = input("Enter new password: ")
                        upper = False
                        number = False
                        for characters in new_password:
                            if characters.isupper():
                                upper = True
                            if characters.isdigit():
                                number = True
                        if 6<=len(new_password) <=8 and upper and number:
                            break
                        else:
                            print("\nPassword must have 6-8 characters")
                            print("Atleast 1 Upper case")
                            print("Atleast 1 digit")

                    while True:
                        confirm_password = getpass("Confirm Password: ")
                        if new_password == confirm_password:
                            break
                        else:
                            print("Password not matched! try again")

                    userdata[user_name] = new_password
                    login_password = new_password

                    print("\nPassword changed Successfully")
                    break
                else:
                    print("\nWrong Current password! Try again")

        elif choice == "3":
            print("\nLogged out Successfully")
            break

def login():
    print("\n--- LOGIN ---")

    user_name = input("Enter your user name: ")
    
    if user_name in userdata:
        attempts = 3
        
        while attempts >0:
            login_password = input("Enter your password: ")
            if login_password == userdata[user_name]:
                print("\nLogin Successfully")
                print("\nWelcome:",user_name)
                dashboard(user_name, login_password)
                break
            else:
                attempts -= 1
                if attempts == 0:
                    print("\nWrong password!")
                    print("Too many incorrect attempts! Access blocked")
                    break
                else:
                    print("\nWrong password!")
                    print("Attempts left:",attempts)
    else:
        print("\nNo user found! Please Signup first")


def forget_password():
    print("\n----- Reset Password -----")

    user_name = input("Enter your User name to reset password: ")

    if user_name in userdata:
        while True:
            user_password = input("Enter new password: ")
            upper = False
            number = False

            for characters in user_password:
                if characters.isupper():
                    upper = True
                if characters.isdigit():
                    number = True
            if 6<= len(user_password) <=8 and upper and number:
                break
            else:
                print("\nPassword must have:")
                print("Atleast 6-8 Characters")
                print("Atleast 1 Upper case")
                print("Atleast 1 Number")
        while True:
            confirm_password = getpass("Enter password again to confirm: ")
            if user_password == confirm_password:
                break
            else:
                print("password dont match!")

        userdata[user_name] = user_password
        print("\nPassword changed Successfully")
    else:
        print("No user found! try again")


def Exit():
    print("\nExit Successfully")


while True:
    print("\n----- Welcome -----")
    print("1. Signup")
    print("2. Login")
    print("3. Forget password")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        signup()
    elif choice == "2":
        login()
    elif choice == "3":
        forget_password()
    elif choice == "4":
        Exit()
        break
    else:
        print("\nInvalid choice!")
