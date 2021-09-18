import random
import sqlite3


class BankAccount:

    db = sqlite3.connect('card.s3db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card ('
                '   id INTEGER,'
                '   number TEXT,'
                '   pin TEXT,'
                '   balance INTEGER DEFAULT 0'
                '     );')
    db.commit()

    def __init__(self):
        self.card_number = '4000000000000000'
        self.pin_number = '0000'
        self.main_menu()


    def main_menu(self):
        actions = {'1': self.create_account,
                   '2': self.log_to_account,
                   '0': self.exit
                   }
        menu_action = input('1. Create an account\n'
                            '2. Log into account\n'
                            '0. Exit\n')
        if menu_action == '1':
            actions['1'](self.card_number, self.pin_number)
        elif menu_action == '2':
            actions['2']()
        elif menu_action == '0':
            actions['0']()

    def luhn_check_sum(self, card):

        luhn_stage2 = [int(x) if (i + 1) % 2 == 0 else int(x) * 2 for i, x in enumerate(card)]
        luhn_stage3 = [x - 9 if x > 9 else x for x in luhn_stage2]
        if sum(luhn_stage3) % 10 > 0:
            ch_sum = 10 - (sum(luhn_stage3) % 10)
        else:
            ch_sum = 0

        return str(ch_sum)

    def create_account(self, card_number, pin_number):
        gen_card_number = self.card_generator(card_number)
        gen_pin_number = self.pin_generator(pin_number)
        self.cur.execute(f'INSERT INTO card (number, pin) VALUES ({gen_card_number}, {gen_pin_number});')
        self.db.commit()

        print('Your card has been created')
        print(f'Your card number:\n{gen_card_number}')
        print(f'Your card pin:\n{gen_pin_number}')
        # below code is just for debugging
        #print(self.cur.fetchall())

        """#######################################################"""
        # self.cur.execute(f'DELETE FROM card;')
        # self.db.commit()
        # print(self.cur.fetchall())
        """#######################################################"""
        self.main_menu()

    def card_generator(self, card_number):
        for i in range(6, 15):
            self.card_number = list(self.card_number)
            self.card_number[i] = str(random.randint(0, 8))
        self.card_number.pop(-1)
        check_sum = self.luhn_check_sum(self.card_number)
        self.card_number.append(check_sum)
        self.card_number = "".join(self.card_number)
        return self.card_number

    def pin_generator(self, pin_number):
        for x in range(4):
            self.pin_number = list(self.pin_number)
            self.pin_number[x] = str(random.randint(0, 9))
        self.pin_number = "".join(self.pin_number)
        return self.pin_number

    def card_check(self, _card_number, _pin_number):
        self.cur.execute(f'SELECT number, pin '
                         f'FROM '
                         f'     card  '
                         f'WHERE '
                         f'     number = "{_card_number}" '
                         f'     AND pin = "{_pin_number}";')
        result = self.cur.fetchall()
        if len(result):
            self.card_number = _card_number
            return True
        else:
            return False

    def log_to_account(self):

        if self.card_check(input('Enter your card number:\n'), input('Enter your PIN:\n')):
            print('You have successfully logged in!')
            self.logged_menu()
        else:
            print('Wrong card number or PIN!')
            self.main_menu()

    def logged_menu(self):
        print(self.card_number)
        logged_actions = {'1': self.balance_print,
                          '2': self.add_income,
                          '3': self.do_transfer,
                          '4': self.close_account,
                          '5': self.log_out,
                          '0': self.exit
                          }
        menu_logged = input('1. Balance\n'
                            '2. Add income\n'
                            '3. Do transfer\n'
                            '4. Close account\n'
                            '5. Log out\n'
                            '0. Exit\n')
        if menu_logged == '1':
            logged_actions['1']()
        elif menu_logged == '2':
            logged_actions['2']()
        elif menu_logged == '3':
            logged_actions['3']()
        elif menu_logged == '4':
            logged_actions['4']()
        elif menu_logged == '5':
            logged_actions['5']()
        elif menu_logged == '0':
            logged_actions['0']()
# testing idea of printing function to reuse account_balance in other part of program
# without the need to comback to logged_menu.
    def balance_print(self):

        print(f'Balance: {self.account_balance()}')
        self.logged_menu()

    def account_balance(self):
        self.cur.execute(f'SELECT balance '
                         f'FROM '
                         f'     card  '
                         f'WHERE '
                         f'     number = "{self.card_number}";')

        # print('card number: ', self.card_number) # tylko debugging DO USUNIECIA
        balance = self.cur.fetchall()
        return balance[0][0]
        #print(f'Balance: {balance[0][0]}')
        #self.logged_menu()

    def add_income(self):
        add = int(input('Enter income:\n'))
        new_balance_add = add + self.account_balance()
        self.cur.execute(f'UPDATE '
                         f'     card '
                         f'SET '
                         f'     balance = {new_balance_add} '
                         f'WHERE'
                         f'     number = "{self.card_number}";')
        self.db.commit()
        print('Income was added!')
        # print(f'to card number: {self.card_number}') # THIS NEED TO BE REMOVED. JUST FOR DEBUGGING
        self.logged_menu()

    def card_exists(self, reciever_card):
        self.cur.execute(f'SELECT number '
                         f'FROM '
                         f'     card  '
                         f'WHERE '
                         f'     number = "{reciever_card}";')
        # JAKIE SA OGRANICZENIA SQLITE VS SQL
        result = self.cur.fetchall()
        if len(result):
            return True
        else:
            return False

    def money_transfer_recv(self,transfer_amount, reciver_card):
        self.cur.execute(f'SELECT balance '
                                          f'FROM '
                                          f'     card  '
                                          f'WHERE '
                                          f'     number = "{reciver_card}";')
        current_amount = self.cur.fetchall()
        new_balance_recv = current_amount[0][0] + transfer_amount

        self.cur.execute(f'UPDATE '
                         f'     card '
                         f'SET '
                         f'     balance = {new_balance_recv} '
                         f'WHERE'
                         f'     number = "{reciver_card}";')
        self.db.commit()

    def money_transfer_send(self, transfer_amount):
        new_balance = self.account_balance() - transfer_amount
        self.cur.execute(f'UPDATE '
                         f'     card '
                         f'SET '
                         f'     balance = {new_balance} '
                         f'WHERE'
                         f'     number = "{self.card_number}";')
        self.db.commit()

    def do_transfer(self):
        print('Transfer')
        # STAGE1 check sum check in luhn
        reciver_card = input('Enter card number:\n')
        reciver_card_check = reciver_card[0: len(reciver_card) - 1]
        luhn_check_sum = self.luhn_check_sum(reciver_card_check)
        if reciver_card[-1] == luhn_check_sum:
            if self.card_exists(reciver_card):
                transfer_amount = int(input('Enter how much money you want to transfer:\n'))
                if self.account_balance() >= transfer_amount:
                    self.money_transfer_recv(transfer_amount, reciver_card)
                    self.money_transfer_send(transfer_amount)
                    print('Success!')
                else:
                    print('Not enough money!')
                    self.logged_menu()
            else:
                print('Such a card does not exist.')
                self.logged_menu()
        else:
            print('Probably you made a mistake in the card number. Please try again!')
        self.logged_menu()

    def close_account(self):
        self.cur.execute(f'DELETE FROM card '
                         f'WHERE'
                         f'     number = "{self.card_number}";')
        self.db.commit()
        print('The account has been closed!')
        self.main_menu()

    def log_out(self):
        print('You have successfully logged out!')
        self.main_menu()

    def exit(self):
        print('Bye!')
        exit()

BankAccount()
