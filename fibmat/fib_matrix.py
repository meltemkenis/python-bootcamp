
def matrix_carp(r, m):

    a11 = (r[0][0] * m[0][0] + r[0][1] * m[1][0])
    a12 = (r[0][0] * m[0][1] + r[0][1] * m[1][1])
    a21 = (r[1][0] * m[0][0] + r[1][1] * m[1][0])
    a22 = (r[1][0] * m[0][1] + r[1][1] * m[1][1])

    r[0][0] = a11
    r[0][1] = a12
    r[1][0] = a21
    r[1][1] = a22

    carpim_matrix = [[a11, a12], [a21, a22]]

    return carpim_matrix


def fib(n, s):

    M = [[1, 1],
         [1, 0]]

    if n == 0:
        return 0

    power(M, n-1)

    return M[0][0] %s


def power(M, n):

    if n == 0:
        return

    elif n==1:
        return 1

    D = [[1, 1],
         [1, 0]]

    power(M, n//2)
    matrix_carp(M, M)

    if n % 2 != 0:
        matrix_carp(M, D)

print(fib(10**2,5))