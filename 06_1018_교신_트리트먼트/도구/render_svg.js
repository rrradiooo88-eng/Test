const { chromium } = require('playwright');
const [, , inPath, outPath, w, h] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + inPath);
  await p.waitForTimeout(300);
  await p.screenshot({ path: outPath, fullPage: false });
  await b.close();
  console.log('rendered', outPath);
})().catch(e => { console.error(e); process.exit(1); });
