import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.coerce.date(),
    lastmod: z.coerce.date().optional(),
    image: z.string().optional(),
    categories: z.array(z.string()).default([]),
    tags: z.array(z.string()).default([]),
    slug: z.string().optional(),
    draft: z.boolean().default(false),
    rating: z.number().optional(),
    speed: z.number().optional(),
    stability: z.number().optional(),
    service: z.number().optional(),
    price: z.number().optional(),
  }),
});

export const collections = {
  posts: postsCollection,
};
