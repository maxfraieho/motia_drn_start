import { chromium } from 'playwright';
import fs from 'fs';

const URL = 'https://dangerboys.exodus.pp.ua/';

async function inspectPage() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto(URL, { waitUntil: 'networkidle' });
    console.log('Page loaded successfully');

    // Отримати HTML структуру
    const html = await page.content();
    fs.writeFileSync('./test/page-structure.html', html, 'utf8');
    console.log('✅ HTML saved to page-structure.html');

    // Знайти всі кнопки
    const buttons = await page.$$eval('button', btns =>
      btns.map(b => ({
        id: b.id,
        class: b.className,
        text: b.textContent.trim().substring(0, 50)
      }))
    );

    console.log('\n📋 BUTTONS FOUND:');
    buttons.forEach((btn, idx) => {
      console.log(`${idx + 1}. ID: "${btn.id}" | Class: "${btn.class}" | Text: "${btn.text}"`);
    });

    // Знайти sidebar та panels
    const sidebar = await page.$('.sidebar');
    const propertiesPanel = await page.$('.properties-panel');
    const canvas = await page.$('#canvas');

    console.log('\n🎨 UI ELEMENTS:');
    console.log(`Sidebar: ${sidebar ? '✅ Found' : '❌ Not found'}`);
    console.log(`Properties Panel: ${propertiesPanel ? '✅ Found' : '❌ Not found'}`);
    console.log(`Canvas: ${canvas ? '✅ Found' : '❌ Not found'}`);

    // Скріншот
    await page.screenshot({ path: './test/initial-page.png', fullPage: true });
    console.log('\n📸 Screenshot saved to initial-page.png');

  } catch (err) {
    console.error('Error:', err.message);
  } finally {
    await browser.close();
  }
}

inspectPage();
