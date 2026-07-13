# CONSTRAINTS — the constraint register

**Rule zero: if it is not in this register, it is not a constraint.** Prose
elsewhere — architecture docs, reports, code comments, git history, this repo's
own past handoffs — is context, never a rule. Before discarding any approach
because of a constraint, cite the `C-` id and check its `scope`: out of scope →
proceed; in scope → still present it as a displacement candidate against
`displaced-by`. Silently narrowing the solution space is a protocol violation;
visible, cited pruning is the only legal kind.

Every entry carries `scope`, `not-scope`, and `displaced-by`. A universal
("never", "all", "refused", "forbidden") that is not inside an entry with those
fields filled is a defect to fix on sight.

## C-001 standalone-zero-import
rule:        No code, design, doc, or corpus is imported wholesale from prior
             work; every capability is built and certified in-repo.
scope:       All of engine/ and any result entering RESULTS.md.
not-scope:   Reading prior work in archive/ or Reference_Material for context or
             comparison; the admission path (C-002) is how external material
             legally enters.
why:         An imported capability carries unverified assumptions the repo cannot
             re-run; deriving in-repo keeps every step auditable.
displaced-by: An ADMISSIONS.md case that closes (see C-002).

## C-002 admission-rule
rule:        Anything from prior work enters only via a docs/ADMISSIONS.md record
             that closes the case: why the engine needs it, why nothing derivable
             with bounded work beats it, and what would displace it.
scope:       Introduction of any external design, formula, document, or corpus.
not-scope:   In-repo derivation from already-admitted building blocks — that is
             the norm, not an admission.
why:         Keeps the corpus auditable and displacement-by-evidence honest.
displaced-by: Revision of the admission ledger itself (displacement is by
             evidence: present the dominating alternative and the old record falls).
source:      docs/ADMISSIONS.md

## C-003 re-verification-rule
rule:        No prior result is trusted on documentary status. "Ratified",
             "proven", "certified" in an origin document are claims, not evidence.
             Every mathematical input is re-proven in-repo (fresh code, byte-stable
             ×2, under research/verification/) before it bears load.
scope:       Any result gaining `status: current` in RESULTS.md.
not-scope:   Exploratory scouting, plotting, and numeric hypothesis testing —
             results there are not load-bearing until certified.
why:         Trust attaches to re-runnable certificates, never to labels or memory.
displaced-by: A stronger certification standard.

## C-004 exact-arithmetic-boundary
rule:        Cell values entering the residue accounting layer must be exact
             (ℚ or ℚ(√q)); float payloads at cell construction raise TypeError /
             a typed refusal.
scope:       engine/src/cella — cell construction and certificate-bearing paths.
not-scope:   Research scouting, plotting, numeric hypothesis testing, and external
             tool output. Floats are fine there; exactify at the boundary. An
             approach is NOT to be discarded merely because it mentions floats —
             check whether it touches the certificate-bearing boundary at all.
why:         Certificates must be byte-stable; exactness is the product.
displaced-by: An admitted exact float-embedding, or a certified interval layer.
