import random
from functools import update_wrapper

def decorator(d):
    def decorated(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(decorated, d)
    return decorated

@decorator
def memo(fn):
    cache = {}

    def decorated(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = fn(*args)
            return result
        except TypeError:
            return fn(*args)

    return decorated

def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    score, yard, cards = state

    next_card_index = random.randint(0, len(cards) - 1)
    next_card = cards[next_card_index]
    cards = cards[:next_card_index] + cards[next_card_index + 1:]

    if 'wait' == action:
        return (score, 0, cards) if next_card == 'F' else (score, yard + 1, cards)

    if 'gather' == action:
        return (score + yard, 0, cards)

    raise ValueError('Invalid action {}'.format(action))

def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    return average_score(A) - average_score(B) > 1.5

def strategy(state):
    score, yard, cards = state
    if 'F' not in cards or yard < 1: return 'wait'
    return best_action(state)

def best_action(state):
    """"""
    def best_quality(action): return quality(state, action)
    return max(valid_actions(state), key=best_quality)

def P(e, cards):
    return cards.count(e) / float(len(cards))

def quality(state, action):
    score, yard, cards = state

    if 'gather' == action:
        return utility( do_sim(state, 'gather') )

    if 'wait' == action:
        pH = P('H', cards)
        return pH * utility((score, yard + 1, cards.replace('H', '', 1))) + (1 - pH) * utility((score, 0, cards.replace('H', '', 1)))

@memo
def utility(state):
    score, yard, cards = state
    if not cards:
        return score + yard
    elif 'H' not in cards:
        return score
    elif 'F' not in cards:
        return score + yard + len(cards)
    return max(quality(state, action) for action in valid_actions(state))

def do_sim(state, action, card = None):
    score, yard, cards = state

    next_card_index = cards.index(card) if card else random.randint(0, len(cards) - 1)
    next_card = cards[next_card_index]
    new_cards = cards[:next_card_index] + cards[next_card_index + 1:]

    if 'gather' == action: return (score + yard, 0, new_cards)

    if 'wait' == action:
        return (score, 0, new_cards) if 'F' == next_card else (score, yard + 1, new_cards)

def valid_actions(state):
    _, yard, cards = state
    return ['wait'] if yard == 0 else ['gather'] if cards == 0 else ['gather', 'wait']

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or
            gather == (9, 0, 'F'*4 + 'H'*9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    return 'tests pass'

print average_score(strategy)
print test()
