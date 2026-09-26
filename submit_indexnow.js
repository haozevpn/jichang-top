const fs = require('fs');
const path = require('path');
const https = require('https');

const API_KEY = "4b68ef5c889f41a1a7a0301d01f89312";
const HOST = "jichang-top.com";
const BASE_URL = `https://${HOST}`;
const postsDir = path.join(__dirname, 'content/post');

function getUrls() {
  const urls = [
    BASE_URL + '/',
    BASE_URL + '/airport/'
  ];
  
  if (fs.existsSync(postsDir)) {
    const files = fs.readdirSync(postsDir);
    files.forEach(file => {
      if (file.endsWith('.md')) {
        const content = fs.readFileSync(path.join(postsDir, file), 'utf-8');
        const slugMatch = content.match(/^slug:\s*"([^"]+)"/m);
        const slug = slugMatch ? slugMatch[1] : file.replace('.md', '');
        urls.push(`${BASE_URL}/p/${slug}/`);
      }
    });
  }
  return urls;
}

const urlList = getUrls();
console.log(`Found ${urlList.length} URLs to submit to IndexNow.`);

const payload = JSON.stringify({
  host: HOST,
  key: API_KEY,
  keyLocation: `${BASE_URL}/${API_KEY}.txt`,
  urlList: urlList
});

const options = {
  hostname: 'api.indexnow.org',
  port: 443,
  path: '/indexnow',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(payload)
  }
};

const req = https.request(options, (res) => {
  console.log(`IndexNow Submission Status Code: ${res.statusCode}`);
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    if (res.statusCode === 200 || res.statusCode === 202) {
      console.log('✅ IndexNow URLs submitted successfully to Bing/IndexNow!');
    } else {
      console.log(`Response: ${data}`);
    }
  });
});

req.on('error', (e) => {
  console.error(`IndexNow submission error: ${e.message}`);
});

req.write(payload);
req.end();
