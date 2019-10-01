import numpy as np
import scipy as si
from pycad.pyart import Pyart
from numpy import polyfit, poly1d
from scipy.optimize import curve_fit


def main():
    with open('data.txt', 'r', encoding='utf-8') as fl:
        lines = fl.readlines()
    xs, ys = [], []
    for line in lines:
        x, y = map(lambda x: float(x), line.split())
        # print(x, y)
        xs.append(x)
        ys.append(y)
    xs = list(map(lambda t: t + 18 + 273, xs))
    Tmax = max(xs)
    xs = list(map(lambda T: T/Tmax, xs))
    # print(xs)

    # ***
    # 1) a + b * x**4
    # 2) a + b * x + c * x**4
    # ***

    # p = polyfit(xs, ys, 4)
    # print(f'poly coeffs: {p}')
    # f = poly1d(p)

    # p0 = si.array([1, 1, 1])
    # la = lambda x ,a ,b ,c: a*x**b + c
    # popt, _ = curve_fit(la, np.array(xs), np.array(ys))#, p0)

    art = Pyart()
    art.skip()
    art = Pyart()

    art.dots(xs, ys)
    # art.nextLabel = 'numpy'  # str(p)
    # art.line(xs, f(xs), color='r', zord=5)
    # art.nextLabel = 'scipy'
    # art.lineWidth = 4
    # art.line(xs, la(xs, *popt), color='b', zord=4)

    # art.nextLabel = 'a*x^b + c'
    # curve = fit(lambda x, a, b, c: a*x**b + c, xs, ys)
    # art.line(*curve, color='r', zord=6)

    art.nextLabel = 'a + b * x**4'
    curve = fit(lambda x, a, b: a * x**np.full_like(x, 4) + b, xs, ys)
    art.line(*curve, color='b', zord=6)

    art.nextLabel = 'a + b * x + c * x**4'
    curve = fit(lambda x, a, b, c: a + x*np.full_like(x, b) +
                c * x**np.full_like(x, 4), xs, ys)
    art.line(*curve, color='r', zord=6)

    art.save('lab-7.png', 350)
    art.show()


def fit(fn, xs, ys):
    popt, _ = curve_fit(fn, np.array(xs), np.array(ys))
    # print(popt)
    return xs, fn(xs, *popt)


if __name__ == '__main__':
    main()
