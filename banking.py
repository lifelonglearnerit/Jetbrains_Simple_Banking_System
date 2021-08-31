# In our banking system, credit cards should begin with 4.
# In our banking system, the IIN must be 400000.
# In our banking system, account number should be unique.
# And the whole card number should be 16-digit length.
import random


class BankAccount:
    accounts_list = []

    def __init__(self):
        self.card_number = '4000000000000000'
        self.pin = '0000'
        self.main_menu()

    def main_menu(self):
        """
        Displays the main menu and allow to make choice.
        Choice will invoke other functions
        :return:
        """
        actions = {'1': self.create_account,
                   '2': self.log_to_account,
                   '0': self.exit
                   }
        menu_action = input('1. Create an account\n'
                            '2. Log into account\n'
                            '0. Exit\n')
        if menu_action == '1':
            actions['1'](self.card_number, self.pin)
        elif menu_action == '2':
            actions['2']()
        elif menu_action == '0':
            actions['0']()

    def create_account(self, card_number, pin):
        """
        Generates 16-digit unique number
        Generates 4 digit PIN in range 0000 - 9999
        Creates object of the class BankAccount
        :return:
        """

        self.accounts_list.append(self.card_generator(self.card_number, self.pin))
        # while True:
        #     self.card_generator(self.card_number, self.pin)
        #     if self.card_generator(self.card_number, self.pin) in self.accounts_list:
        #         self.card_generator(self.card_number, self.pin)
        #     else:
        #
        #         self.accounts_list.append(self.card_generator(self.card_number, self.pin))
        #         break

        print('Your card has been created')
        if len(self.accounts_list) >= 1:
            print(f'Your card number:\n{self.accounts_list[len(self.accounts_list) - 1][0]}')
        else:
            print(f'Your card number:\n{self.accounts_list[0][0]}')
        print(f'Your card PIN:\n{self.accounts_list[len(self.accounts_list) - 1][1]}')
        print(self.accounts_list)
        self.main_menu()

    def card_generator(self, card_number, pin):
        print(type(card_number))
        for i in range(6, 15):
            self.card_number = list(self.card_number)
            self.card_number[i] = str(random.randint(0, 8))
        print('to jest przed luhna', self.card_number)
        self.card_number.append(self.luhn_check_sum(self.card_number))
        self.card_number = "".join(self.card_number)
        print(self.card_number)
        for x in range(4):
            self.pin = list(self.pin)
            self.pin[x] = str(random.randint(0, 9))
            self.pin = "".join(self.pin)
        return self.card_number, self.pin

    def log_to_account(self):
        """
        Takes input from user - Card information and PIN
        :return:
        """
        if (input('Enter your card number:\n'), input('Enter your PIN:\n')) in self.accounts_list:
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
        print('Balance: 0')
        self.logged_menu()

    def log_out(self):
        print('You have successfully logged out!')
        self.main_menu()

    def exit(self):
        exit()

    def luhn_check_sum(self, card):
        print('luna',type(card))
        print('dlugosc numeru karty:',len(card))
        print('to trafia do luny', card)
        luhn_stage2 = [int(x) if (i + 1) % 2 == 0 else int(x) * 2 for i, x in enumerate(card)]
        luhn_stage3 = [x - 9 if x > 9 else x for x in luhn_stage2]
        if sum(luhn_stage3) % 10 > 0:
            ch_sum = 10 - (sum(luhn_stage3) % 10)
            print('to jest w lunie', ch_sum)
        card.pop(-1)
        card.insert(len(card),str(ch_sum))
        print('to wychodzi lunie', card)
        print('dlugosc numeru na wyjsciu:', len(card))
        return str(ch_sum)


BankAccount()
