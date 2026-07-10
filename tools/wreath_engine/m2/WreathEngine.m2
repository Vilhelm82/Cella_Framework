-- WreathEngine.m2 — Macaulay2 library for the wreath-engine pipeline.
--
-- This file is the mathematical authority behind the Python MCP server.
-- Generated scripts load it by absolute path and call:
--   emitResult      : print one fenced JSON result block (parsed by Python)
--   ordAlongPrime   : bounded symbolic-power order of an element along a prime
--   multiplicityOf  : multiplicity of an irreducible factor in a polynomial
--
-- Every generated script is standalone-except-this-file and rerunnable by
-- hand with `M2 --script <script>`.

needsPackage "PrimaryDecomposition";

jsonEscape = s -> (
    s = replace("\"", "\\\"", s);
    replace("\n", "\\n", s)
    );

jsonVal = v -> (
    if instance(v, String) then ("\"" | jsonEscape v | "\"")
    else if instance(v, Boolean) then (if v then "true" else "false")
    else if instance(v, ZZ) then toString v
    else if instance(v, List) then ("[" | demark(",", apply(v, jsonVal)) | "]")
    else ("\"" | jsonEscape toString v | "\"")
    );

-- kvs: list of Options key => value, keys are strings
emitResult = kvs -> (
    print "-----BEGIN WREATH RESULT-----";
    print("{" | demark(",", apply(kvs, kv -> "\"" | kv#0 | "\":" | jsonVal kv#1)) | "}");
    print "-----END WREATH RESULT-----";
    );

-- Order of vanishing of r along the prime P (both in the same ring, which may
-- be a quotient ring), via symbolic powers: the P-primary component of P^n is
-- topComponents(P^n) because every embedded component has strictly smaller
-- dimension. Returns -1 if the bound nmax is hit (caller must treat as error,
-- never as an answer).
ordAlongPrime = (r, P, nmax) -> (
    if r % P != 0 then return 0;
    for n from 1 to nmax do (
        Pn := topComponents(P^(n+1));
        if r % Pn != 0 then return n;
        );
    -1
    );

-- Multiplicity of f in g by exact division (valid in a polynomial ring, which
-- is a UFD). Returns -1 for g == 0 (infinite multiplicity).
multiplicityOf = (g, f) -> (
    if g == 0 then return -1;
    m := 0;
    while (g % f == 0) do (g = g // f; m = m + 1);
    m
    );
