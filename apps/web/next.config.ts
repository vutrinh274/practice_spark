import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  turbopack: {
    resolveAlias: {
      fs: { browser: "./lib/empty.ts" },
      path: { browser: "./lib/empty.ts" },
      os: { browser: "./lib/empty.ts" },
    },
  },
};

export default nextConfig;
