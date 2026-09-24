#!/usr/bin/env node
// Gate for the Two-Tape Fence Cuts calculation core.
// Loads the <script id="fence-core"> block straight out of index.html (so the shipped
// code is what gets tested), then checks it against an independent placement model:
// every cut sheet is stood between the rails and must meet them exactly.
// Run: node apps/fence_cut_calculator/tests/test_core.js   (exit 0 = pass)
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const m = /<script id="fence-core">([\s\S]*?)<\/script>/.exec(html);
if (!m) { console.error('FAIL: fence-core script block not found in index.html'); process.exit(1); }
const sandbox = {};
vm.runInNewContext(m[1], sandbox);
const C = sandbox.FenceCore;

let passed = 0, failed = 0;
function check(name, cond, detail) {
  if (cond) { passed++; return; }
  failed++;
  console.error('FAIL: ' + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : ''));
}
const near = (a, b, tol = 1e-6) => Math.abs(a - b) <= tol;

function post(g) { return { g: String(g) }; }
function gapJob(readings, widths, settings) {
  return { settings: Object.assign({}, settings), posts: readings.map(post),
           bays: (widths || []).map(w => ({ width: w === null ? '' : String(w) })) };
}

// Deterministic PRNG for the property sweep.
let seed = 0x5eed1234;
function rnd() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
const between = (lo, hi) => lo + (hi - lo) * rnd();

// ---------------------------------------------------------------------------
// 1. The worked example: 1500 -> 1560 over a standard bay of 3 sheets.
{
  const p = C.planRun(gapJob([1500, 1560], [null]));
  const bay = p.bays[0];
  check('example: no errors', bay.errors.length === 0, bay.errors);
  check('example: cut bottom (top rail level)', bay.mode === 'bottom', bay.mode);
  check('example: 3 sheets', bay.sheets.length === 3, bay.sheets.length);
  check('example: step is +20', near(bay.delta, 20), bay.delta);
  const want = [[1500, 1520], [1520, 1540], [1540, 1560]];
  bay.sheets.forEach((sh, i) => {
    check('example: sheet ' + (i + 1) + ' marks', near(sh.lines[0].l, want[i][0]) && near(sh.lines[0].r, want[i][1]),
          [sh.lines[0].l, sh.lines[0].r]);
    check('example: factory end at top', sh.ref === 'top');
  });
  check('example: chalk line 1500 -> 1560', bay.chalk && near(bay.chalk.l, 1500) && near(bay.chalk.r, 1560), bay.chalk);
  check('example: stack offsets 0/20/40', bay.stacks[0].offsets.every((o, i) => near(o, 20 * i)), bay.stacks[0].offsets);
  check('example: 2 readings', p.totals.readings === 2, p.totals.readings);
}

// 2. Hand-off: with no lap, each sheet's right mark is the next sheet's left mark.
{
  const p = C.planRun(gapJob([1432, 1611, 1520, 1702], [null, null, null], { sheetsPerBay: 4 }));
  p.bays.forEach((bay, k) => {
    for (let i = 0; i + 1 < bay.sheets.length; i++) {
      check('hand-off bay ' + k + ' sheet ' + i, near(bay.sheets[i].lines[0].r, bay.sheets[i + 1].lines[0].l));
    }
  });
  check('continuous run of 3 bays needs 4 readings', p.totals.readings === 4, p.totals.readings);
}

// 3. Bottom rail level -> cut the top, factory end in the bottom rail.
{
  const bay = C.planRun(gapJob([1500, 1440], [null], { levelRail: 'bottom' })).bays[0];
  check('bottom-level: cut top', bay.mode === 'top', bay.mode);
  check('bottom-level: factory end at bottom', bay.sheets.every(s => s.ref === 'bottom'));
  check('bottom-level: marks 1500..1440', near(bay.sheets[0].lines[0].l, 1500) && near(bay.sheets[2].lines[0].r, 1440));
}

// 4. String-line mode with a level top rail reproduces gap mode exactly.
{
  const gap = C.planRun(gapJob([1500, 1560, 1605], [null, 2000])).bays;
  const str = C.planRun({ settings: { mode: 'string' },
    posts: [{ t: 250, b: 1750 }, { t: 250, b: 1810 }, { t: 250, b: 1855 }],
    bays: [{ width: '' }, { width: 2000 }] }).bays;
  gap.forEach((b, k) => b.sheets.forEach((sh, i) => {
    const o = str[k].sheets[i];
    check('string == gap bay ' + k + ' sheet ' + i, near(sh.lines[0].l, o.lines[0].l) && near(sh.lines[0].r, o.lines[0].r) && b.mode === str[k].mode);
  }));
}

// 5. Auto cut-end choice.
{
  const run = (t0, b0, t1, b1, extra) => C.planRun({ settings: Object.assign({ mode: 'string' }, extra),
    posts: [{ t: t0, b: b0 }, { t: t1, b: b1 }], bays: [{ width: '' }] }).bays[0];
  check('auto: both rails slope -> both', run(200, 1700, 320, 1760).mode === 'both');
  check('auto: both near level -> square', run(200, 1700, 202, 1703).mode === 'square');
  check('auto: top slopes, bottom level -> top', run(200, 1700, 330, 1700).mode === 'top');
  check('auto: top level, bottom slopes -> bottom', run(200, 1700, 200, 1640).mode === 'bottom');
  const forced = run(200, 1700, 320, 1760, { cutEnds: 'bottom' });
  check('forced bottom on sloping top rail warns about the corner gap', forced.mode === 'bottom' && forced.warnings.length > 0, forced.warnings);
}

// 6. Sheet layout: even bays, ripped bays, laps.
{
  const s = C.resolveSettings({});
  let L = C.layoutSheets(2365, s);
  check('layout: standard bay = 3 even sheets', L.even && L.spans.length === 3 && L.spans.every(x => x.rip === 0));
  check('layout: spans tile [0, W]', near(L.spans[0].a, 0) && near(L.spans[2].b, 2365));
  L = C.layoutSheets(1400, s);
  check('layout: 1400 bay -> 2 sheets, last ripped', !L.even && L.spans.length === 2 && L.spans[1].rip > 100, L.spans);
  check('layout: ripped sheet ends at the post', near(L.spans[1].b, 1400));
  L = C.layoutSheets(2380, s);
  check('layout: 15 mm over is spread, not ripped', L.even && L.spans.length === 3, L.spans);
  const sl = C.resolveSettings({ lap: 30 });
  L = C.layoutSheets(2365, sl);
  check('layout with lap: sheets overlap by 30', L.spans.length === 3 && near(L.spans[0].b - L.spans[1].a, 30) && near(L.spans[2].b, 2365), L.spans);
  L = C.layoutSheets(300, s);
  check('layout: tiny bay is one ripped sheet', L.spans.length === 1 && near(L.spans[0].b, 300) && L.spans[0].rip > 0);
}

// 7. Interpolated ("rails run straight through") post.
{
  const job = { settings: {}, posts: [post(1500), { g: '', skip: true }, post(1620)], bays: [{ width: '' }, { width: '' }] };
  const p = C.planRun(job);
  const mid = p.stations[1];
  check('skip: interpolated', mid.interp && near(mid.left.T - mid.left.B, 1560), mid);
  check('skip: saves a reading', p.totals.readings === 2, p.totals.readings);
  const blocked = C.planRun({ settings: {}, posts: [post(''), { skip: true }, post(1620)], bays: [{}, {}] });
  check('skip: missing neighbour blocks both bays', blocked.bays.every(b => b.errors.length > 0));
}

// 8. Stepped post: separate readings either side.
{
  const job = { settings: {}, posts: [post(1500), { g: '1560', g2: '1420', step: true }, post(1480)], bays: [{}, {}] };
  const p = C.planRun(job);
  check('step: bay 1 ends at 1560', near(p.bays[0].g1, 1560));
  check('step: bay 2 starts at 1420', near(p.bays[1].g0, 1420));
  check('step: 4 readings', p.totals.readings === 4, p.totals.readings);
}

// 9. Stock length check and allowance.
{
  const p = C.planRun(gapJob([1500, 1560], [null], { stock: 1530, allowance: 0 }));
  const shorts = p.bays[0].sheets.filter(s => s.short > 0).map(s => s.n);
  check('stock: sheets 2 and 3 come up short', shorts.join() === '2,3', shorts);
  const a = C.planRun(gapJob([1500, 1560], [null], { allowance: 40 })).bays[0];
  check('allowance: added to every mark', near(a.sheets[0].lines[0].l, 1540) && near(a.chalk.r, 1600));
}

// 9b. Raked top rail in gap mode.
{
  // One rise across a sheet, measured with a sheet held plumb: gives the whole top rail.
  const job = { settings: { levelRail: 'raked', topRise: 30, topRiseDir: 'up' },
    posts: [post(1500), post(1440), post(1470)], bays: [{ width: '' }, { width: '' }] };
  const p = C.planRun(job);
  const s = p.settings;
  const bay = p.bays[0];
  check('raked: top rail rises 30 per sheet', near(bay.sT * s.sheetWidth, 30), bay.sT);
  check('raked: both ends cut', bay.mode === 'both', bay.mode);
  check('raked: top trim 30 at the left corner, 0 at the right', near(bay.sheets[0].lines[0].l, 30) && near(bay.sheets[0].lines[0].r, 0), bay.sheets[0].lines[0]);
  check('raked: lengths from the raked top are the gap readings', near(bay.sheets[0].lines[1].l, 1500) && near(bay.sheets[2].lines[1].r, 1440));
  check('raked: 3 readings + 1 rise', p.totals.readings === 3, p.totals.readings);
  // Same fence described with a string line gives the same sheets.
  const W = s.bayWidth, rise = 30 / s.sheetWidth * W;
  const str = C.planRun({ settings: { mode: 'string' },
    // Drops from a level string: the top rail rises (drop shrinks), bottom = top drop + gap.
    posts: [{ t: 400, b: 400 + 1500 }, { t: 400 - rise, b: 400 - rise + 1440 }, { t: 400 - 2 * rise, b: 400 - 2 * rise + 1470 }],
    bays: [{}, {}] });
  str.bays[0].sheets.forEach((sh, i) => {
    const o = bay.sheets[i];
    check('raked gap == string line, sheet ' + i, near(sh.lenL, o.lenL, 1e-6) && near(sh.lenR, o.lenR, 1e-6) && str.bays[0].mode === bay.mode, [sh.lenL, o.lenL]);
  });
  // Per-bay override and direction.
  job.bays[1] = { width: '', rise: '12', riseDir: 'down' };
  const q = C.planRun(job);
  check('raked: per-bay rise override', near(q.bays[1].rise, -12) && near(q.bays[1].sT * s.sheetWidth, -12), q.bays[1].rise);
  check('raked: small rise within tolerance keeps the top square', C.planRun({ settings: { levelRail: 'raked', topRise: 4 },
    posts: [post(1500), post(1560)], bays: [{}] }).bays[0].mode === 'bottom');
  // Straight-through post: the rake carries on and only the bottom rail is interpolated.
  const sk = C.planRun({ settings: { levelRail: 'raked', topRise: 30 },
    posts: [post(1500), { skip: true }, post(1620)], bays: [{}, {}] });
  check('raked: interpolated post keeps the gap straight', near(sk.stations[1].left.T - sk.stations[1].left.B, 1560, 1e-9));
}

// 10. Input parsing.
{
  check('num: thousands comma', C.num('1,500') === 1500);
  check('num: blank is null', C.num('  ') === null && C.num('') === null);
  check('num: junk is null', C.num('12a') === null);
  const bad = C.planRun(gapJob([1500, -10], [null])).bays[0];
  check('negative gap is refused', bad.errors.length > 0);
}

// ---------------------------------------------------------------------------
// 11. Property sweep: stand every sheet up between random rails and check the fit.
//     Independent model: the sheet is a quadrilateral cut from stock by its marks,
//     then dropped into the fence plumb. Its cut ends must lie on their rails; its
//     square ends must touch the rail at one corner and never cross it.
function placeAndCheck(tag, bay, rails, W, s) {
  const T = x => rails.T0 + (rails.T1 - rails.T0) * x / W;
  const B = x => rails.B0 + (rails.B1 - rails.B0) * x / W;
  const tol = 1e-6;
  bay.sheets.forEach(sh => {
    const xa = sh.a, xb = sh.b;
    // Marks are distances from the factory end, so they can't fall off the sheet,
    // and a rake cut off the factory end should start right at it (no wasted strip).
    check(tag + ' marks lie on the sheet', sh.lines.every(li => li.l >= -tol && li.r >= -tol), sh.lines);
    if (bay.mode === 'both') check(tag + ' top rake leaves the high corner untouched', near(Math.min(sh.lines[0].l, sh.lines[0].r), 0, tol), sh.lines[0]);
    // Outline in the sheet's own frame: y measured from the factory end, toward the other end.
    // Rebuild the finished sheet's four corner heights in the fence from the marks alone.
    let top, bot;
    if (bay.mode === 'bottom') {
      // Factory end is up. Square top at y0; cut line is marks.l / marks.r below it.
      const y0 = Math.min(T(xa), T(xb));
      top = [y0, y0];
      bot = [y0 - sh.lines[0].l, y0 - sh.lines[0].r];
    } else if (bay.mode === 'top' || bay.mode === 'square') {
      const y0 = Math.max(B(xa), B(xb));
      bot = [y0, y0];
      top = [y0 + sh.lines[0].l, y0 + sh.lines[0].r];
    } else {
      // Both: factory end up, raised until the raked top meets the rail at the high corner.
      // The trims must describe one straight line in the rail; the lengths hang from it.
      const yf = T(xa) + sh.lines[0].l;
      check(tag + ' both: top rake is straight in the rail', near(yf, T(xb) + sh.lines[0].r, tol), [yf, T(xb) + sh.lines[0].r]);
      top = [yf - sh.lines[0].l, yf - sh.lines[0].r];
      bot = [top[0] - sh.lines[1].l, top[1] - sh.lines[1].r];
      check(tag + ' both: stock covers the sheet', near(sh.need, Math.max(sh.lines[0].l + sh.lines[1].l, sh.lines[0].r + sh.lines[1].r), 1e-9));
    }
    const cutTop = bay.mode === 'top' || bay.mode === 'both';
    const cutBot = bay.mode === 'bottom' || bay.mode === 'both';
    if (cutTop) check(tag + ' top cut meets top rail', near(top[0], T(xa), tol) && near(top[1], T(xb), tol), [top, T(xa), T(xb)]);
    else {
      check(tag + ' square top never above top rail', top[0] <= T(xa) + tol && top[1] <= T(xb) + tol);
      check(tag + ' square top touches at one corner', near(top[0], T(xa), tol) || near(top[1], T(xb), tol));
    }
    if (cutBot) check(tag + ' bottom cut meets bottom rail', near(bot[0], B(xa), tol) && near(bot[1], B(xb), tol), [bot, B(xa), B(xb)]);
    else {
      check(tag + ' square bottom never below bottom rail', bot[0] >= B(xa) - tol && bot[1] >= B(xb) - tol);
      check(tag + ' square bottom touches at one corner', near(bot[0], B(xa), tol) || near(bot[1], B(xb), tol));
    }
    const gapT = Math.max(T(xa) - top[0], T(xb) - top[1]);
    const gapB = Math.max(bot[0] - B(xa), bot[1] - B(xb));
    check(tag + ' reported corner gaps', near(gapT, sh.gapTop, 1e-6) && near(gapB, sh.gapBot, 1e-6), [gapT, sh.gapTop, gapB, sh.gapBot]);
    if (s.cutEnds === 'auto' && sh.rip === 0) {
      check(tag + ' auto keeps square-end gaps within tolerance', gapT <= s.floatTol + 1e-9 && gapB <= s.floatTol + 1e-9);
    }
  });

  // Stack claim: shifting each sheet's factory end by its offset puts every cut line on the
  // first sheet's line, including a ripped sheet cut at full width.
  const w = s.sheetWidth;
  bay.stacks.forEach((stack, j) => {
    const base = bay.sheets[0].lines[j];
    if (bay.mode === 'both' && j === 0) {
      // Top rake: the same trim line on every sheet cut at full width, so the stack is flush.
      bay.sheets.forEach((sh, i) => {
        const li = sh.lines[0];
        check(tag + ' top rake stack is flush', stack.offsets[i] === 0);
        check(tag + ' top rake same slope', near((li.r - li.l) / sh.width, (base.r - base.l) / bay.sheets[0].width, 1e-9));
        if (sh.rip === 0) check(tag + ' top rake identical on full sheets', near(li.l, base.l, 1e-9) && near(li.r, base.r, 1e-9));
      });
      return;
    }
    const baseW = bay.sheets[0].width;
    const baseSlope = (base.r - base.l) / baseW;
    bay.sheets.forEach((sh, i) => {
      const li = sh.lines[j];
      const slope = (li.r - li.l) / sh.width;
      check(tag + ' stack line ' + j + ' same slope, sheet ' + i, near(slope, baseSlope, 1e-9), [slope, baseSlope]);
      check(tag + ' stack line ' + j + ' aligns after offset, sheet ' + i, near(li.l - stack.offsets[i], base.l, 1e-9));
      const rFull = li.l + slope * w;
      check(tag + ' stack full-width mark aligns, sheet ' + i, near(rFull - stack.offsets[i], base.l + baseSlope * w, 1e-6));
    });
  });

  // Chalk-line claim: every edge length lies on the straight line g0 -> g1, and those lengths
  // are the marks measured from the reference edge (factory end, or raked top).
  if (bay.chalk) {
    bay.sheets.forEach(sh => {
      const line = x => bay.g0 + (bay.g1 - bay.g0) * x / W;
      const marks = bay.mode === 'both' ? sh.lines[1] : sh.lines[0];
      check(tag + ' chalk line hits every mark', Math.abs(marks.l - line(sh.a)) <= 1 && Math.abs(marks.r - line(sh.b)) <= 1);
    });
  }
  if (bay.mode === 'both') check(tag + ' both ends: chalk line always offered', !!bay.chalk);
}

let sweeps = 0;
for (let trial = 0; trial < 400; trial++) {
  const cutEnds = ['auto', 'auto', 'bottom', 'top', 'both'][trial % 5];
  const settings = {
    mode: 'string', cutEnds,
    bayWidth: between(1800, 2600), sheetsPerBay: 2 + Math.floor(rnd() * 3),
    lap: rnd() < 0.5 ? 0 : between(10, 40), allowance: between(-20, 60),
    floatTol: between(0, 12), spreadTol: 20
  };
  const s = C.resolveSettings(settings);
  const W = rnd() < 0.6 ? s.bayWidth : between(300, s.bayWidth * 1.3);
  const t0 = between(100, 400), t1 = t0 + between(-250, 250) * (rnd() < 0.3 ? 0 : 1);
  const b0 = t0 + between(1200, 1900), b1 = b0 + (t1 - t0) + between(-300, 300);
  const p = C.planRun({ settings, posts: [{ t: t0, b: b0 }, { t: t1, b: b1 }], bays: [{ width: W }] });
  const bay = p.bays[0];
  if (bay.errors.length) { check('sweep ' + trial + ' no errors', false, bay.errors); continue; }
  const rails = bay.rails;
  placeAndCheck('sweep ' + trial + ' [' + bay.mode + ']', bay, rails, W, s);
  check('sweep ' + trial + ' first sheet starts at the post', near(bay.sheets[0].a, 0));
  check('sweep ' + trial + ' last sheet ends at the post', near(bay.sheets[bay.sheets.length - 1].b, W, 1e-9));
  sweeps++;
}

// Gap mode sweep too (level top rail and level bottom rail).
for (let trial = 0; trial < 200; trial++) {
  const levelRail = trial % 2 ? 'top' : 'bottom';
  const settings = { levelRail, sheetsPerBay: 3, lap: trial % 3 ? 0 : 25 };
  const s = C.resolveSettings(settings);
  const g0 = between(1300, 1900), g1 = g0 + between(-300, 300);
  const W = rnd() < 0.7 ? s.bayWidth : between(500, 2300);
  const bay = C.planRun({ settings, posts: [post(g0), post(g1)], bays: [{ width: W }] }).bays[0];
  placeAndCheck('gap sweep ' + trial + ' [' + levelRail + ']', bay, bay.rails, W, s);
  if (bay.mode === 'bottom' || bay.mode === 'top') check('gap sweep ' + trial + ' chalk line offered', !!bay.chalk);
  sweeps++;
}

console.log((failed ? 'FAIL' : 'PASS') + ': ' + passed + ' checks passed, ' + failed + ' failed (' + sweeps + ' random bays placed).');
process.exit(failed ? 1 : 0);
