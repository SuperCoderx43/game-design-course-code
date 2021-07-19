from GameController import GameController

class Runner:

    def __init__(self):
        self.number_of_games_played = 0
        self.maximum_number_of_days_survived = 0
        self.playing = True
    
    def play(self):
        print("\n**********\nWelcome to Escape the Island! Explore an ancient island and try to survive until help arrives!\n**********\n")
        while(self.playing):
            newGame = GameController()
            newGame.play()
            self.save_max_number_of_days(newGame.days)
            self.number_of_games_played += 1
            self.playing = self.ask_to_play_again()
    
    def save_max_number_of_days(self, days_survived):
        if days_survived > self.maximum_number_of_days_survived:
            self.maximum_number_of_days_survived = days_survived

    def ask_to_play_again(self):
        while True:
            play_again = input("Play Again? (Y/N) ")
            if play_again.upper() == 'Y':
                return True
            elif play_again.upper() == 'N':
                print("\nThanks for Playing!\nCode by\nAnthony Silva\n2021")
                return False
            else:
                print("Invalid Input.")
                continue

