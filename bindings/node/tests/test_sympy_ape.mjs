import assert from 'node:assert/strict';

import { diff, integrate, solve, subs, version } from '../src/index.js';

const sympyVersion = await version();
const integrated = await integrate({ expr: 'sin(x)' });
const differentiated = await diff({ expr: '-x**2' });
const solved = await solve({ expr: 'x**2-1' });
const substituted = await subs({ expr: 'x**2+y', symbols: 'x', value: '3' });

assert.equal(sympyVersion, '1.14.0');
assert.equal(integrated.result, '-cos(x)');
assert.match(integrated.latex, /cos/);
assert.equal(differentiated.result, '-2*x');
assert.equal(solved.result, '[-1, 1]');
assert.equal(substituted.result, 'y + 9');
