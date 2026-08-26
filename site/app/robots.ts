import type { MetadataRoute } from "next";

const siteUrl = "https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
    },
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
