#!/usr/bin/env python3
import random

def main():
    newgame = Game()
    while not newgame.won:
        nextguess = input("Guess? ")
        if nextguess == "qqqqq":
            break
        guessnum, nexthint = newgame.taketurn(nextguess)
        print(f"{guessnum}: {nexthint}")

class Game():

    def __init__(self):
        with open("WORDS") as IFH:
            FLW = IFH.readlines()
        self.answer = random.choice(FLW)
        self.won = False
        self.guesscount = 0

    def taketurn(self, guess):
        self.guesscount += 1
        hint = ['_'] * 5
        for lnum, ltr in enumerate(guess):
            if self.answer[lnum] == ltr:
                hint[lnum] = 'G'
            elif ltr in self.answer:
                hint[lnum] = 'Y'
        if hint == ['G'] * 5:
            self.won = True
        return (self.guesscount, " ".join(hint))

if __name__ == '__main__':
    main()
