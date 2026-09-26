const fs = require('fs');
const path = require('path');

const HOST = "https://jichang-top.com";
const contentDir = path.join(__dirname, 'content');
const staticSitemapPath = path.join(__dirname, 'static', 'sitemap.xml');

function getPageInfo(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  
  // Extract slug or filename
  let slug = path.basename(filePath, '.md');
  const slugMatch = content.match(/^slug:\s*"([^"]+)"/m);
  if (slugMatch) {
    slug = slugMatch[1];
  }

  // Extract date
  let date = "2026-09-26T00:00:00+08:00";
  const dateMatch = content.match(/^date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})/m);
  if (dateMatch) {
    date = `${dateMatch[1]}T00:00:00+08:00`;
  }

  // Determine URL
  let url = `${HOST}/p/${slug}/`;
  let priority = "0.7";
  let changefreq = "weekly";

  const rel = path.relative(contentDir, filePath).replace(/\\/g, '/');
  if (rel === 'airport/index.md') {
    url = `${HOST}/airport/`;
    priority = "0.9";
    changefreq = "daily";
  } else if (rel.startsWith('page/about')) {
    url = `${HOST}/about/`;
    priority = "0.6";
    changefreq = "monthly";
  }

  return { url, date, priority, changefreq };
}

function getAllMdFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const full = path.join(dir, file);
    if (fs.statSync(full).isDirectory()) {
      getAllMdFiles(full, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(full);
    }
  });
  return fileList;
}

const mdFiles = getAllMdFiles(contentDir);
const items = [
  { url: `${HOST}/`, date: "2026-09-27T00:00:00+08:00", priority: "1.0", changefreq: "daily" }
];

mdFiles.forEach(file => {
  items.push(getPageInfo(file));
});

let xml = `<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n`;
xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n`;

items.forEach(item => {
  xml += `  <url>\n`;
  xml += `    <loc>${item.url}</loc>\n`;
  xml += `    <lastmod>${item.date}</lastmod>\n`;
  xml += `    <changefreq>${item.changefreq}</changefreq>\n`;
  xml += `    <priority>${item.priority}</priority>\n`;
  xml += `  </url>\n`;
});

xml += `</urlset>\n`;

fs.writeFileSync(staticSitemapPath, xml, 'utf-8');
console.log(`✅ Generated static sitemap at static/sitemap.xml with ${items.length} URLs!`);
