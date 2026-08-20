const fs = require('fs');
const pdfjsLib = require('pdfjs-dist/legacy/build/pdf.js');
const pdfPath = 'c:/Users/Admin/Downloads/B1_konsultatsioon_2021.pdf';
const raw = fs.readFileSync(pdfPath);
const typedArray = new Uint8Array(raw);

pdfjsLib.getDocument({ data: typedArray }).promise.then(async doc => {
  console.error('numPages', doc.numPages);
  let out = '';
  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    const strings = content.items.map(item => item.str).join(' ');
    out += `--- PAGE ${i} ---\n${strings}\n\n`;
  }
  fs.writeFileSync('pdf_full_text.txt', out);
  console.log('DONE', out.length);
}).catch(err => { console.error(err); process.exit(1); });
