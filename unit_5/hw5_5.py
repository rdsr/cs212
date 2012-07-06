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

@memo
def Pscore(state):
    (score, yard, cards) = state
    if not cards:
        return score + yard
    foxes = cards.count('F')
    if not foxes:
        return score + yard + len(cards)
    return max(Q(state, action) for action in ['gather', 'wait'])

def Q(state, action):
    (score, yard, cards) = state
    pH = P('H', cards)

    if action == 'gather':
        return Pscore((score + yard, 0, cards[1:]))

    if action == 'wait':
        return pH * Pscore((score, yard + 1, cards.replace('H', '', 1))) + (1 - pH) * Pscore((score, 0, cards.replace('F', '', 1)))

    raise ValueError

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)

    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def strategy(state):
    def EU(action): return Q(state, action)
    return max(['gather', 'wait'], key=EU)

def do(action, state):
    "Apply action to state, returning a new state."
    (score, yard, cards) = state
    cardno = random.randint(0,len(cards)-1)
    card = cards[cardno]
    cards = cards[:cardno] + cards[cardno+1:]
    if action == 'gather':
        score += yard
        yard = 0
        return (score, yard, cards)
    elif card == 'F':
        return (score, 0, cards)
    elif card == 'H':
        return (score, yard + 1, cards)
    raise ValueError

def average_score(strategy, N=1000):
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
