#!/usr/bin/env python

import random
import string
import argparse #Välj fil som cmd-line argument till programmet

parser = argparse.ArgumentParser()
parser.add_argument("len", nargs='?', help="the length of the password")
args = parser.parse_args()

if args.len is None:
    pass_len = int(input("How long password gonna be yes? "))
else:
    pass_len = int(args.len)
    
#pass_len = int(input("How long password gonna be yes? "))
if pass_len > 1000000:
    exit("Are you sure you need such a long string?")
choice = random.randint(0, 1)
if choice:
    digits_amount = pass_len // 2
    letters_amount = pass_len - digits_amount
else:
    letters_amount = pass_len // 2
    digits_amount = pass_len - letters_amount

## Hur många speciella, måste kolla om det är fler än längden av password
## Då ska efter att ha generat ett password med siffror och bokstäver ska byta ut så många som skall bytas ut.
## Blir förstås lite ridiculous om har många men kan välja liksom en eller två is nice.
## Kan kanske ha det som %?
# special_signs = input("How many special charcthers?")

# letters = random.choices(string.ascii_uppercase, k=letters_amount)
letters = random.choices(string.ascii_letters, k=letters_amount) #ascii_letters för både upper och lower bokstäver
digits = random.choices(string.digits, k=digits_amount)
generated_pass = random.sample(digits + letters, pass_len)

print(''.join(generated_pass))
