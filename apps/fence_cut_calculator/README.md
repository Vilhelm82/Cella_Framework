# Two-Tape Fence Cuts

A cut-to-fit calculator for sheet metal fencing on sloping ground. The sheets stand
plumb between a bottom rail and a top rail. When the rails aren't parallel, every sheet
needs a different angled cut. This tool gets every one of those cuts from **two tape
readings per bay**. Along a continuous run that is **N + 1 readings for N bays**, plus
one more number if the top rail is raked.

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

The page walks you through the job one screen at a time. Each screen asks for one
measurement, and its picture shows that measurement as a red arrow.

1. **Setup, once per job:**
   - sheets in a full bay;
   - full bay width;
   - whether the top rail is level or slopes;
   - any extra length to add to every reading.

   The 2365 mm / 3 sheet defaults are placeholders, so set them from your own sheets.
   With the rails already up, each sheet is lifted into the top rail and dropped into the
   bottom rail. Set the extra length to the top rail's channel depth less about 5 mm.
2. **P1 gap:** hold the tape upright beside the post. Measure from the top of the bottom
   rail to the underside of the top rail.
3. **Bay 1 width:** post face to post face, with the tape level. *Full bay* fills in the
   standard width. The screen tells you how many sheets the bay takes, and whether one
   needs ripping.
4. **P2 gap**, then either *Another bay* or *That's the last post*. If the rails change
   height at a post, that post takes a reading on each side. A corner is just another
   post.
5. **Cut list:** each bay opens with **two marks**. Lay the bay's sheets face up, side by
   side and lapped as they go in, with the tops against a straight string. Mark the left
   number on the first sheet's left edge and the right number on the last sheet's right
   edge (or at the bay width, on a part sheet's rip line). Pull a string between the two
   marks, tick every pan under it, and cut.
   - That's 2 marks per bay, instead of measuring both sides of every sheet at the fence.
   - It works because laid out as fitted, the sheets sit where they will in the fence.
   - For a full bay with a level top rail, the two marks are simply the post readings plus
     the allowance.
   - *Or one sheet at a time* gives each sheet **one number**, plus a grey check number for
     its other edge, for marking with a bevel.

**Cutting with a bevel.** At the first post of each bay, set a sliding bevel with its
handle flat on the post and its blade on the top of the bottom rail. If the top rail
slopes, set a second bevel against the underside of the top rail. The rails are straight,
so that angle is the same for every sheet in the bay. Then, for each sheet:
1. Lay it face up with its top away from you.
2. If the top slopes, bevel the top first.
3. Measure the sheet's number down the left edge from the top. Mark it.
4. Lay the bottom bevel through the mark and cut.
5. Check the right edge against the grey number.

Measuring the angle alone isn't enough. It doesn't say where on each sheet the cut goes,
and a 1° error is about 14 mm across a sheet and 41 mm across a bay. The tape readings
fix the positions to a millimetre or two, and the bevel carries the angle without any
numbers. Because the bevel carries the slope of each rail, the app never needs the top
rail's rake.

The calculation core in `index.html` also supports string-line readings, raked-rail rise
inputs, laps, stack and chalk-line shortcuts, and stock-length checks. The gate below
tests all of them. The step-by-step screens use only the gap-at-each-post path.

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

**Rake first, then the readings still apply.** With both ends cut, rake the top of every
sheet first. With the factory end up, trim the top rail's rise across one sheet
(`sT·w`) off one corner, running out to nothing at the other. The rake depends only on the top rail,
so it's the same cut on every sheet: one flush stack. The top edge then follows the rail
exactly. So each edge's length down from the raked top is the rail-to-rail gap, `g(a)`
and `g(b)`, and everything in points 1, 2 and 4 applies unchanged, measured from the raked
top.

**4. Putting the marks on the steel, fewest steps first.**

| Method | Per bay | Why it works |
|---|---|---|
| **Chalk line** | 2 marks, 1 snap, no sums | Lay the bay's sheets face up, lapped as fitted, factory ends against a straight edge. They now sit exactly as in the fence, and g(x) is straight, so one line from `g0` at the first edge to `g1` at *W* marks every sheet. Exact whenever the factory end is on a level rail. |
| **Staggered stack** | set n−1 stagger offsets, 1 cut | Each sheet's cut line has the same slope in its own frame. Nest the sheets and slide each factory end out by its length difference (multiples of δ). Every line then lands on the same place, so one cut does the bay. A ripped sheet is cut at full width with the rest, then ripped. |
| **Sheet by sheet** | 2 marks, 1 line, 1 cut per sheet | The per-sheet table. |

With *both ends* cut, the chalk line is laid against a straight edge along the raked
tops, which stands in for the top rail. The stack is lined up on the raked tops.

## What the gate checks

`tests/test_core.js` checks the shipped code in two ways.

**Worked examples:** the 1500 → 1560 bay, hand-off, both level-rail cases, string mode
matching gap mode, the auto cut choice, ripped and spread bays, laps, interpolated and
stepped posts, stock-length and allowance handling, and input parsing. Also the raked top
rail: trims, lengths from the raked top, per-bay overrides, a small rake kept square, and
a raked gap-mode fence matching the same fence measured from a string line.

**Placement sweep** (600 random bays, every cut mode, laps, odd widths, allowances): each
sheet is rebuilt from its marks alone and stood up between the rails. Then:
- cut ends must lie on their rail;
- square ends must touch at one corner and never cross the rail;
- reported corner gaps must match;
- marks must stay on the sheet, and a top rake must leave its high corner untouched;
- the stack and chalk-line shortcuts must put every mark on one line.

Eight deliberately planted bugs each fail the gate: a flipped min/max, a wrong
reference end, wrong stack offsets, wrong pitch, a flipped rake corner, swapped lengths,
a mis-scaled rake, and a dropped rake.

## Scope

This is a standalone site tool. It is not part of the Cella engine and imports nothing
from it.
