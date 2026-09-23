# Two-Tape Fence Cuts

A cut-to-fit calculator for sheet metal fencing on sloping ground. The sheets stand
plumb between a bottom rail and a top rail. When the rails aren't parallel, every sheet
needs a different angled cut. This tool gets every one of those cuts from **two tape
readings per bay**. Along a continuous run that is **N + 1 readings for N bays**.

It's one self-contained file, `index.html`. Open it in any browser, phone included. It
works offline once the fonts are cached, and it still works if they never load. The job
is saved in that browser's local storage.

```
apps/fence_cut_calculator/
  index.html          the app: UI plus the calculation core (<script id="fence-core">)
  tests/test_core.js  gate: loads the core straight out of index.html and checks it
```

Run the gate (exit 0 = pass):

```bash
node apps/fence_cut_calculator/tests/test_core.js
```

## Using it

1. **Setup** (once per job): standard bay width, sheets per bay, and which rail is level.
   Defaults: 2365 mm bay, 3 sheets, top rail level.
2. **Readings**: at each post, measure plumb from the bottom rail to the top rail, on the
   face where the sheets start. Type the reading into that post's yellow tape field.
   - *Rails step here*: the rails jump at this post, so it takes a reading on each side.
   - *Rails run straight through*: both rails continue in a straight line through this
     post, so it needs no reading. The value is interpolated from the posts either side.
     A long run on one steady grade needs only its two end readings.
   - If an odd bay isn't a whole number of sheets, enter its width. The last sheet gets a
     rip width.
3. **Cut list**: each bay card gives every sheet's left and right marks, measured from the
   factory end. It also gives the two shortcuts below.

If **both** rails slope, switch Setup to *From a string line*. You then take two readings
per post (down to each rail). The gap alone can't tell how the slope is split between
the two rails.

## Why two readings are enough (the derivation)

Let *x* run along the bay from the start post (0 … W), with *y* up. Sheets hang plumb.
Between posts, each rail is a straight line:

```
top rail stop line    T(x) = T0 + sT·x
bottom rail seat      B(x) = B0 + sB·x
gap                   g(x) = T(x) − B(x) = g0 + (g1 − g0)·x/W
```

**1. Two readings fix a bay.** `g` is linear, so it has two degrees of freedom. The
readings `g0` and `g1` at the posts fix it completely. A third reading could only be a
check. Neighbouring bays meet at a shared post, so a continuous run takes N + 1 readings.
Measuring each sheet's edges on site takes 2 per sheet, which is 6 per bay.

**2. Constant step.** Identical sheets at an even pitch *p* put the edges *p* apart, so
the length changes by the same amount from each sheet to the next:

```
δ = (g1 − g0)·p/W   ≈   (g1 − g0) / sheets
```

That gives three results:
- Every sheet in a bay has the same cut angle.
- Each sheet's long edge equals the next one's short edge (exactly, with no lap).
- The marks run `g0, g0+δ, g0+2δ, …`, so the list can be checked in your head.

**3. Cut the end that meets the sloping rail.** A square end is flush only against a level
rail. Against a rail of slope *s* it touches at one corner and gaps by `|s|·w` at the
other (*w* = sheet width). Cutting the rail-to-rail length with the square end on a
sloping rail makes the far corner **jam** by that same amount. So:
- Factory end goes on the level rail. It sits at the rail's lowest point over the sheet
  (top) or its highest point (bottom).
- The angled cut goes on the sloping rail.
- If both rails slope, cut both ends. In *Auto*, an end stays square when its corner gap
  is within the tolerance, since the rail channel hides it.

**4. Putting the marks on the steel, fewest steps first.**

| Method | Per bay | Why it works |
|---|---|---|
| **Chalk line** | 2 marks, 1 snap, no sums | Lay the bay's sheets face up, lapped as fitted, factory ends against a straight edge. They now sit exactly as in the fence, and g(x) is straight, so one line from `g0` at the first edge to `g1` at *W* marks every sheet. Exact whenever the factory end is on a level rail. |
| **Staggered stack** | set n−1 stagger offsets, 1 cut | Each sheet's cut line has the same slope in its own frame. Nest the sheets and slide each factory end out by its length difference (multiples of δ). Every line then lands on the same place, so one cut does the bay. A ripped sheet is cut at full width with the rest, then ripped. |
| **Sheet by sheet** | 2 marks, 1 line, 1 cut per sheet | The per-sheet table. |

With *both ends* cut, both lines are measured from the factory bottom end. Cut the top
line first so that end stays square as the reference, then cut the bottom rake (the same
for every full sheet).

## What the gate checks

`tests/test_core.js` checks the shipped code in two ways.

**Worked examples:** the 1500 → 1560 bay, hand-off, both level-rail cases, string mode
matching gap mode, the auto cut choice, ripped and spread bays, laps, interpolated and
stepped posts, stock-length and allowance handling, and input parsing.

**Placement sweep** (600 random bays, every cut mode, laps, odd widths, allowances): each
sheet is rebuilt from its marks alone and stood up between the rails. Then:
- cut ends must lie on their rail;
- square ends must touch at one corner and never cross the rail;
- reported corner gaps must match;
- marks must stay on the sheet;
- the stack and chalk-line shortcuts must put every mark on one line.

Deliberately planted bugs (a flipped min/max, a wrong reference end, wrong stack
offsets, wrong pitch) each fail the gate.

## Scope

This is a standalone site tool. It is not part of the Cella engine and imports nothing
from it.
