#!/usr/bin/python
# simple choose-your-own-adventure game
import sys, time, random
N = ['poop', 'toilet', 'dinosaur']
V = ['run', 'poop', 'pee']
A = ['smelly', 'dark', 'slimy', 'cold', 'disgusting']
LEVELS = [
    { 'intro' : 'You enter a room. There are many ways forward.\n', 'subs' : [], 'choices' : ['left', 'right', 'straight'] },
    { 'intro' : 'You are now on the roof. It is %s outside. You kind of want to %s but that is not an option. How do you want to proceed?\n', 'subs' : [A, V], 'choices' : ['look up', 'look at the next building over'] },
    { 'intro' : 'It is too %s to see clearly.\n', 'subs' : [A], 'choices' : ['go back inside through the door', 'climb back in through the window'] },
    { 'intro' : 'It was difficult, but you are back inside. You hear a noise from downstairs.\n', 'subs' : [], 'choices' : ['put your ear to the floor', 'go to the top of the stairs to listen'] },
    { 'intro' : 'It\'s music that you hear!\n', 'subs' : [], 'choices' : ['Start singing', 'Try to whistle'] },
]
FINAL_OUTCOMES = [lambda x : lambda : slow_print("you win\n"), lambda x : lambda : slow_print("you lose\n")]
OUTCOMES = FINAL_OUTCOMES + [lambda x : generate_dictionary(x)]
OUTCOME_ODDS = [3, 2, 8]
def slow_print(s):
    for letter in s: sys.stdout.write(letter) ; sys.stdout.flush() ; time.sleep(.04)
def mad_libs(s, sublists):
    return s % tuple([random.choice(sublist) for sublist in sublists])
def generate_dictionary(level):
    d = {}
    raw_sentence = LEVELS[level]['intro']
    subs = LEVELS[level]['subs']
    if len(subs) > 0:
        sentence = mad_libs(raw_sentence, subs)
    else:
        sentence = raw_sentence
    d['sentence']=sentence
    d['options']={}
    outcomes_raw = FINAL_OUTCOMES if level == len(LEVELS)-1 else OUTCOMES
    outcome_functions = []
    for i in range(0, len(outcomes_raw)):
        newelements = outcomes_raw[i:i+1] * OUTCOME_ODDS[i]
        outcome_functions = outcome_functions + newelements
    for choice in LEVELS[level]['choices']:
        subtree_value = random.choice(outcome_functions)(level+1)
        d['options'][choice] = subtree_value
    return d
def play_dict(d):
    slow_print(d['sentence'])
    slow_print("Here are your choices:\n")
    for k in d['options'].keys(): print k
    slow_print("choose carefully ==> ")
    choice = raw_input()
    while choice not in d['options'].keys():
        slow_print("please type carefully ==> ")
        choice = raw_input()
    subtree = d['options'][choice]
    if type(subtree) is dict:
        play_dict(subtree)
    else:
        subtree()
def main():
    #slow_print("")
    d = generate_dictionary(0)
    play_dict(d)
    #slow_print(mad_libs("You see a %s %s.\n", [A, N]))
main()
