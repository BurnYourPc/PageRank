from src.parse import htmlParser as parse
from src.purifier import purifier as pure
from src.uniq_purifier import unqpurifier as unqpure
from src.createPdf import pdfcreator as PdfC
import numpy as np
from numpy import linalg as LA
from copy import deepcopy


def getAready(A, n):
    for j in range(n):
        nz = np.count_nonzero(A[:, j])
        for i in range(n):
            if (A[i, j] != 0):
                A[i, j] = A[i, j] / nz
    return A


def removeSpiderTraps(A, n):
    A = 0.8 * A
    A2 = np.zeros((n, n), dtype=float)
    A2 = (1 / n) + A2
    A2 = 0.2 * A2
    A = A + A2
    return A


def getRank(A, n):
    r = np.zeros((n, 1), dtype=float)
    for i in range(n):
        r[i] = 1 / n
    rnew = np.dot(A, r)
    while (LA.norm(rnew - r, 2) > 0.000001):
        r = rnew
        rnew = np.dot(A, rnew)
    return rnew


def rankUrls(urls, n):  # we do the same as in siteGui function
    A = np.zeros((n, n), dtype=float)
    urls2 = urls
    col = 0
    for link in urls:
        basetocheck = unqpure.getBaseToCheck(link)
        checkin, outlinks = unqpure.find_outlinks(link, False, basetocheck, 1)
        print(outlinks)
        if (checkin):
            A[col, col] = 1
        counter = 0
        for otherLink in urls2:
            if otherLink != link:
                counter = counter + 1
                if otherLink in outlinks:
                    A[counter, col] = 1
        col = col + 1
    print(A)
    A = getAready(A, n)
    print(A)
    A = removeSpiderTraps(A, n)
    r = getRank(A, n)
    print("The ranking of the sites' is:")
    print(r)
    return r


def is_ascii(s):   # check if url have encoded a unicode string in ascii to be produced (non english characters for example or "–" (not "-") character)
    isascii = len(s) != len(s.encode())
    return isascii