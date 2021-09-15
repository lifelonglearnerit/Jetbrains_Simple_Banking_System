# In our banking system, credit cards should begin with 4.
# In our banking system, the IIN must be 400000.
# In our banking system, account number should be unique.
# And the whole card number should be 16-digit length.
import random
import sqlite3


class BankAccount:

    # database creation
    db = sqlite3.connect('card.s3db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card ('
                '   id INTEGER,'
                '   number TEXT,'
                '   pin TEXT,'
                '   balance INTEGER DEFAULT 0'
                '     );')
    db.commit()

    # list of accounts will be not needed since we have db
    # accounts_list = []
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
        #self.accounts_list.append(self.card_generator(self.card_number, self.pin))
        self.cur.execute(f'INSERT INTO card (number, pin) VALUES ({gen_card_number}, {gen_pin_number});')
        self.db.commit()
        #self.cur.execute(f'SELECT * FROM card;')

        print('Your card has been created')
        print(f'Your card number:\n{gen_card_number}')
        print(f'Your card pin:\n{gen_pin_number}')
        # below code is just for debugging
        #print(self.cur.fetchall())
        # self.cur.execute(f'DELETE FROM card;')
        # self.db.commit()
        # print(self.cur.fetchall())

        # CHANGE IT FOR QUERY TO COMPARE EXISTING NUMBER WITH GENERATED - REGEX?
        # if len(self.accounts_list) >= 1:
        #     print(f'Your card number:\n{self.accounts_list[len(self.accounts_list) - 1][0]}')
        # else:
        #     print(f'Your card number:\n{self.accounts_list[0][0]}')

        # self.cur.execute(f'INSERT INTO card (pin) VALUES ({self.pin_generator(pin)});')
        # self.db.commit()
        #print(f'Your card PIN:\n{self.accounts_list[len(self.accounts_list) - 1][1]}')
        # print(self.accounts_list)
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


    # NEW METHOD FOR PIN
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
        if len(result) == 0:
            return False
        else:
            return True

    def log_to_account(self):

        if self.card_check(input('Enter your card number:\n'), input('Enter your PIN:\n')):
            print('You have successfully logged in!')
            self.logged_menu()
        else:
            print('Wrong card number or PIN!')
            self.main_menu()

    def logged_menu(self):
        logged_actions = {'1': self.account_balance,
                          '2': self.log_out,
                          '0': self.exit
                          }
        menu_logged = input('1. Balance\n'
                            '2. Log out\n'
                            '0. Exit\n')
        if menu_logged == '1':
            logged_actions['1']()
        elif menu_logged == '2':
            logged_actions['2']()
        elif menu_logged == '0':
            logged_actions['0']()




    def account_balance(self):
        self.cur.execute(f'SELECT balance '
                         f'FROM '
                         f'     card  '
                         f'WHERE '
                         f'     number = "{self.card_number}" '
                         f'     AND pin = "{self.pin_number}";')
        #print('card number: ', self.card_number)
        balance = self.cur.fetchall()
        print(f'Balance: {balance[0][0]}')
        self.logged_menu()

    def log_out(self):
        print('You have successfully logged out!')
        self.main_menu()

    def exit(self):
        exit()


    def exit(self):
        print('Bye!')
        exit()

BankAccount()
