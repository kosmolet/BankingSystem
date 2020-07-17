from random import sample
import sqlite3
 
 
class Bank:
 
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_db()
        self.choice = ""
        self.INN = "400000"
        self.menu()
 
    def init_db(self):
        self.conn = sqlite3.connect("card.s3db")
        self.cursor = self.conn.cursor()
        create_table_sql = "CREATE TABLE IF NOT EXISTS card(id integer, number text, pin text, balance integer default 0)"
        self.cursor.execute(create_table_sql)
 
    def menu(self):
        while True:
            print("""1. Create an account
            2. Log into account
            0. Exit""")
            self.choice = input()
            if self.choice == "1":
                self.create_account(self.generate_account(), self.generate_pin())
            elif self.choice == "2":
                self.login()
            else:
                break
 
    def create_account(self, number, pin):
        self.cursor.execute(f"INSERT INTO card(number, pin) VALUES('{number}', '{pin}')")
        self.conn.commit()
        print(f"Your card number:\n{number}")
        print(f"Your card PIN:\n{pin}")
        print("Your card has been created")
 
    def login(self):
        print("Enter your card number:")
        card_numb = input()
        print("Enter your PIN:")
        pin = input()
        check_pin_sql = f"SELECT * from card where number = '{card_numb}' and pin = '{pin}'"
        account = self.cursor.execute(check_pin_sql).fetchone()
        if not account:
            print("Wrong card number or PIN!")
        else:
            Account(account[1], account[2], account[3], self)
 
    def generate_account(self):
        card_number = self.INN + "".join(map(str, sample(range(0, 10), 9)))
        return card_number + str(self.generate_chkd(card_number))
 
    @staticmethod
    def generate_pin():
        return "".join(map(str, sample(range(0, 9), 4)))
 
    @staticmethod
    def generate_chkd(card_number):
        digits = list(map(int, list(card_number)))
        digits = [digits[i] * 2 if i % 2 == 0 else digits[i] for i in range(len(digits))]
        digits = [i - 9 if i > 9 else i for i in digits]
        if sum(digits) % 10 == 0:
            return 0
        return (sum(digits) // 10 + 1) * 10 - sum(digits)
 
 
class Account:
 
    def __init__(self, account_number, pin, balance, bank):
        self.choice = ""
        self.bank = bank
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.menu()
 
    def menu(self):
        print("You have successfully logged in!")
        while True:
            print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
            self.choice = input()
            if self.choice == "1":
                self.print_balance()
            elif self.choice == "2":
                self.add_income()
            elif self.choice == "3":
                self.make_transfer()
            elif self.choice == "4":
                self.close_account()
                break
            elif self.choice == "5":
                print("You have successfully logged out!")
                break
            else:
                print("Bye!")
                quit()
 
    def close_account(self):
        self.bank.cursor.execute("DELETE FROM card WHERE number= ?", (self.account_number,))
        self.bank.conn.commit()
        print("The account has been closed!")
 
    def print_balance(self):
        print("Balance:", self.balance)
 
    def add_income(self):
        print("Enter income:")
        income = int(input())
        self.update_balance(income, self.account_number)
        print("Income was added!")
 
    def make_transfer(self):
        print("Enter card number:")
        new_card = input()
        if len(new_card) == 16 and str(Bank.generate_chkd(new_card[:15])) == new_card[15]:
            if not self.check_card(new_card):
                print("Enter how much money you  want to transfer:")
                amount = int(input())
                if self.balance >= amount:
                    self.update_balance(amount, new_card)
                    self.update_balance(- amount, self.account_number)
                    print("Success!")
                else:
                    print("Not enough money!")
            else:
                print("Such a card does not exist")
        else:
            print("Probably you made mistake in the card number. Please try again!")
 
    def check_card(self, number):
        exists = self.bank.cursor.execute("SELECT * FROM card WHERE number = ?", (number,)).fetchone()
        return exists is None
 
    def update_balance(self, amount, card):
        self.bank.cursor.execute("UPDATE card set balance = balance + ? WHERE number = ?", (amount, card))
        self.bank.conn.commit()
        self.balance += amount
 
 
Bank()
print("Bye")
