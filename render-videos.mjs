import puppeteer from 'puppeteer';
import { spawn, execSync } from 'child_process';
import path from 'path';
import http from 'http';

const OUT = '/Users/alexhosage/Desktop/MMD Videos';
const BASE = 'http://localhost:8888';
const FPS = 30;

// ─── Videos to render ────────────────────────────────────────────────
const VIDEOS = [
  { html: 'ads/video-16x9.html',          width: 1200, height: 675,  name: 'Wedding_16x9.mp4'  },
  { html: 'ads/video-9x16-wedding.html',  width: 1080, height: 1920, name: 'Wedding_9x16.mp4'  },
  { html: 'ads/video-16x9-events.html',   width: 1200, height: 675,  name: 'Events_16x9.mp4'   },
  { html: 'ads/video-9x16-events.html',   width: 1080, height: 1920, name: 'Events_9x16.mp4'   },
];

// ─── Ensure http-server is running on port 8888 ─────────────────────
async function ensureServer() {
  const alive = await new Promise(resolve => {
    const req = http.get(BASE, () => resolve(true));
    req.on('error', () => resolve(false));
    req.setTimeout(2000, () => { req.destroy(); resolve(false); });
  });

  if (alive) {
    console.log('http-server already running on port 8888');
    return null;
  }

  console.log('Starting http-server on port 8888...');
  const server = spawn('npx', ['http-server', '.', '-p', '8888', '-c-1', '--silent'], {
    cwd: '/Users/alexhosage/Desktop/mmd-website',
    stdio: 'ignore',
    detached: true,
  });
  server.unref();

  // Wait for it to be ready
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 500));
    const ok = await new Promise(resolve => {
      const req = http.get(BASE, () => resolve(true));
      req.on('error', () => resolve(false));
      req.setTimeout(2000, () => { req.destroy(); resolve(false); });
    });
    if (ok) {
      console.log('http-server ready');
      return server;
    }
  }
  throw new Error('http-server failed to start within 10s');
}

// ─── Render one video using the stepped SCENES API ──────────────────
async function renderVideo({ html, width, height, name }) {
  const url = `${BASE}/${html}`;
  const outPath = path.join(OUT, name);

  console.log(`\nRendering ${name} (${width}x${height})`);
  console.log(`  Source: ${html}`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts + images
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    return Promise.all(imgs.map(img =>
      img.complete ? Promise.resolve() : new Promise(r => { img.onload = r; img.onerror = r; })
    ));
  });
  await new Promise(r => setTimeout(r, 500));

  // Kill all CSS animations/transitions so scenes are static snapshots
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.textContent = '*, *::before, *::after { animation: none !important; transition: none !important; }';
    document.head.appendChild(style);
  });

  // Read scene durations
  const scenes = await page.evaluate(() =>
    window.SCENES.map(s => ({ duration: s.duration }))
  );

  const totalFrames = scenes.reduce((sum, s) => sum + Math.ceil((s.duration / 1000) * FPS), 0);
  const totalDuration = scenes.reduce((sum, s) => sum + s.duration, 0);
  console.log(`  ${scenes.length} scenes, ${totalDuration / 1000}s total, ${totalFrames} frames`);

  // Start ffmpeg
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-i', '-',
    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '20',
    '-movflags', '+faststart',
    outPath,
  ], { stdio: ['pipe', 'pipe', 'pipe'] });

  let ffmpegErr = '';
  ffmpeg.stderr.on('data', d => { ffmpegErr += d.toString(); });

  let framesSoFar = 0;

  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    const sceneFrames = Math.ceil((scene.duration / 1000) * FPS);

    console.log(`  Scene ${i + 1}/${scenes.length} (${scene.duration / 1000}s) — ${sceneFrames} frames`);

    // Show this scene (hides all others)
    await page.evaluate((idx) => window.showScene(idx), i);
    await new Promise(r => setTimeout(r, 200)); // let DOM settle

    // Take the same screenshot N times for the scene's duration
    const screenshot = await page.screenshot({ type: 'png', captureBeyondViewport: false });

    for (let f = 0; f < sceneFrames; f++) {
      try {
        if (ffmpeg.stdin.destroyed) break;
        ffmpeg.stdin.write(screenshot);
      } catch (err) {
        console.error(`  ffmpeg stdin write error at frame ${framesSoFar + f}: ${err.message}`);
        break;
      }
    }

    framesSoFar += sceneFrames;
  }

  console.log(`  Encoding ${framesSoFar} frames...`);

  // Close ffmpeg stdin and wait for it to finish
  await new Promise((resolve, reject) => {
    ffmpeg.stdin.end();
    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited with code ${code}\n${ffmpegErr}`));
    });
    ffmpeg.on('error', reject);
  });

  await browser.close();
  console.log(`  Saved: ${outPath}`);
}

// ─── Main ────────────────────────────────────────────────────────────
async function main() {
  console.log('MrsMillennial Designs — Video Renderer (stepped)');
  console.log(`Output: ${OUT}`);
  console.log(`FPS: ${FPS}\n`);

  const server = await ensureServer();

  try {
    for (const video of VIDEOS) {
      await renderVideo(video);
    }
  } finally {
    if (server) {
      try { process.kill(-server.pid); } catch {}
    }
  }

  console.log(`\nDone — ${VIDEOS.length} videos saved to: ${OUT}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
