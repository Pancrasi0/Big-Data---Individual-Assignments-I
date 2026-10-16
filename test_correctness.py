#!/usr/bin/env python3
"""Correctness tests. Exact integer arithmetic -> numerical tolerance is ZERO.

1. Hand-computed 2x2 case (see report).
2. Full result matrices ("dump" mode) of C, Java and Python compared element by element with a
   NumPy int64 reference for several sizes (including n=1 and non-power-of-two sizes).
3. Weighted checksums of the three implementations compared with the reference for larger n.
Writes correctness.csv and exits with status 1 if any test fails.
"""
import csv
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
IMPLS = {
    "C": ["./matrix_c"],
    "Java": ["java", "main"],
    "Python": [sys.executable, "matrix.py"],
}


def inputs(n):
    i = np.arange(n, dtype=np.int64)[:, None]
    j = np.arange(n, dtype=np.int64)[None, :]
    return (7 * i + 3 * j + 1) % 10 + 1, (5 * i + 11 * j + 2) % 10 + 1


def run(impl, n, *extra):
    cmd = IMPLS[impl] + [str(n)] + [str(x) for x in extra]
    return subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, check=True).stdout


def parse_matrix(text):
    return np.array([[int(x) for x in line.split()] for line in text.strip().splitlines()], dtype=np.int64)


def main():
    results = []

    # 1. hand-computed case: A=[[2,5],[9,2]], B=[[3,4],[8,9]] -> C=[[46,53],[43,54]]
    hand = np.array([[46, 53], [43, 54]], dtype=np.int64)
    a, b = inputs(2)
    assert (a == np.array([[2, 5], [9, 2]])).all() and (b == np.array([[3, 4], [8, 9]])).all()
    for impl in IMPLS:
        got = parse_matrix(run(impl, 2, "dump"))
        results.append(("hand-computed 2x2", 2, impl, bool((got == hand).all())))

    # 2. full matrices vs NumPy reference
    for n in (1, 2, 3, 5, 10, 16, 33, 64):
        a, b = inputs(n)
        ref = a @ b
        for impl in IMPLS:
            got = parse_matrix(run(impl, n, "dump"))
            results.append(("full matrix vs NumPy", n, impl, bool(got.shape == ref.shape and (got == ref).all())))

    # 3. checksums for larger sizes
    for n in (100, 250):
        a, b = inputs(n)
        w = (np.arange(n)[:, None] + 1) * (np.arange(n)[None, :] + 1)
        ref = int((w * (a @ b)).sum())
        for impl in IMPLS:
            got = int(run(impl, n).split()[1])
            results.append(("checksum vs NumPy", n, impl, got == ref))

    with open(os.path.join(HERE, "correctness.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["test", "n", "impl", "pass"])
        wr.writerows(results)
    failed = [r for r in results if not r[3]]
    print(f"{len(results) - len(failed)}/{len(results)} checks passed")
    for r in failed:
        print("FAILED:", r)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
