import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';

const OUT = '/Users/alexhosage/Desktop/MMD Videos';
const BASE = 'http://localhost:8888';
const FPS = 30;

async function renderVideo({ url, width, height, duration, outputName, clickPlay }) {
  console.log(`\n🎬 Rendering ${outputName} (${width}x${height}, ${duration/1000}s)...`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts to load
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1000));

  const outPath = path.join(OUT, outputName);
  const totalFrames = Math.ceil((duration / 1000) * FPS);

  // Start ffmpeg process
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'medium',
    '-crf', '18',
    '-movflags', '+faststart',
    outPath
  ], { stdio: ['pipe', 'pipe', 'pipe'] });

  let ffmpegErr = '';
  ffmpeg.stderr.on('data', d => ffmpegErr += d.toString());

  // Click play button
  if (clickPlay) {
    await clickPlay(page);
  }

  const startTime = Date.now();

  for (let frame = 0; frame < totalFrames; frame++) {
    const targetTime = (frame / FPS) * 1000;
    const elapsed = Date.now() - startTime;

    // Wait until we're at the right time
    if (elapsed < targetTime) {
      await new Promise(r => setTimeout(r, targetTime - elapsed));
    }

    const screenshot = await page.screenshot({ type: 'png' });
    ffmpeg.stdin.write(screenshot);

    if (frame % 30 === 0) {
      process.stdout.write(`  Frame ${frame}/${totalFrames} (${Math.round(frame/totalFrames*100)}%)\r`);
    }
  }

  console.log(`  Frame ${totalFrames}/${totalFrames} (100%)   `);

  // Close ffmpeg
  ffmpeg.stdin.end();
  await new Promise((resolve, reject) => {
    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited ${code}: ${ffmpegErr}`));
    });
  });

  await browser.close();
  console.log(`✅ Saved: ${outPath}`);
}

// The real-time approach above won't sync well with CSS animations.
// Better approach: use puppeteer's CDP to control time and screenshot each frame.
async function renderVideoStepped({ url, width, height, duration, outputName, setupFn }) {
  console.log(`\n🎬 Rendering ${outputName} (${width}x${height}, ${duration/1000}s)...`);

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });

  // Pause all animations initially
  const client = await page.createCDPSession();
  await client.send('Animation.enable');

  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 500));

  // Run setup (click play, etc)
  if (setupFn) {
    await setupFn(page);
  }

  // Small wait for click handler to fire
  await new Promise(r => setTimeout(r, 100));

  const outPath = path.join(OUT, outputName);
  const totalFrames = Math.ceil((duration / 1000) * FPS);
  const frameDuration = 1000 / FPS; // ms per frame

  // Start ffmpeg
  const ffmpeg = spawn('ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'medium',
    '-crf', '18',
    '-movflags', '+faststart',
    outPath
  ], { stdio: ['pipe', 'pipe', 'pipe'] });

  let ffmpegErr = '';
  ffmpeg.stderr.on('data', d => ffmpegErr += d.toString());

  // Capture frames in real time — CSS animations run on their own clock
  // We just need to screenshot fast enough
  const t0 = Date.now();

  for (let frame = 0; frame < totalFrames; frame++) {
    const targetMs = frame * frameDuration;

    // Wait until target time
    const now = Date.now() - t0;
    if (now < targetMs) {
      await new Promise(r => setTimeout(r, targetMs - now));
    }

    const screenshot = await page.screenshot({ type: 'png', captureBeyondViewport: false });
    ffmpeg.stdin.write(screenshot);

    if (frame % FPS === 0) {
      process.stdout.write(`  ${Math.round(frame/totalFrames*100)}% (${Math.round(targetMs/1000)}s/${duration/1000}s)\r`);
    }
  }

  console.log(`  100% — encoding...                    `);

  ffmpeg.stdin.end();
  await new Promise((resolve, reject) => {
    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`ffmpeg exited ${code}: ${ffmpegErr}`));
    });
  });

  await browser.close();
  console.log(`✅ Saved: ${outPath}`);
}

async function main() {
  console.log('🎬 MrsMillennial Designs — Video Renderer');
  console.log(`Output folder: ${OUT}\n`);

  // 1. 16:9 Mother's Day ad (from the website)
  await renderVideoStepped({
    url: `${BASE}/mothers-day.html`,
    width: 1920,
    height: 1080,
    duration: 37000,
    outputName: 'MothersDay_16x9.mp4',
    setupFn: async (page) => {
      // Click the play button overlay
      await page.evaluate(() => {
        const po = document.getElementById('po');
        if (po) po.click();
      });
    }
  });

  // 2. 9:16 Instagram ad
  await renderVideoStepped({
    url: `${BASE}/ig-mothers-day.html`,
    width: 1080,
    height: 1920,
    duration: 37000,
    outputName: 'MothersDay_9x16_IG.mp4',
    setupFn: async (page) => {
      // Click play
      await page.evaluate(() => {
        if (typeof go === 'function') go();
      });
    }
  });

  console.log(`\n🎉 All done! Videos saved to: ${OUT}`);
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
