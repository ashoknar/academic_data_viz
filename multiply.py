
def mtply(x, y):

    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y
    else:
        n = max(len(str(x)), len(str(y)))
        n2 = n//2
        a = x // 10**(n2)
        b = x % 10**(n2)

        c = y // 10**(n2)
        d = y % 10**(n2)

        ac = mtply(a, c)
        bd = mtply(b, d)
        adbc = mtply((a+b), (c+d)) - ac - bd

        return (10**(2*n2))*ac + (10**n2)*adbc + bd


x = 3141592653589793238462643383279502884197169399375105820974944592
y = 2718281828459045235360287471352662497757247093699959574966967627

ans = mtply(x, y)

print(ans)