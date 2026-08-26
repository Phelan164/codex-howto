import type { MetadataRoute } from "next";

const siteUrl = "https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: siteUrl,
      changeFrequency: "monthly",
      priority: 1,
    },
  ];
}
