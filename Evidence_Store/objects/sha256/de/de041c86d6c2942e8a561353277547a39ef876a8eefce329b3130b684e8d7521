#!/usr/bin/env python3
"""rur_tools.py — validated msolve RUR output parser (S-2026-07-03).
Recursive-descent tokenizer; two coefficient modes:
  parse_stream(path, p)      -> nested structure with big ints reduced mod p on the fly
  parse_stream_exact(path)   -> nested structure with exact ints (sets int_max_str_digits(0))
Validated against ast.literal_eval on small 3-var outputs (S-2026-07-03).
Structure: [dim, [char, nvars, ideal_deg, vars, lf, [1, [[deg_w,[w]], [deg_d,[d]], [[[deg_vi,[vi]], den_i], ...]]]]]
Coordinate convention (numerically confirmed, residual ~1e-47):
  x_i = -v_i(theta) / (den_i * w'(theta)),  coordinates in declared order.
Rational-root certificate: zero roots of w mod one good prime (deg preserved)
=> zero rational roots [PROVEN: denominator divides lead(w)].
Rules of engagement: assert isprime(p) on EVERY modulus; use Euclid-by-% for gcd
(hand-rolled), never rely on nmod_poly.gcd without a primality-clean modulus.
"""
import sys

def _make_value(s, reduce_fn):
    i = 0
    def value():
        nonlocal i
        while s[i] in ' \n\t\r': i += 1
        c = s[i]
        if c == '[':
            i += 1; out = []
            while s[i] in ' \n\t\r': i += 1
            if s[i] == ']': i += 1; return out
            while True:
                out.append(value())
                while s[i] in ' \n\t\r': i += 1
                if s[i] == ',': i += 1; continue
                if s[i] == ']': i += 1; return out
        if c == "'":
            j = s.index("'", i+1); tok = s[i+1:j]; i = j+1; return tok
        j = i
        if s[j] == '-': j += 1
        k = j
        while k < len(s) and s[k].isdigit(): k += 1
        digits = s[j:k]; neg = s[i] == '-'; i = k
        v = reduce_fn(digits)
        return -v if neg else v
    return value

def parse_stream(path, p):
    from sympy import isprime
    assert isprime(p), "modulus not prime"
    s = open(path).read()
    def red(digits):
        acc = 0
        for ch in digits: acc = (acc*10 + (ord(ch)-48)) % p
        return acc
    return _make_value(s, red)()

def parse_stream_exact(path):
    sys.set_int_max_str_digits(0)
    s = open(path).read()
    return _make_value(s, int)()

def blocks_of(parsed):
    hdr = parsed[1]
    b = hdr[5][1]
    return {"nvars": hdr[1], "ideal_deg": hdr[2], "vars": hdr[3], "lf": hdr[4],
            "w": b[0][1], "d": b[1][1], "vlist": b[2]}

def safe_gcd(a, b):
    while not b.is_zero(): a, b = b, a % b
    return a
