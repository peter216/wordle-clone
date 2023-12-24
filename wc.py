#!/usr/bin/env python3
import random

def main():
    playagain = "y"
    while playagain[0].lower() != "n":
        newgame = Game()
        over = False
        while not (newgame.won or over):
            nextguess = input("Guess? ")
            if nextguess == "qqqqq":
                print(f"It was {newgame.answer}")
                over = True
            else:
                guessnum, nexthint = newgame.taketurn(nextguess)
                print(f"{guessnum}: {nexthint}")
        if newgame.won:
            print(f"You got it in {guessnum}!")    
        print()
        playagain = input("Play again? ")
        print()

class Game():

    def __init__(self):
        with open("word-bank.csv") as IFH:
            self.wordbank = [w.strip() for w in IFH.readlines()]
        with open("valid-words.csv") as IFH:
            self.dictionary = [w.strip() for w in IFH.readlines()]
        self.answer = random.choice(self.wordbank)
        self.won = False
        self.guesscount = 0

    def taketurn(self, guess):
        ans = self.answer
        if guess not in self.dictionary:
            return (self.guesscount, "invalid")
        self.guesscount += 1
        glist = list(guess)
        hint = ['_'] * 5
        for lnum, ltr in enumerate(ans):
            if ltr in glist:
                if guess[lnum] == ltr:
                    hint[lnum] = 'G'
                else:    
                    hint[guess.index(ltr)] = 'Y'
                glist.remove(ltr)
        if hint == ['G'] * 5:
            self.won = True
        return (self.guesscount, " ".join(hint))

if __name__ == '__main__':
    main()
