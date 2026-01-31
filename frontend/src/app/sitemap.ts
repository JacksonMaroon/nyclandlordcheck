import type { MetadataRoute } from 'next';

const baseUrl = 'https://www.nyclandlordcheck.com';
const lastModified = new Date();

const routes = [
  '/',
  '/about',
  '/data-sources',
  '/leaderboard/buildings',
  '/leaderboard/landlords',
  '/map',
  '/methodology',
  '/neighborhoods',
  '/violations/recent',
];

export default function sitemap(): MetadataRoute.Sitemap {
  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified,
  }));
}
