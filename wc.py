#!/usr/bin/env python3
import random

def main():
    newgame = Game()
    while not newgame.won:
        nextguess = input("Guess? ")
        if nextguess == "qqqqq":
            print(newgame.answer)
            break
        guessnum, nexthint = newgame.taketurn(nextguess)
        print(f"{guessnum}: {nexthint}")

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
        gset = set(guess)
        hint = ['_'] * 5
        for lnum, ltr in enumerate(ans):
            if ltr in gset:
                if guess[lnum] == ltr:
                    hint[lnum] = 'G'
                else:    
                    hint[guess.index(ltr)] = 'Y'
                gset.remove(ltr)
        if hint == ['G'] * 5:
            self.won = True
        return (self.guesscount, " ".join(hint))

if __name__ == '__main__':
    main()
