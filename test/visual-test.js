import { chromium } from 'playwright';

const URL = 'http://localhost:8080';

async function visualTest() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/chromium',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  console.log('🔍 Opening page...');
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  // Wait for diagram list to load
  await page.waitForSelector('#diagram-nav a', { timeout: 10000 });

  console.log('📋 Collecting console logs...');
  page.on('console', msg => {
    console.log(`[BROWSER] ${msg.type()}: ${msg.text()}`);
  });

  page.on('pageerror', error => {
    console.log(`[ERROR] ${error.message}`);
  });

  // Get list of available diagrams
  const diagrams = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('#diagram-nav a'));
    return links.map(a => ({
      text: a.textContent.trim(),
      path: a.dataset.path,
      diagramId: a.dataset.diagramId
    }));
  });

  console.log('📊 Available diagrams:', diagrams.length);
  diagrams.forEach((d, i) => console.log(`  ${i + 1}. ${d.text}`));

  // Клік на example_workflow діаграму
  console.log('\n🖱️ Clicking on Example_workflow diagram...');
  const clicked = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('#diagram-nav a'));
    const link = links.find(a => a.textContent.includes('Example_workflow'));
    if (link) {
      link.click();
      return true;
    }
    return false;
  });

  if (clicked) {
    console.log('✅ Clicked on diagram');
    await page.waitForTimeout(3000);

    // Перевірити canvas
    const canvasInfo = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      if (canvas) {
        return {
          width: canvas.width,
          height: canvas.height,
          style: canvas.style.transform,
          visible: canvas.offsetParent !== null
        };
      }
      return null;
    });

    console.log('📊 Canvas info:', canvasInfo);

    // Зробити скріншот
    await page.screenshot({ path: './test/diagram-visual-test.png', fullPage: true });
    console.log('📸 Screenshot saved to ./test/diagram-visual-test.png');

    // Отримати структуру діаграми
    const diagramStructure = await page.evaluate(() => {
      if (window.DrakonTestAPI) {
        const diagram = window.DrakonTestAPI.getDiagram();
        return {
          name: diagram.name,
          itemsCount: Object.keys(diagram.items || {}).length,
          items: diagram.items,
          hasParams: !!diagram.params,
          hasAccess: !!diagram.access
        };
      }
      return null;
    });

    console.log('📦 Diagram structure:', JSON.stringify(diagramStructure, null, 2));

    console.log('\n✅ Test complete');
  } else {
    console.log('❌ Could not find diagram');
  }

  await browser.close();
}

visualTest().catch(console.error);
