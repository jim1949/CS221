commit 3c3d7c6fdb9f12084a6383381f286d235c477ad2
Author: songhan <songhan@stanford.edu>
Date:   Sun Nov 2 18:18:43 2014 -0800

    sum 2b

diff --git a/submission.py b/submission.py
index 8885715..a10dbef 100644
--- a/submission.py
+++ b/submission.py
@@ -433,7 +433,48 @@ def get_sum_variable(csp, name, variables, maxSum):
     """
     # Problem 2b
     # BEGIN_YOUR_CODE (around 20 lines of code expected)

    result = ('sum', name, 'aggregated')
    csp.add_variable(result, range(maxSum + 1))

    # no input variable, result should be 0
    if len(variables) == 0:
        csp.add_unary_potential(result, lambda val: val == 0)
        return result

    # Let the input be n variables X0, X1, ..., Xn.
    # After adding auxiliary variables, the factor graph will look like this:
    #
    # ^--A0 --*-- A1 --*-- ... --*-- An --*-- result--^
    #    |        |                  |
    #    *        *                  *
    #    |        |                  |
    #    X0       X1                 Xn
    #
    # where each "--*--" is a binary constraint
    # and each "--^" is a unary constraint.

    for i, X_i in enumerate(variables):
        # create auxiliary variable for variable i
        # use systematic naming to avoid naming collision
        A_i = ('sum', name, i)
        var = csp.varNames.index(X_i)
        varDomain = csp.valNames[var]
        if i == 0:
            csp.add_variable(A_i, [(0, val) for val in varDomain])
            preDomain = varDomain
        else:
            currentDomain = [(a, a + b) for a in preDomain for b in varDomain]
            currentDomain = list(set(currentDomain))
            csp.add_variable(A_i, currentDomain)
            # Add potential between Ai-1 and Ai
            csp.add_binary_potential(('sum', name, i - 1), A_i, lambda Ai_1, Ai: Ai_1[1] == Ai[0])
            preDomain = [a[1] for a in currentDomain]

        # Add potential between Ai and Xi
        csp.add_binary_potential(A_i, X_i, lambda Ai, Xi: Ai[1] == Ai[0] + Xi)
    csp.add_binary_potential(A_i, result, lambda val, result: result == val[1])
    return result
    # END_YOUR_CODE


