const fs = require('fs');
const path = require('path');

const rootDir = 'd:/桌面文件/jichang-top.com';
const hugoPostsDir = path.join(rootDir, 'content/post');
const astroPostsDir = path.join(rootDir, 'astro-site/src/content/posts');
const staticSitemap = path.join(rootDir, 'static/sitemap.xml');
const astroPublicSitemap = path.join(rootDir, 'astro-site/public/sitemap.xml');
const indexnowKey = path.join(rootDir, 'static/4b68ef5c889f41a1a7a0301d01f89312.txt');
const astroPublicIndexnow = path.join(rootDir, 'astro-site/public/4b68ef5c889f41a1a7a0301d01f89312.txt');

// 1. Copy sitemap.xml and IndexNow key to astro-site/public
if (fs.existsSync(staticSitemap)) {
  fs.copyFileSync(staticSitemap, astroPublicSitemap);
  console.log(`✅ Copied sitemap.xml to astro-site/public/sitemap.xml`);
}
if (fs.existsSync(indexnowKey)) {
  fs.copyFileSync(indexnowKey, astroPublicIndexnow);
  console.log(`✅ Copied IndexNow key to astro-site/public/4b68ef5c889f41a1a7a0301d01f89312.txt`);
}

// 2. Sync frontmatter (description & keywords) from Hugo posts to Astro posts
if (fs.existsSync(hugoPostsDir) && fs.existsSync(astroPostsDir)) {
  const hugoFiles = fs.readdirSync(hugoPostsDir);
  let count = 0;
  
  hugoFiles.forEach(file => {
    if (file.endsWith('.md')) {
      const hugoPath = path.join(hugoPostsDir, file);
      const astroPath = path.join(astroPostsDir, file);
      
      if (fs.existsSync(astroPath)) {
        const hugoContent = fs.readFileSync(hugoPath, 'utf-8');
        let astroContent = fs.readFileSync(astroPath, 'utf-8');
        
        const descMatch = hugoContent.match(/^description:\s*"([^"]+)"/m);
        const kwMatch = hugoContent.match(/^keywords:\s*"([^"]+)"/m);
        
        if (descMatch) {
          if (astroContent.match(/^description:\s*".*?"/m)) {
            astroContent = astroContent.replace(/^description:\s*".*?"/m, `description: "${descMatch[1]}"`);
          } else {
            astroContent = astroContent.replace(/^description:\s*.+/m, `description: "${descMatch[1]}"`);
          }
        }
        
        if (kwMatch) {
          if (astroContent.match(/^keywords:\s*".*?"/m)) {
            astroContent = astroContent.replace(/^keywords:\s*".*?"/m, `keywords: "${kwMatch[1]}"`);
          } else if (astroContent.match(/^description:\s*".*?"/m)) {
            astroContent = astroContent.replace(/(^description:\s*".*?"\n)/m, `$1keywords: "${kwMatch[1]}"\n`);
          }
        }
        
        fs.writeFileSync(astroPath, astroContent, 'utf-8');
        count++;
      }
    }
  });
  console.log(`✅ Synced ${count} post frontmatters to astro-site/src/content/posts`);
}
