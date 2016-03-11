import collections

############################################################
# Problem 3a

def computeMaxWordLength(text):
    """
    Given a string |text|, return the longest word in |text|.  If there are
    ties, choose the word that comes latest in the alphabet. There won't be 
    puctuations and there will only be splits on spaces. You might find
    max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)    

    return max(text.split(), key = lambda word: (len(word), word))
    
    # END_YOUR_CODE

print computeMaxWordLength('which is zhich zzngest longest the aongest word')
############################################################
# Problem 3b

def createExistsFunction(text):
    """
    Given a text, return a function f, where f(word) returns whether |word|
    occurs in |text| or not.  f should run in O(1) time.  You might find it
    useful to use set().
    """
    # BEGIN_YOUR_CODE (around 4 lines of code expected)
    word_set = set(text.split())
    def f(word):
        return word in word_set
    return f
    # END_YOUR_CODE

# func = createExistsFunction('the   quick brown fox jumps over the lazy fox lazy')
# print func('lazy ')
# print func('')
############################################################
# Problem 3c

def manhattanDistance(loc1, loc2):
    """
    Return the Manhattan distance between two locations, where locations are
    pairs (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return abs(loc1[0]-loc2[0])+abs(loc1[1]-loc2[1])
    # END_YOUR_CODE

# print manhattanDistance((3, 5), (1, 9))
############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as Counters, return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    """
    # BEGIN_YOUR_CODE (around 4 lines of code expected)    
    key_list = [v1[key]*v2[key] for key in v1 if key in v2]
    # print key_list
    return sum(key_list)
    # END_YOUR_CODE
# print sparseVectorDotProduct(collections.Counter({'a': 5, 'b':8, 'c':1}), collections.Counter({'a': 3, 'c':9,  'b': 2}))
############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    """
    # BEGIN_YOUR_CODE (around 2 lines of code expected)
    for key in v2:
        v1[key] += scale * v2[key]
    # END_YOUR_CODE

v = collections.Counter({'a': 5, 'b':1, 'c':-6})
incrementSparseVector(v, 1, collections.Counter({'d':-8}))
# incrementSparseVector(v, 1, collections.Counter({'c': 3, 'd':2}))
print v
############################################################
# Problem 3f

def computeMostFrequentWord(text):
    """
    Splits the string |text| by whitespace and returns two things as a pair: 
        the set of words that occur the maximum number of times, and
	their count, i.e.
	(set of words that occur the most number of times, that maximum number/count)
    You might find it useful to use collections.Counter().
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
     
    word_counter = collections.Counter(text.split())
    cnt_max = max( [word_counter[key] for key in word_counter] )

    return (set([key for key in word_counter if word_counter[key] == cnt_max]), cnt_max)
    # END_YOUR_CODE


# print computeMostFrequentWord('a')
############################################################
# Problem 3g

def computeLongestPalindrome(text):    
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (around 19 lines of code expected)
    cache = {}
    def fun(i, j):
        if (i,j) in cache:
            return cache[(i,j)]
        if (i>j):
            ans = 0
        elif (i==j):
            ans = 1
        elif (text[i] == text[j]):            
            ans = fun(i+1, j-1) + 2            
        else:
            ans = max(fun(i, j-1), fun(i+1, j))
        cache[(i,j)] = ans
        return ans

    if (len(text) == 0):
        return 0
    else:
        return fun(0, len(text)-1)

# print computeLongestPalindrome("ab"*800)


    # END_YOUR_CODE
