// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://jichang-top.com',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      // 自定义优先级
      customPages: [
        'https://jichang-top.com/',
        'https://jichang-top.com/airport',
        'https://jichang-top.com/categories/机场测评',
        'https://jichang-top.com/categories/科学上网指南',
      ],
      serialize(item) {
        // 首页和机场推荐页面优先级最高
        if (item.url === 'https://jichang-top.com/' ||
            item.url === 'https://jichang-top.com/airport') {
          item.priority = 1.0;
          item.changefreq = 'daily';
        }
        // 分类页面高优先级
        else if (item.url.includes('/categories/')) {
          item.priority = 0.8;
          item.changefreq = 'weekly';
        }
        // 文章页面中等优先级
        else if (item.url.includes('/p/')) {
          item.priority = 0.7;
          item.changefreq = 'monthly';
        }
        return item;
      },
    })
  ],
  vite: {
    plugins: [tailwindcss()]
  },
  markdown: {
    shikiConfig: {
      theme: 'nord',
    },
  },
});