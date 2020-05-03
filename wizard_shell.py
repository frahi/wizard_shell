
import configparser
import datetime
import email.message
import random
import smtplib

class WizardCardDealer:
    """Class that is dealing the cards for a wizard game """

    def __init__(self, list_of_names):
        self.players = list_of_names
        self.all_cards = self.generate_all_cards()
        self.card_mix = self.generate_card_mix()        
        self.riffle()

    def generate_card_mix(self):
        card_mix = {}
        for player in self.players:
            card_mix[player] = []
        return card_mix

    def generate_all_cards(self):
        colors= { 'grün', 'blau', 'gelb', 'rot'}
        numbers = {'01','02','03','04','05','06','07','08','09','10','11','12','13'}
        special_cards = {'Zorro', 'Nixer'}
        all_cards = []
        for color in colors:
            for number in numbers:
                all_cards.append(color + number)
            for special_card in special_cards:
                all_cards.append(special_card)
        return all_cards

    def create_cards_sets(self, number_sets, cards_per_set):
        random.seed()
        selected_cards = random.sample(self.all_cards, number_sets*cards_per_set)
        #print(selected_cards)
        sets = []
        for set_id in range(number_sets):
            start_index = set_id * cards_per_set
            end_index = start_index + cards_per_set
            subset = selected_cards[start_index:end_index]
            subset = sorted(subset)
            sets.append( subset )
        return sets
        
    def riffle(self):
        num_players = len(self.players)
        num_rounds = int(60 / num_players)
        rounds = range(1,num_rounds+1)
        for round in rounds:
            round_card_set = self.create_cards_sets(num_players, round)
            cur_player_index = 0
            for player in self.players:
                self.card_mix[player].append(round_card_set[cur_player_index])
                cur_player_index = cur_player_index + 1

    def get_card_mix(self):
        return self.card_mix

class WizardPlayerManager():
    def __init__(self):
        self.names = []
        self.emails = {}

    def add_player(self, name, email):
        self.names.append(name)
        self.emails[name] = email

    def player_names(self):
        return self.names

    def get_address(self, player_name):
        return self.emails[player_name]

class WizardCommunication():
    def __init__(self, playerManager, smtp):
        self.playerManager = playerManager
        self.smtp = smtp
    
    def generate_smtp(host, port, user, password):
        smtp = smtplib.SMTP_SSL(host=host, port=port)
        smtp.login(user=user, password=password)
        return smtp

    def generate_rounds_string(rounds):
        outputstring = ''
        for round in rounds:
            outputstring = outputstring + 'Runde ' + str(len(round)) + ': '
            for round_element in round:
                outputstring =  outputstring + round_element + ', '
            outputstring = outputstring.rstrip(', ')
            outputstring = outputstring + '\n'
        return outputstring

    def create_game(self):
        wizardCardDealer = WizardCardDealer(playerManager.player_names())
        game_id = str(datetime.datetime.now())
        card_mix = wizardCardDealer.get_card_mix()
        for player in card_mix:
            card_mix_for_player = card_mix[player]
            message_text = 'Hallo ' + player + '\n\n'
            message_text = message_text + 'Das Wizard Spiel mit folgender ID wurde erzeugt: ' + game_id + '\n\n'
            message_text = message_text +  WizardCommunication.generate_rounds_string(card_mix_for_player)
            email_address = self.playerManager.get_address(player)
            print("Sending email for player " + player)
            self.send_email(email_address, message_text)

    def send_email(self, target_address, text, subject='Wizard Shell'):
        msg = email.message.EmailMessage()
        msg.set_content(text)
        msg['Subject'] = subject
        msg['From'] = 'franz.hirschbeck@frahi.de'
        msg['To'] = target_address
        #print(msg)
        smtp.send_message(msg)


config = configparser.ConfigParser()
config.read('wizard_shell.ini')

smtp = WizardCommunication.generate_smtp( host = config['SMTP']['host'],
                                          port =  config['SMTP']['port'],
                                          user = config['SMTP']['user'],
                                          password = config['SMTP']['password'] )

playerManager = WizardPlayerManager()
playerManager.add_player('Franz', 'info@frahi.de')
playerManager.add_player('Franz2', 'info@frahi.de')
playerManager.add_player('Franz3', 'info@frahi.de')

wizardCommunication = WizardCommunication(playerManager, smtp)
wizardCommunication.create_game()
