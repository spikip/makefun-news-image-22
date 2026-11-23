// news-image-20261122 entry (Node 22, standard library only).
// The front page for Sunday 22 November 2026 lives beside this file as entry.png
// (drawn by render.py from that day's reporting); this program copies it to the
// output path the harness reads. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
