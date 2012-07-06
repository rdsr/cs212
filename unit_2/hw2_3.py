# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def max_slice(palindromes):
    "Return the tuple which repesents the max slice representing a palindrome"
    l = r = 0
    for ((i, j), v) in palindromes.items():
        if v and j - i > r - l:
            l,r = i,j
    return (l,r+1)

def is_palindrome(text, i, j, palindromes):
    "Returns true if text[i:j+1] is a palindrome. Makes use of previously solved, cached subproblems"
    if j >= len(text):
        return False
    if j - i == 0:
        return True
    boundaries = text[i] == text[j]
    if j - i <= 2:
        return boundaries
    else:
        return boundaries and palindromes[i+1, j-1] == True

def fill_palindromes(text, palindromes, l):
    "fills 'palindromes' up with indices of palindromes of length l"
    for i in range(0, len(text)):
        j = i + l
        if is_palindrome(text, i, j, palindromes):
            palindromes[i,j] = True
        else:
            palindromes[i,j] = False


def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if len(text) == 0:
        return (0,0)

    palindromes = {}
    text = text.lower()
    for l in range(1, len(text)):
        fill_palindromes(text, palindromes, l)

    return max_slice(palindromes)

def Test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)

    return 'tests pass'

#print Test()
#print longest_subpalindrome_slice("Dennis, Nell, Edna, Leon, Nedra, Anita, Rolf, Nora, Alice, Carol, Leo, Jane, Reed, Dena, Dale, Basil, Rae, Penny, Lana, Dave, Denny, Lena, Ida, Bernadette, Ben, Ray, Lila, Nina, Jo, Ira, Mara, Sara, Mario, Jan, Ina, Lily, Arne, Bette, Dan, Reba, Diane, Lynn, Ed, Eva, Dana, Lynne, Pearl, Isabel, Ada, Ned, Dee, Rena, Joel, Lora, Cecil, Aaron, Flora, Tina, Arden, Noel and Ellen sinned")

print longest_subpalindrome_slice("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nunc libero, venenatis id porttitor et, pharetra et urna. Donec nec velit varius massa lacinia placerat. Fusce vulputate mollis nunc, et tincidunt erat imperdiet at. Aliquam sit amet tortor in sem tempor condimentum. Curabitur vel mauris lectus. Nulla at metus ac turpis malesuada accumsan vitae et arcu. Sed semper pellentesque est quis tristique. Mauris egestas porttitor risus, lobortis accumsan ligula sollicitudin eu. Ut sollicitudin nibh ac quam viverra id euismod velit posuere. Nullam ut ultrices arcu.Quisque et turpis massa, quis faucibus libero. Sed nulla nunc, pellentesque in congue id, dictum eget sem. Vivamus ultrices interdum velit ac pulvinar. Curabitur facilisis, purus nec commodo vulputate, purus magna dictum dolor, at fringilla arcu ante nec est. Nulla rutrum semper ullamcorper. Praesent fermentum ultrices sem id auctor. Sed eget euismod tortor. Vestibulum vestibulum, massa faucibus semper laoreet, dui arcu viverra turpis, eu rhoncus ante mauris suscipit velit. Phasellus vitae nisi molestie ligula eleifend fermentum at vel est. Aliquam quis erat massa, sit amet fringilla mi. Nulla ac dolor nisl. Pellentesque egestas felis id ante bibendum sed aliquet augue mollis. Maecenas condimentum lacinia mauris, ut egestas est bibendum quis. Donec vel sem nec turpis bibendum ultricies eget sed diam. Vestibulum sed metus vel ipsum convallis adipiscing.Nulla eu lacus eget est pellentesque pulvinar eu nec libero. Nullam orci ligula, consectetur eget adipiscing at, scelerisque quis neque. Curabitur tempor urna ac nisi placerat nec tincidunt magna pulvinar. Praesent id congue augue. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum pretium ullamcorper dolor sit amet consectetur. Curabitur vehicula ultricies commodo. In erat massa, condimentum nec elementum id, ullamcorper in felis.Integer nec imperdiet ante. Vestibulum pellentesque libero eget odio mollis at ullamcorper ipsum cursus. Curabitur quis justo a leo porta aliquam vitae eu nunc. In dolor sem, viverra non euismod at, auctor sit amet turpis. Phasellus convallis egestas dui, sed pharetra leo dignissim in. Praesent mi tortor, posuere ut gravida at, facilisis vel nisl. Integer orci metus, volutpat sit amet tincidunt eu, tincidunt vitae sapien. In imperdiet elementum lobortis. Vestibulum viverra augue eu urna vehicula feugiat. Aliquam sapien velit, posuere ut egestas at, bibendum nec risus. Vestibulum lacus elit, semper sit amet laoreet at, bibendum non risus.Duis turpis dolor, tincidunt sed condimentum ut, sodales vitae eros. Morbi urna odio, eleifend at adipiscing vitae, pretium ut mi. In consequat, tellus quis scelerisque aliquam, turpis metus sagittis mi, semper dapibus sem ligula et felis. Curabitur turpis ante, pretium id mollis vitae, fringilla nec turpis. In enim ligula, porta nec posuere quis, vestibulum ac justo. Vestibulum laoreet nisi ac magna accumsan aliquet. Pellentesque sed metus bibendum enim sodales rutrum. Nullam pretium arcu quis erat eleifend tempus. Suspendisse lacinia, est nec mollis lobortis, dui leo commodo nulla, a aliquam diam orci ut mauris. Aenean non purus in eros fermentum ultrices. In at libero dolor, ut venenatis ante. Phasellus turpis quam, laoreet at porta nec, gravida a erat. Morbi purus augue, fermentum non aliquet blandit, fermentum viverra tortor. Donec consequat sodales libero et venenatis. Nam a felis non massa aliquet pharetra dictum quis erat. ingirumimusnocteetconsumimurigni")
