################################
# Tenzin Wangchuk
# BE ELECTRICAL ENGG. 1ST YEAR
# CSF101
# 02230087
################################
# REFERENCES
# chat GPT
#https://www.upgrad.com/blog/python-banking-project/
# https://youtu.be/julcNz6rWVc
###################################


import os  # Importing the os module for file operations.
import json  # Importing the json module for data serialization.
import random  # Importing the random module for generating random numbers.

class Account:
    def __init__(self, account_number, password, account_type, balance=0.00):
        # Initializes the user with account number, password, account type, and optional balance.
        self.account_number = account_number  # Stores the account number.
        self.password = password  # Stores the password.
        self.account_type = account_type  # Stores the account type 
        self.balance = balance  # Stores the balance, default is 0.00.

    def deposit(self, amount):
        # deposit money into the account if the amount is positive.
        if amount > 0:  # Check if the deposit amount is positive.
            self.balance += amount  # Add the amount to the current balance.
            return True  # Return True indicating successful deposit.
        return False  # Return False if the deposit amount is not positive.

    def withdraw(self, amount):
        # withdraw money from the account if the amount is positive and does not exceed the balance.
        if 0 < amount <= self.balance:  # Check if the withdrawal amount balance.
            self.balance -= amount  # Subtract the amount from the current balance.
            return True  # Return True indicating successful withdrawal.
        return False  # Return False if the withdrawal amount is not valid.

    def to_dict(self):
        # convert account details to a dictionary for easy storage in JSON format.
        return {
            'account_number': self.account_number,  # Add account number to the dictionary.
            'password': self.password,  # Add password to the dictionary.
            'account_type': self.account_type,  # Add account type to the dictionary.
            'balance': self.balance  # Add balance to the dictionary.
        }

class BankingSystem:
    def __init__(self, filepath='accounts.txt'):
        # Initializes the BankingSystem object with a filepath to store account data.
        self.filepath = filepath  # Stores the filepath.
        self.load_accounts()  # Load accounts from the file.

    def load_accounts(self):
        # Method to load accounts from the file if it exists, otherwise create an empty accounts dictionary.
        if not os.path.exists(self.filepath):  # Check if the file does not exist.
            self.accounts = {}  # Initialize an empty dictionary for accounts.
            self.save_accounts()  # Save the empty accounts dictionary to the file.
        else:
            with open(self.filepath, 'r') as file:  # Open the file in read mode.
                self.accounts = json.load(file)  # Load the accounts from the file.

    def save_accounts(self):
        # Method to save the accounts dictionary to the file in JSON format.
        with open(self.filepath, 'w') as file:  # Open the file in write mode.
            json.dump(self.accounts, file)  # Save the accounts dictionary to the file in JSON format.

    def create_account(self, account_type):
        account_number = str(random.randint(100000000, 999999999))  # Generate a random account number.
        password = str(random.randint(0000, 9999))  # Generate a random password.
        if account_number in self.accounts:  # Check if the account number already exists (rare case).
            return None, None  # Return None if account number collision occurs.
        account = Account(account_number, password, account_type)  # Create a new Account object.
        self.accounts[account_number] = account.to_dict()  # Add the account to the accounts dictionary.
        self.save_accounts()  # Save the updated accounts dictionary to the file.
        return account_number, password  # Return the new account number and password.

    def login(self, account_number, password):
        # Method to authenticate a user by verifying the account number and password.
        account_info = self.accounts.get(account_number)  # Get the account info from the accounts dictionary.
        if account_info and account_info['password'] == password:  # Check if account exists and password matches.
            return Account(**account_info)  # authentication is successful.
        return None  # authentication fails.

    def update_account(self, account):
        # Method to update account information in the accounts dictionary and save to file.
        self.accounts[account.account_number] = account.to_dict()  # Update the account details in the dictionary.
        self.save_accounts()  # Save the updated accounts dictionary to the file.

    def delete_account(self, account_number):
        # Method to delete an account from the accounts dictionary and save to file.
        if account_number in self.accounts:  # Check if the account number exists.
            del self.accounts[account_number]  # Delete the account from the dictionary.
            self.save_accounts()  # Save the updated accounts dictionary to the file.
            return True  # successful deletion.
        return False  # the account number does not exist.

    def transfer_money(self, from_account, to_account_number, amount):
        # Method to transfer money from one account to another acc.
        to_account_info = self.accounts.get(to_account_number)  # Get the recipient account info.
        if not to_account_info:  # Check if the recipient account does not exist.
            return False  # Return False indicating transfer failure.
        if from_account.withdraw(amount):  # Attempt to withdraw the amount from the sender's account.
            to_account = Account(**to_account_info)  # Create an Account object for the recipient.
            to_account.deposit(amount)  # Deposit the amount into the recipient's account.
            self.update_account(from_account)  # Update the sender's account details.
            self.update_account(to_account)  # Update the recipient's account details.
            return True  # Return True indicating successful transfer.
        return False  # Return False if withdrawal fails due to insufficient balance.

def main():
    # Main function to interact with the banking system.
    banking_system = BankingSystem()  # Instantiate the BankingSystem object.

    while True:
        # Display main menu options.
        print("1. Create Account")
        print("2. Login")
        print("3. Log out")
        choice = input("Select an option: ")  # Prompt user to select an option.

        if choice == '1':
            # Handle account creation.
            account_type = input("Enter account type (savings/current/business/personal): ")
            account_number, password = banking_system.create_account(account_type)  # Create the account.
            if account_number:  # Check if account creation was successful.
                print(f"Account created. Account Number: {account_number}, Password: {password}")  # Display account details.
            else:
                print("Failed to create account. Try again.")  # Display error message if account creation fails.

        elif choice == '2':
            # Handle account login.
            account_number = input("Enter account number: ")  # Prompt for account number.
            password = input("Enter password: ")  # Prompt for password.
            account = banking_system.login(account_number, password)  # Attempt to login.
            if account:  # Check if login was successful.
                print("Login successful.")  # Display success message.
                while True:
                    # Display account management menu.
                    print("1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Select an option: ") 

                    if choice == '1':
                        # Display account balance.
                        print(f"Balance: {account.balance}")  # Show the current balance.

                    elif choice == '2':
                        # Handle deposit operation.
                        amount = float(input("Enter amount to deposit: "))  # Prompt for deposit amount.
                        if account.deposit(amount):  # Attempt to deposit the amount.
                            banking_system.update_account(account)
                            print("Deposit successful.") 
                        else:
                            print("Invalid deposit amount.")

                    elif choice == '3':
                        # Handle withdrawal operation.
                        amount = float(input("Enter amount to withdraw: "))  # Prompt for withdrawal amount.
                        if account.withdraw(amount):  # Attempt to withdraw the amount.
                            banking_system.update_account(account)  # Update the account details.
                            print("Withdrawal successful.")  # Display success message.
                        else:
                            print("Insufficient balance")  # Display error message if withdrawal fails.

                    elif choice == '4':
                        # Handle money transfer operation.
                        to_account_number = input("Enter recipient account number: ")  # Prompt for recipient account number.
                        amount = float(input("Enter amount to transfer: "))  # Prompt for transfer amount.
                        if banking_system.transfer_money(account, to_account_number, amount):  # Attempt to transfer money.
                            print("Transfer successful.")  # Display success message.
                        else:
                            print("Transfer failed. Check recipient account number or balance.")  # Display error message if transfer fails.

                    elif choice == '5':
                        # Handle account deletion.
                        if banking_system.delete_account(account.account_number):  # Attempt to delete the account.
                            print("Account deleted successfully.")  # Display success message.
                            break  # Exit the account management menu.
                        else:
                            print("Failed to delete account.")  # Display error message if deletion fails.

                    elif choice == '6':
                        # Handle logout operation.
                        print("Logout successful.")  # Display success message.
                        break  # Exit the account management menu.

        elif choice == '3':
            # Handle exit operation.
            print("Exit successful")  # Display goodbye message.
            break  # Exit the main menu loop.

if __name__ == "__main__":
    main()  # Execute the main function.
