"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
    one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

def day_after(person_a, person_b):
    "Returns true of 'a' arrives a day after 'b'"
    return person_a - person_b == 1

def arrival_order(days, people):
    order = list(people)
    for day in days:
        order[day - 1] = people.pop(0)
    return order

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed

    Monday, Tuesday, Wednesday, Thursday, Friday = range(1, 6)

    orderings = list(itertools.permutations([1, 2, 3, 4, 5]))
    days = [(Hamming, Knuth, Minsky, Simon, Wilkes)
           for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
           if day_after(Knuth, Simon)
           for (programmer, writer, manager, designer, _) in orderings
           if (programmer is not Wilkes) and (writer is not Minsky) and (Thursday is not designer) and day_after(Knuth, manager)
           for (laptop, droid, tablet, iphone, _) in orderings
           if (laptop is Wednesday) and ((programmer is Wilkes and droid is Hamming) or (programmer is Hamming and droid is Wilkes)) and (Knuth is not manager and tablet is not manager) and (Friday is not tablet) and (designer is not droid) and ((laptop is Monday and Wilkes is writer) or (laptop is writer and Wilkes is Monday)) and (iphone is Tuesday or tablet is Tuesday)
           ]

    return arrival_order(days[0], ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes'])


print logic_puzzle()
