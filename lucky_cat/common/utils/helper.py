
def isMonotonicInc(A):
    return all(A[i] <= A[i + 1] for i in range(len(A) - 1))

def isMonotonicDec(A):
    return all(A[i] >= A[i + 1] for i in range(len(A) - 1))

# check whether array is monotonic
def isMonotonic(A):
    return (all(A[i] <= A[i + 1] for i in range(len(A) - 1)) or
            all(A[i] >= A[i + 1] for i in range(len(A) - 1)))

def isMonotonicIncApproximate(A):
    # monotonically increase
    iVio = False
    iPass = True
    for i in range(1, len(A)):
        if A[i] < A[i - 1]:
            if iVio:
                iPass = False
                break
            else:
                # if last elem decreases, treat as violation
                if i == len(A) - 1:
                    return False
                iVio = True

    if iPass:
        return True
    return False

def isMonotonicDecApproximate(A):
    # monotonically decrease
    dVio = False
    dPass = True
    for i in range(1, len(A)):
        if A[i] > A[i - 1]:
            if dVio:
                dPass = False
                break
            else:
                # if last elem increases, treat as violation
                if i == len(A) - 1:
                    return False
                dVio = True
    if dPass:
        return True
    return False

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