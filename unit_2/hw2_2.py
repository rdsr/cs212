#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?
#
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay,
# Liskov, Perlis, and Ritchie.

def nextto(f1, f2):
    "Two floors are next to each other if they differ by 1."
    return abs(f1-f2) == 1

import itertools

def floor_puzzle():
    orderings = list(itertools.permutations([1,2,3,4,5]))
    return list(next((Hopper, Kay, Liskov, Perlis, Ritchie)
                     for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
                     if Hopper != 5 and
                     Kay != 1 and
                     Liskov != 5 and Liskov != 1 and
                     Perlis > Kay and
                     not nextto(Ritchie, Liskov) and
                     not nextto(Liskov, Kay)))

print next(floor_puzzle())
