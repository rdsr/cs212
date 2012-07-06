# -----------------
# User Instructions
#
# This problem deals with the one-player game foxes_and_hens. This
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'.
#
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions,
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card.
#
# Your job is to define two functions. The first is do(action, state),
# where action is either 'gather' or 'wait' and state is a tuple of
# (score, yard, cards). This function should return a new state with
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an
# action based on the state. This strategy should average at least
# 1.5 more points than the take5 strategy.

import random
from functools import update_wrapper

## code for best strategy begin...
def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f

def P(e, cards):
    return cards.count(e) / float(len(cards))

def Q(state, action):
    (score, yard, cards) = state
    pH = P('H', cards)
    if action == "gather":
        return pH * U((score + yard, 0, cards.replace('H', '', 1))) + (1 - pH) * U((score + yard, 0, cards.replace('F', '', 1)))
    else:
        return pH * U((score, yard + 1, cards.replace('H', '', 1))) + (1 - pH) * U((score, 0, cards.replace('F', '', 1)))

@memo
def U(state):
    (score, yard, cards) = state
    if len(cards) == 0:
        return score + yard
    elif 'H' not in cards:
        return score + yard
    elif 'F' not in cards:
        return score + yard + len(cards)
    else:
        return max(Q(state, action) for action in actions(state))

def actions(state):
    (_, _, cards) = state
    return ["gather", "wait"] if len(cards) > 0 else ["gather"]

def best_action(state):
    "Return the optimal action for a state, given U."
    def EU(action):
        return Q(state, action)
    return max(actions(state), key=EU)

def max_score(state):
    return best_action(state)

## code for best strategy end...

def shuffle(cards):
    cards = list(cards)
    random.shuffle(cards)
    return "".join(cards)

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, shuffle('F'*foxes + 'H'*hens))

    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    (score, yard, cards) = state
    cards_left = cards[1:]
    if action == 'gather':
        return (score + yard, 0, cards_left)
    elif cards[0] == 'H' and action == 'wait':
        return (score, yard + 1, cards_left)
    elif cards[0] == 'F' and action == 'wait':
        return (score, 0, cards_left)
    else:
        return state

# various strategies
def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def take(n):
    def _takeN(state):
        "A strategy that waits until there are N hens in yard, then gathers."
        (score, yard, cards) = state
        if yard < n:
            return 'wait'
        else:
            return 'gather'
    return _takeN

def wait_conditionally(state):
    (score, yard, cards) = state
    if 'F' not in cards:
        return 'wait'
    else:
        return take(3)(state)

strategy = wait_conditionally

def average_score(strategy, N=10):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5, verbose=True):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    SA = average_score(A)
    SB = average_score(B)
    if verbose:
        print "average score for strategy A: " + str(SA)
        print "average score for strategy B: " + str(SB)

    return SA - SB > 1.5

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or
            gather == (9, 0, 'F'*4 + 'H'*9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    return 'tests pass'

#print average_score(strategy)
print test();
