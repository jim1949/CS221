import collections, sys, os
from logic import *

############################################################
# Problem 1: propositional logic
# Convert each of the following natural language sentences into a propositional
# logic formula.  See rainWet() in examples.py for a relevant example.

# Sentence: "If it's summer and we're in California, then it doesn't rain."
def formula1a():
    # Predicates to use:
    Summer = Atom('Summer')  # whether it's summer
    California = Atom('California')  # whether we're in California
    Rain = Atom('Rain')  # whether it's raining
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Implies(And(Summer, California), Not(Rain))
    # END_YOUR_CODE

# Sentence: "It's wet if and only if it is raining or the sprinklers are on."
def formula1b():
    # Predicates to use:
    Rain = Atom('Rain')  # whether it is raining
    Wet = Atom('Wet')  # whether it it wet
    Sprinklers = Atom('Sprinklers')  # whether the sprinklers are on
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Equiv(Wet, Or(Rain, Sprinklers))
    # END_YOUR_CODE

# Sentence: "Either it's day or night (but not both)."
def formula1c():
    # Predicates to use:
    Day = Atom('Day')  # whether it's day
    Night = Atom('Night')  # whether it's night
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Or(And(Day, Not(Night)) , And(Not(Day), Night))
    # END_YOUR_CODE

############################################################
# Problem 2: first-order logic

# Sentence: "Every person has a mother."
def formula2a():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person
    def Mother(x, y): return Atom('Mother', x, y)  # whether x's mother is y
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Forall('$x', Implies(Person('$x'), Exists('$y', Mother('$x', '$y'))))
    # END_YOUR_CODE

# Sentence: "At least one person has no children."
def formula2b():
    # Predicates to use:
    def Person(x): return Atom('Person', x)  # whether x is a person
    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y
    # BEGIN_YOUR_CODE (around 1 line of code expected)
    return Exists('$x', And(Person('$x'), Not(Exists('$y', Child('$x', '$y')))))
    # END_YOUR_CODE

# Return a formula which defines Daughter in terms of Female and Child.
# See parentChild() in examples.py for a relevant example.
def formula2c():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female
    def Child(x, y): return Atom('Child', x, y)  # whether x has a child y
    def Daughter(x, y): return Atom('Daughter', x, y)  # whether x has a daughter y
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return Forall('$x', Forall('$y', Equiv(Daughter('$x', '$y'), And(Child('$x', '$y'), Female('$y')))))
    # END_YOUR_CODE

# Return a formula which defines Grandmother in terms of Female and Parent.
# Note: It is ok for a person to be her own parent
def formula2d():
    # Predicates to use:
    def Female(x): return Atom('Female', x)  # whether x is female
    def Parent(x, y): return Atom('Parent', x, y)  # whether x has a parent y
    def Grandmother(x, y): return Atom('Grandmother', x, y)  # whether x has a grandmother y
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return Forall('$x', Forall('$z', Equiv(Grandmother('$x', '$z'), Exists('$y', AndList([Female('$z'), Parent('$x', '$y'), Parent('$y', '$z')])))))
    # END_YOUR_CODE

############################################################
# Problem 3: Liar puzzle

# Facts:
# 0. John: "It wasn't me!"
# 1. Susan: "It was Nicole!"
# 2. Mark: "No, it was Susan!"
# 3. Nicole: "Susan's a liar."
# 4. Exactly one person is telling the truth.
# 5. Exactly one person crashed the server.
# Query: Who did it?
# This function returns a list of 6 formulas corresponding to each of the
# above facts.
# Hint: You might want to use the Equals predicate, defined in logic.py.  This
# predicate is used to assert that two objects are the same.
# In particular, Equals(x,x) = True and Equals(x,y) = False if x is not equal to y.
def liar():
    def TellTruth(x): return Atom('TellTruth', x)
    def CrashedServer(x): return Atom('CrashedServer', x)
    john = Constant('john')
    susan = Constant('susan')
    nicole = Constant('nicole')
    mark = Constant('mark')
    formulas = []
    # We provide the formula for fact 0 here.
    formulas.append(Equiv(TellTruth(john), Not(CrashedServer(john))))
    # You should add 5 formulas, one for each of facts 1-5.
    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    formulas.append(Equiv(TellTruth(susan), CrashedServer(nicole)))
    formulas.append(Equiv(TellTruth(mark), CrashedServer(susan)))
    formulas.append(Equiv(TellTruth(nicole), Not(TellTruth(susan))))
    formulas.append(Exists('$x', And(TellTruth('$x'), Forall('$y', Implies(Not(Equals('$x', '$y')) , Not(TellTruth('$y')))))))
    formulas.append(Exists('$x', And(CrashedServer('$x'), Forall('$y', Implies(Not(Equals('$x', '$y')) , Not(CrashedServer('$y')))))))
    # END_YOUR_CODE
    query = CrashedServer('$x')
    return (formulas, query)

############################################################
# Problem 5: Odd and even integers

# Return the following 6 laws:
# 0. Each number $x$ has a unique successor, which is not equal to $x$.
# 1. Each number is either even or odd, but not both.
# 2. The successor number of an even number is odd.
# 3. The successor number of an odd number is even.
# 4. For every number $x$, the successor of $x$ is larger than $x$.
# 5. Larger is a transitive property: if $x$ is larger than $y$ and $y$ is
#    larger than $z$, then $x$ is larger than $z$.
# Query: For each number, there exists an even number larger than it.
def ints():
    def Even(x): return Atom('Even', x)  # whether x is even
    def Odd(x): return Atom('Odd', x)  # whether x is odd
    def Successor(x, y): return Atom('Successor', x, y)  # whether x's successor is y
    def Larger(x, y): return Atom('Larger', x, y)  # whether x is larger than y
    # Note: all objects are numbers, so we don't need to define Number as an
    # explicit predicate.
    # Note: pay attention to the order of arguments of Successor and Larger.
    # Populate |formulas| with the 6 laws above and set |query| to be the
    # query.
    # Hint: You might want to use the Equals predicate, defined in logic.py.  This
    # predicate is used to assert that two objects are the same.
    formulas = []
    query = None
    # BEGIN_YOUR_CODE (around 25 lines of code expected)
# 0. Each number $x$ has a unique successor, which is not equal to $x$.
    cond1 = Not(Equals('$y', '$x'))
    cond2 = Forall('$z', Implies(Not(Equals('$y', '$z')), Not(Successor('$x', '$z'))))
    cond = Exists('$y', AndList([Successor('$x', '$y'), cond1, cond2]))
    formulas.append(Forall('$x', cond))
# 1. Each number is either even or odd, but not both.
    cond = Or(And(Even('$x'), Not(Odd('$x'))), And(Odd('$x'), Not(Even('$x'))))
    formulas.append(Forall('$x', cond))
# 2. The successor number of an even number is odd.
    cond = And(Even('$x'), Successor('$x', '$y'))
    result = Odd('$y')
    formulas.append(Forall('$x', Forall('$y', Implies(cond, result))))
# 3. The successor number of an odd number is even.
    cond = And(Odd('$x'), Successor('$x', '$y'))
    result = Even('$y')
    formulas.append(Forall('$x', Forall('$y', Implies(cond, result))))
# 4. For every number $x$, the successor of $x$ is larger than $x$.
    cond = Successor('$x', '$y')
    result = Larger('$y', '$x')
    formulas.append(Forall('$x', Forall('$y', (Implies(cond, result)))))
# 5. Larger is a transitive property: if $x$ is larger than $y$ and $y$ is
#    larger than $z$, then $x$ is larger than $z$.
    cond1 = Larger('$x', '$y')
    cond2 = Larger('$y', '$z')
    result = Larger('$x', '$z')
    formulas.append(Forall('$x', Forall('$y', Forall('$z', (Implies(And(cond1, cond2), result))))))

    # END_YOUR_CODE
    # For part (b), your job is to show that adding the following formula
    # would result in a contradiction for finite domains.
    # formulas.append(Forall('$x', Not(Larger('$x', '$x'))))
    query = Forall('$x', Exists('$y', And(Even('$y'), Larger('$y', '$x'))))
    return (formulas, query)

############################################################
# Problem 6: (Extra Credit)
# Write a parser for our natural language interface.

from nlparser import GrammarRule, getCategoryProcessor

def createLanguageProcessor():
    # Defines a mapping from each in-domain word to its word class.
    # This automatically creates rules such as
    #   $Noun -> cat
    # with the string "cat" as the denotation
    categories = {
        'Noun': ['cat', 'tabby', 'dog', 'hound', 'dolphin', 'mammal', 'leg', 'foot', 'tail', 'fin'],
        'Name': ['Garfield', 'Pluto'],
        }
    return getCategoryProcessor(categories)

def createNLIGrammar():
    # Add your rules to the provided variable named rules.
    # Three examples are provided for you.
    # Please see nli.py for more information on the GrammarRule class.
    # IMPORTANT: Name all added variables '$x' (or '$y if necessary')
    rules = []

    # Parse if it's a question or statement.
    rules.append(GrammarRule('$ROOT', ['$Statement'], lambda args: ('tell', args[0])))
    rules.append(GrammarRule('$ROOT', ['$Question'], lambda args: ('ask', args[0])))
    rules.append(GrammarRule('$Statement', ['$Clause', '.'], lambda args: args[0]))
    rules.append(GrammarRule('$Question', ['$Clause', '?'], lambda args: args[0]))

    # (1) every X is a Y.
    rules.append(GrammarRule('$Clause', ['every', '$Noun', 'is', 'a', '$Noun'],
        lambda args: Forall('$x', Implies(Atom(args[0].title(), '$x'), Atom(args[1].title(), '$x')))))

    # (2) X is a Y.
    rules.append(GrammarRule('$Clause', ['$Name', 'is', 'a', '$Noun'],
        lambda args: Atom(args[1].title(), args[0].lower())))

    # (3) is X a Y?
    rules.append(GrammarRule('$Question', ['is', '$Clause-be', '?'],
        lambda args: args[0]))
    rules.append(GrammarRule('$Clause-be', ['$Name', 'a', '$Noun'],
        lambda args: Atom(args[1].title(), args[0].lower())))

    # BEGIN_YOUR_CODE (around 15 lines of code expected)
    def Has(x, y): return Atom('Has', x, y)  # whether x is larger than y
    # (1) every X has a Y.
    # should use '$Noun' and args[0].title()
    # all X, Y and Z categories i.e. they should be processed with title()

    rules.append(GrammarRule('$Clause', ['every', '$Noun' , 'has' , 'a' , '$Noun'], \
                             lambda args: Forall('$x', Implies(Atom(args[0].title(), '$x'), Exists('$y', And(Atom(args[1].title(), '$y'), Has('$x', '$y')))))))

#     return Forall('$x', Implies(Person('$x'), Exists('$y', Mother('$x', '$y'))))

    # (2) no X has a Y.
    rules.append(GrammarRule('$Clause', ['no', '$Noun' , 'has' , 'a' , '$Noun'] ,
                             lambda args: Not(Exists('$x', Implies(Atom(args[0].title(), '$x'), Exists('$y', And(Atom(args[1].title(), '$y'), Has('$x', '$y'))))))))

    # (3) if a X has a Y, then it has a Z.
    rules.append(GrammarRule('$Clause', ['if', 'a', '$Noun', 'has', 'a', '$Noun' , ',', 'then', 'it', 'has', 'a', '$Noun'],
                             lambda args:  Forall('$x', Forall('$y', Implies(AndList([ Atom(args[0].title(), '$x'), Atom(args[1].title(), '$y'), Has('$x', '$y')]) , Exists('$z', And(Atom(args[2].title(), '$z') , Has('$x', '$z'))))))))

    # END_YOUR_CODE
    return rules