# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart
# or diamond.
#
# The itertools library may be helpful. Feel free to
# define multiple functions if it helps you solve the
# problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

red_suits   = ['H', 'D']
black_suits = ['S', 'C']
ranks       = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'K', 'Q', 'A']

def get_wild_cards(hand):
    "Returns all the wildcards in a hand"
    return [card for card in hand if card.find("?") == 0]

def flatten(l):
    "Flattens a list"
    return [item for sublist in l for item in sublist]

def create_hand(hand, cards):
    """Creates a hand from a given hand with wild cards and some specific cards.
    The no of wild cards in hand is same as the number of cards in cards"""
    hand = list(hand)
    hand = [card for card in hand if card.find("?") == -1]
    hand.extend(cards)
    return hand

def contains_wild_cards(hand):
    return True if '?R' in hand or '?B' in hand else False

def get_suits(wild_cards):
    return flatten([red_suits if 'R' in wild_card else black_suits for wild_card in wild_cards])

def all_combinations(hand):
    "Returns all combinations of hand if it contains a wildcard."
    if contains_wild_cards(hand):
        wild_cards = get_wild_cards(hand)
        possible_suits = get_suits(wild_cards)
        possible_cards = [r+s for r,s in itertools.product(ranks, possible_suits)]
        return [create_hand(hand, cards) for cards in itertools.combinations(possible_cards, len(wild_cards))]
    else:
        return [hand]

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    all_hands = [list(_hand) for _hand in itertools.combinations(hand, 5)]
    all_hands = [all_combinations(_hand) for _hand in all_hands]
    all_hands = flatten(all_hands)
    all_hands = [_hand for _hand in all_hands if len(set(_hand)) == 5]
    return max(all_hands, key=hand_rank)

def test_internal_functions():
    assert (sorted(get_wild_cards("6C 7C 8C 9C TC 5C ?B".split()))
            == ['?B'])
    assert (sorted(get_wild_cards("6C 7C 8C 9C TC 5C 3D".split()))
            == [])
    assert (sorted(flatten([[1, 2], [3, 4], []]))
            == [1, 2, 3, 4])
    assert (sorted(create_hand("6C 7C 8C 9C TC 5C ?B".split(), ["6C"]))
            == sorted("6C 7C 8C 9C TC 5C 6C".split()))
    assert (sorted(create_hand("6C 7C 8C 9C TC ?B ?B".split(), ("6C", "7C")))
            == sorted("6C 7C 8C 9C TC 7C 6C".split()))
    assert (contains_wild_cards("6C 7C 8C 9C TC ?B ?B".split()) == True)
    assert (contains_wild_cards("6C 7C 8C 9C TC".split()) == False)
    assert (sorted(get_suits(["?R"]))
            == ["D", "H"])
    assert (sorted(get_suits(["?R", "?R"]))
            == ["D", "D", "H", "H"])
    assert (len(all_combinations("6C ?R".split()))
            == (len(ranks) * len(red_suits)))
    return 'test_internal_functions passes'

print test_internal_functions()

# ------------------
# Provided Functions
#
# You may want to use some of the functions which
# you have already defined in the unit to write
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

print test_best_wild_hand()
