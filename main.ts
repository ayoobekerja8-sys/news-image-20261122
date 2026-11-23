#!/usr/bin/env node
/**
 * Entrypoint for the make.fun news-image-20261122 bounty.
 *
 * Copies the pre-rendered entry.png into the output directory. The image is
 * produced deterministically by draw.py (Pillow, fixed fonts, no clock, no
 * network); this program only validates and moves the finished bytes.
 *
 * Node 22, standard library only. No network, no clock, no randomness.
 */

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUTPUT_DIR, "entry.png");

/** Hard limits from the competition rules. */
const MAX_BYTES = 1_048_576;
const MAX_SIDE = 1024;

function fail(message: string): never {
  process.stderr.write(`main.ts: ${message}\n`);
  process.exit(1);
}

/**
 * Read the pixel dimensions from the PNG IHDR chunk (always the first chunk
 * after the 8-byte signature). Returns null when the bytes are not a PNG.
 */
function pngSize(buf: Buffer): { width: number; height: number } | null {
  const signature = "89504e470d0a1a0a";
  if (buf.length < 24 || buf.subarray(0, 8).toString("hex") !== signature) {
    return null;
  }
  if (buf.subarray(12, 16).toString("latin1") !== "IHDR") return null;
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

/** First two bytes of a JPEG stream. */
function isJpeg(buf: Buffer): boolean {
  return buf.length > 2 && buf[0] === 0xff && buf[1] === 0xd8;
}

function main(): void {
  let stat;
  try {
    stat = statSync(SOURCE);
  } catch {
    fail(`cannot read ${SOURCE}`);
  }
  if (!stat.isFile()) fail(`not a regular file: ${SOURCE}`);
  if (stat.size === 0) fail("entry.png is empty");
  if (stat.size > MAX_BYTES) {
    fail(`entry.png is ${stat.size} bytes, over the ${MAX_BYTES}-byte limit`);
  }

  const buf = readFileSync(SOURCE);
  if (isJpeg(buf)) {
    process.stdout.write("entry.png is a JPEG stream\n");
  } else {
    const size = pngSize(buf);
    if (size === null) fail("entry.png is neither a whole PNG nor a JPEG");
    if (size.width > MAX_SIDE || size.height > MAX_SIDE) {
      fail(`entry.png is ${size.width}x${size.height}, over ${MAX_SIDE}px`);
    }
    process.stdout.write(`entry.png is PNG ${size.width}x${size.height}\n`);
  }

  mkdirSync(resolve(OUTPUT_DIR), { recursive: true });
  copyFileSync(SOURCE, TARGET);
  process.stdout.write(
    `copied ${stat.size} bytes from ${SOURCE} to ${TARGET}\n`,
  );
}

main();
