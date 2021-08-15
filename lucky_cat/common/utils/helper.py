
# check whether array is monotonic
def isMonotonic(A):
    return (all(A[i] <= A[i + 1] for i in range(len(A) - 1)) or
            all(A[i] >= A[i + 1] for i in range(len(A) - 1)))

# if only one day's date is decreasing, then treat it as monotonic as well
def isMonotonicApproximate(A):
    # monotonically increase
    iVio = False
    iPass = True
    for i in range(1, len(A)):
        if A[i] < A[i - 1]:
            if iVio:
                iPass = False
                break
            else:
                iVio = True

    if iPass:
        return True
    # monotonically decrease
    dVio = False
    dPass = True
    for i in range(1, len(A)):
        if A[i] > A[i - 1]:
            if dVio:
                dPass = False
                break
            else:
                dVio = True
    if dPass:
        return True
    return False