import fs from 'fs';
import pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';

const filePath = 'c:/Users/Admin/Downloads/B1_konsultatsioon_2021.pdf';
const raw = fs.readFileSync(filePath);
const typedArray = new Uint8Array(raw);

const doc = await pdfjsLib.getDocument(typedArray).promise;
let output = '';
const pages = Math.min(10, doc.numPages);
for (let i = 1; i <= pages; i++) {
  const page = await doc.getPage(i);
  const content = await page.getTextContent();
  const strings = content.items.map(item => item.str).join(' ');
  output += `--- PAGE ${i} ---\n${strings}\n\n`;
}
console.log(output);
