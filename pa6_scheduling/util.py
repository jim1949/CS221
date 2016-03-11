import json, re

# General code for representing a weighted CSP (Constraint Satisfaction Problem).
# All variables are being referenced by their index instead of their original
# names.
class CSP:
    def __init__(self):
        # Total number of variables in the CSP.
        self.numVars = 0

        # The list of variable names in the same order as they are added. A
        # variable name can be any hashable objects, for example: int, str,
        # or any tuple with hashtable objects.
        self.varNames = []

        # Each entry is the list of domain values that its corresponding
        # variable can take on.
        # E.g. if B \in ['a', 'b'] is the second variable
        # then valNames[1] == ['a', 'b']
        self.valNames = []

        # Each entry is a unary potential table for the corresponding variable.
        # The potential table corresponds to the weight distribution of a variable
        # for all added unary potential functions. The table itself is a list
        # that has the same length as the variable's domain. If there's no
        # unary function, this table is stored as a None object.
        # E.g. if B \in ['a', 'b'] is the second variable, and we added two
        # unary potential functions f1, f2 for B,
        # then unaryPotentials[1][0] == f1('a') * f2('a')
        self.unaryPotentials = []

        # Each entry is a dictionary keyed by the index of the other variable
        # involved. The value is a binary potential table, where each table
        # stores the potential value for all possible combinations of
        # the domains of the two variables for all added binary potneital
        # functions. The table is represented as a 2D list, with size
        # dom(var) x dom(var2).
        #
        # As an example, if we only have two variables
        # A \in ['b', 'c'],  B \in ['a', 'b']
        # and we've added two binary functions f1(A,B) and f2(A,B) to the CSP,
        # then binaryPotentials[0][1][0][0] == f1('b','a') * f2('b','a').
        # binaryPotentials[0][0] should return a key error since a variable
        # shouldn't have a binary potential table with itself.
        #
        # One important thing to note here is that the indices in the potential
        # tables are indexed with respect to its variable's domain. Hence, 'b'
        # will have an index of 0 in A, but an index of 1 in B. Conversely, the
        # first value for A and B may not necessarily represent the same thing.
        # Beaware of the difference when implementing your CSP solver.
        self.binaryPotentials = []

    def add_variable(self, varName, domain):
        """
        Add a new variable to the CSP.
        """
        if varName in self.varNames:
            raise Exception("Variable name already exists: %s" % str(varName))
        var = len(self.varNames)
        self.numVars += 1
        self.varNames.append(varName)
        self.valNames.append(domain)
        self.unaryPotentials.append(None)
        self.binaryPotentials.append(dict())

    def get_neighbor_vars(self, var):
        """
        Returns a list of indices of variables which are neighbors of
        the variable of indec |var|.
        """
        return self.binaryPotentials[var].keys()

    def add_unary_potential(self, varName, potentialFunc):
        """
        Add a unary potential function for a variable. Its potential
        value across the domain will be *merged* with any previously added
        unary potential functions through elementwise multiplication.

        How to get unary potential value given a variable index |var| and
        value index |val|?
        => csp.unaryPotentials[var][val]
        """
        try:
            var = self.varNames.index(varName)
        except ValueError:
            if isinstance(varName, int):
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                print '!! Tip:                                                                       !!'
                print '!! It seems you trying to add a unary potential with variable index...        !!'
                print '!! When adding a potential, you should use variable names.                    !!'
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            raise

        potential = [float(potentialFunc(val)) for val in self.valNames[var]]
        if self.unaryPotentials[var] is not None:
            assert len(self.unaryPotentials[var]) == len(potential)
            self.unaryPotentials[var] = [self.unaryPotentials[var][i] * \
                potential[i] for i in range(len(potential))]
        else:
            self.unaryPotentials[var] = potential

    def add_binary_potential(self, varName1, varName2, potential_func):
        """
        Takes two variable names and a binary potential function
        |potentialFunc|, add to binaryPotentials. If the two variables already
        had binaryPotentials added earlier, they will be *merged* through element
        wise multiplication.

        How to get binary potential value given a variable index |var1| with value
        index |val1| and variable index |var2| with value index |val2|?
        => csp.binaryPotentials[var1][var2][val1][val2]
        """
        try:
            var1 = self.varNames.index(varName1)
            var2 = self.varNames.index(varName2)
        except ValueError:
            if isinstance(varName1, int) or isinstance(varName2, int):
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                print '!! Tip:                                                                       !!'
                print '!! It seems you trying to add a binary potential with variable indices...     !!'
                print '!! When adding a potential, you should use variable names.                    !!'
                print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            raise

        self.update_binary_potential_table(var1, var2,
            [[float(potential_func(val1, val2)) \
                for val2 in self.valNames[var2]] for val1 in self.valNames[var1]])
        self.update_binary_potential_table(var2, var1, \
            [[float(potential_func(val1, val2)) \
                for val1 in self.valNames[var1]] for val2 in self.valNames[var2]])

    def update_binary_potential_table(self, var1, var2, table):
        """
        Private method you can skip for 0c, might be useful for 1c though.
        Update the binary potential table for binaryPotentials[var1][var2].
        If it exists, element-wise multiplications will be performed to merge
        them together.
        """
        if var2 not in self.binaryPotentials[var1]:
            self.binaryPotentials[var1][var2] = table
        else:
            currentTable = self.binaryPotentials[var1][var2]
            assert len(table) == len(currentTable)
            assert len(table[0]) == len(currentTable[0])
            for i in range(len(table)):
                for j in range(len(table[i])):
                    currentTable[i][j] *= table[i][j]

############################################################
# CSP examples.

def create_map_coloring_csp():
    """
    A classic CSP of coloring the map of Australia with 3 colors.
    """
    csp = CSP()
    provinces = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    neighbors = {
        'SA' : ['WA', 'NT', 'Q', 'NSW', 'V'],
        'NT' : ['WA', 'Q'],
        'NSW' : ['Q', 'V']
    }
    colors = ['red', 'blue', 'green']
    def are_neighbors(a, b):
        return (a in neighbors and b in neighbors[a]) or \
            (b in neighbors and a in neighbors[b])

    # Add the variables and binary potentials
    for p in provinces:
        csp.add_variable(p, colors)
    for p1 in provinces:
        for p2 in provinces:
            if are_neighbors(p1, p2):
                # Neighbors cannot have the same color
                csp.add_binary_potential(p1, p2, lambda x, y : x != y)
    return csp

def create_weighted_csp():
    """
    An example demonstrating how to create a weighted CSP.
    """
    csp = CSP()
    csp.add_variable('A', [1, 2, 3])
    csp.add_variable('B', [1, 2, 3, 4, 5])
    csp.add_unary_potential('A', lambda x : x > 1)
    csp.add_unary_potential('A', lambda x : x != 2)
    csp.add_unary_potential('B', lambda y : 1.0 / y)
    csp.add_binary_potential('A', 'B', lambda x, y : x != y)
    return csp


############################################################
# Course scheduling specifics.

# Information about a course:
# - self.cid: course ID (e.g., CS221)
# - self.name: name of the course (e.g., Artificial Intelligence)
# - self.quarters: quarters without the years (e.g., Aut)
# - self.minUnits: minimum allowed units to take this course for (e.g., 3)
# - self.maxUnits: maximum allowed units to take this course for (e.g., 3)
# - self.prereqs: list of course IDs that must be taken before taking this course.
class Course:
    def __init__(self, info):
        self.__dict__.update(info)

    # Return whether this course is offered in |quarter| (e.g., Aut2013).
    def is_offered_in(self, quarter):
        return any(quarter.startswith(q) for q in self.quarters)

    def short_str(self): return '%s: %s' % (self.cid, self.name)

    def __str__(self):
        return 'Course{cid: %s, name: %s, quarters: %s, units: %s-%s, prereqs: %s}' % (self.cid, self.name, self.quarters, self.minUnits, self.maxUnits, self.prereqs)


# Information about all the courses
class CourseBulletin:
    def __init__(self, coursesPath):
        """
        Initialize the bulletin.

        @param coursePath: Path of a file containing all the course information.
        """
        # Read courses (JSON format)
        self.courses = {}
        info = json.loads(open(coursesPath).read())
        for courseInfo in info.values():
            course = Course(courseInfo)
            self.courses[course.cid] = course

# A request to take one of a set of courses at some particular times.
class Request:
    def __init__(self, cids, quarters, prereqs, weight):
        """
        Create a Request object.

        @param cids: list of courses from which only one is chosen.
        @param quarters: list of strings representing the quarters (e.g. Aut2013)
            the course must be taken in.
        @param prereqs: list of strings representing courses pre-requisite of
            the requested courses separated by comma. (e.g. CS106,CS103,CS109)
        @param weight: real number denoting how much the student wants to take
            this/or one the requested courses.
        """
        self.cids = cids
        self.quarters = quarters
        self.prereqs = prereqs
        self.weight = weight

    def __str__(self):
        return 'Request{%s %s %s %s}' % \
            (self.cids, self.quarters, self.prereqs, self.weight)

    def __eq__(self, other): return str(self) == str(other)

    def __hash__(self): return hash(str(self))

    def __repr__(self): return str(self)

# Given the path to a preference file and a
class Profile:
    def __init__(self, bulletin, prefsPath):
        """
        Parses the preference file and generate a student's profile.

        @param prefsPath: Path to a txt file that specifies a student's request
            in a particular format.
        """
        self.bulletin = bulletin

        # Read preferences
        self.minUnits = 9  # minimum units per quarter
        self.maxUnits = 12  # maximum units per quarter
        self.quarters = []  # (e.g., Aut2013)
        self.taken = set()  # Courses that we've taken
        self.requests = []
        for line in open(prefsPath):
            m = re.match('(.*)\\s*#.*', line)
            if m: line = m.group(1)
            line = line.strip()
            if len(line) == 0: continue

            # Units
            m = re.match('minUnits (.+)', line)
            if m:
                self.minUnits = int(m.group(1))
                continue
            m = re.match('maxUnits (.+)', line)
            if m:
                self.maxUnits = int(m.group(1))
                continue

            # Register a quarter (quarter, year)
            m = re.match('register (.+)', line)
            if m:
                quarter = m.group(1)
                m = re.match('(Aut|Win|Spr|Sum)(\d\d\d\d)', quarter)
                if not m:
                    raise Exception("Invalid quarter '%s', want something like Spr2013" % quarter)
                self.quarters.append(quarter)
                continue

            # Already taken a course
            m = re.match('taken (.+)', line)
            if m:
                cid = self.ensure_course_id(m.group(1))
                self.taken.add(cid)
                continue

            # Request to take something
            m = re.match('request (\w+)(.*)', line)
            if m:
                cids = [self.ensure_course_id(m.group(1))]
                quarters = []
                prereqs = []
                weight = 1  # Default: would want to take
                args = m.group(2).split()
                for i in range(0, len(args), 2):
                    if args[i] == 'or':
                        cids.append(self.ensure_course_id(args[i + 1]))
                    elif args[i] == 'after':  # Take after a course
                        prereqs = [self.ensure_course_id(c) for c in args[i + 1].split(',')]
                    elif args[i] == 'in':  # Take in a particular quarter
                        quarters = [self.ensure_quarter(q) for q in args[i + 1].split(',')]
                    elif args[i] == 'weight':  # How much is taking this class worth
                        weight = float(args[i + 1])
                    elif args[i].startswith('#'):  # Comments
                        break
                    else:
                        raise Exception("Invalid arguments: %s" % args)
                self.requests.append(Request(cids, quarters, prereqs, weight))
                continue

            raise Exception("Invalid command: '%s'" % line)

        # Determine any missing prereqs and validate the request.
        self.taken = set(self.taken)
        self.taking = set()

        # Make sure each requested course is taken only once
        for req in self.requests:
            for cid in req.cids:
                if cid in self.taking:
                    raise Exception("Cannot request %s more than once" % cid)
            self.taking.update(req.cids)

        # Make sure user-designated prerequisites are requested
        for req in self.requests:
            for prereq in req.prereqs:
                if prereq not in self.taking:
                    raise Exception("You must take " + prereq)

        # Add missing prerequisites if necessary
        for req in self.requests:
            for cid in req.cids:
                course = self.bulletin.courses[cid]
                for prereq_cid in course.prereqs:
                    if prereq_cid in self.taken:
                        continue
                    elif prereq_cid in self.taking:
                        if prereq_cid not in req.prereqs:
                            req.prereqs.append(prereq_cid)
                            print "INFO: Additional prereqs inferred: %s after %s" % \
                                (cid, prereq_cid)
                    else:
                        print "WARNING: missing prerequisite of %s -- %s; you should add it as 'taken' or 'request'" % \
                            (cid, self.bulletin.courses[prereq_cid].short_str())

    def print_info(self):
        print "Units: %d-%d" % (self.minUnits, self.maxUnits)
        print "Quarter: %s" % self.quarters
        print "Taken: %s" % self.taken
        print "Requests:"
        for req in self.requests: print '  %s' % req

    def ensure_course_id(self, cid):
        if cid not in self.bulletin.courses:
            raise Exception("Invalid course ID: '%s'" % cid)
        return cid

    def ensure_quarter(self, quarter):
        if quarter not in self.quarters:
            raise Exception("Invalid quarter: '%s'" % quarter)
        return quarter

def extract_course_scheduling_solution(profile, assign):
    """
    Given an assignment returned from the CSP solver, reconstruct the plan. It
    is assume that (req, quarter) is used as the variable to indicate if a request
    is being assigned to a speific quarter, and (quarter, cid) is used as the variable
    to indicate the number of units the course should be taken in that quarter.

    @param profile: A student's profile and requests
    @param assign: An assignment of your variables as generated by the CSP
        solver.

    @return result: return a list of (quarter, courseId, units) tuples according
        to your solution sorted in chronological of the quarters provided.
    """
    result = []
    if not assign: return result
    for quarter in profile.quarters:
        for req in profile.requests:
            cid = assign[(req, quarter)]
            if cid == None: continue
            if (cid, quarter) not in assign:
                result.append((quarter, cid, None))
            else:
                result.append((quarter, cid, assign[(cid, quarter)]))
    return result

def print_course_scheduling_solution(solution):
    """
    Print a schedule in a nice format based on a solution.

    @para solution: A list of (quarter, course, units). Units can be None, in which
        case it won't get printed.
    """

    if solution == None:
        print "No schedule found that satisfied all the constraints."
    else:
        print "Here's the best schedule:"
        print "Quarter\t\tUnits\tCourse"
        for quarter, course, units in solution:
            if units != None:
                print "  %s\t%s\t%s" % (quarter, units, course)
            else:
                print "  %s\t%s\t%s" % (quarter, 'None', course)
