'use client';

import { useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { getBuilding, searchBuildings } from '@/lib/api';

type WebMCPTool = {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  execute: (input: unknown, agent?: unknown) => unknown | Promise<unknown>;
};

type WebMCPNavigator = Navigator & {
  modelContext?: {
    registerTool: (tool: WebMCPTool) => void;
    unregisterTool: (name: string) => void;
  };
};

export function WebMCPTools() {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const modelContext = (navigator as WebMCPNavigator).modelContext;
    if (!modelContext) return;

    const searchToolName = 'search-nyc-buildings';
    const reportToolName = 'get-building-report';
    const openToolName = 'open-building-page';

    modelContext.registerTool({
      name: searchToolName,
      description:
        'Search NYC buildings by address or landlord name and return likely matches with BBL IDs.',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Address or landlord name search query.',
          },
          limit: {
            type: 'number',
            description: 'Maximum number of results to return (default 10).',
          },
        },
        required: ['query'],
      },
      execute: async (input: unknown) => {
        const query =
          input && typeof input === 'object' && 'query' in input
            ? String((input as { query?: unknown }).query ?? '')
            : '';
        const requestedLimit =
          input && typeof input === 'object' && 'limit' in input
            ? Number((input as { limit?: unknown }).limit)
            : 10;

        const limit = Number.isFinite(requestedLimit)
          ? Math.max(1, Math.min(25, Math.floor(requestedLimit)))
          : 10;

        if (!query.trim()) {
          throw new Error('query is required');
        }

        const results = await searchBuildings(query, limit);
        return { query, count: results.length, results };
      },
    });

    modelContext.registerTool({
      name: reportToolName,
      description:
        'Get a full public building report by BBL, including score, violations, complaints, and ownership.',
      inputSchema: {
        type: 'object',
        properties: {
          bbl: {
            type: 'string',
            description: 'NYC BBL identifier for the building.',
          },
        },
        required: ['bbl'],
      },
      execute: async (input: unknown) => {
        const bbl =
          input && typeof input === 'object' && 'bbl' in input
            ? String((input as { bbl?: unknown }).bbl ?? '')
            : '';
        if (!bbl.trim()) {
          throw new Error('bbl is required');
        }

        const report = await getBuilding(bbl);
        return report;
      },
    });

    modelContext.registerTool({
      name: openToolName,
      description:
        'Open the detailed building page for a given BBL in the current tab.',
      inputSchema: {
        type: 'object',
        properties: {
          bbl: {
            type: 'string',
            description: 'NYC BBL identifier for the building.',
          },
        },
        required: ['bbl'],
      },
      execute: (input: unknown) => {
        const bbl =
          input && typeof input === 'object' && 'bbl' in input
            ? String((input as { bbl?: unknown }).bbl ?? '')
            : '';
        if (!bbl.trim()) {
          throw new Error('bbl is required');
        }

        const path = `/building/${bbl}`;
        router.push(path);
        return { ok: true, path };
      },
    });

    return () => {
      try {
        modelContext.unregisterTool(searchToolName);
        modelContext.unregisterTool(reportToolName);
        modelContext.unregisterTool(openToolName);
      } catch {
        // Ignore cleanup race during route changes/hot reload.
      }
    };
  }, [pathname, router]);

  return null;
}
