import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';

export async function GET(context: { site: URL }) {
  const posts = await getCollection('posts', ({ data }: { data: { draft?: boolean } }) => !data.draft);
  const sorted = posts.sort((a: { data: { date: Date } }, b: { data: { date: Date } }) => b.data.date.valueOf() - a.data.date.valueOf());

  return rss({
    title: '机场TOP - 最新机场评测与科学上网指南',
    description: '专注于机场评测与科学上网工具推荐',
    site: context.site,
    items: sorted.map((post: { data: { title: string; description?: string; date: Date; slug?: string }; id: string }) => ({
      title: post.data.title,
      description: post.data.description || '',
      pubDate: post.data.date,
      link: `/p/${post.data.slug || post.id.replace(/\.md$/, '')}/`,
    })),
  });
}
