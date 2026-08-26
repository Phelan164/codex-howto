import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const siteUrl = new URL(
  "https://codex-howto-benchmark.nguyenvantamdk2.chatgpt.site",
);
const repositoryUrl = "https://github.com/Phelan164/codex-howto";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: siteUrl,
  title: "Codex Skill Benchmark — Codex How To",
  description:
    "Explore six controlled GPT-5.6-sol runs showing when an engineering skill helped—and when it added overhead.",
  alternates: {
    canonical: "/",
  },
  authors: [{ name: "Codex How To contributors", url: repositoryUrl }],
  creator: "Codex How To contributors",
  keywords: [
    "OpenAI Codex",
    "Codex skills",
    "engineering loop",
    "AI coding agents",
    "agent skills benchmark",
    "software engineering workflow",
  ],
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
  openGraph: {
    title: "Do Codex skills save tokens? It depends.",
    description:
      "Six controlled GPT-5.6-sol runs reveal a task-size boundary worth replicating.",
    type: "website",
    url: "/",
    siteName: "Codex How To",
    images: [
      {
        url: "/og.png",
        width: 1728,
        height: 907,
        alt: "Do Codex skills save tokens? It depends. Six runs, two task sizes, all passed.",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Do Codex skills save tokens? It depends.",
    description:
      "Explore six controlled GPT-5.6-sol runs and reproduce the result.",
    images: ["/og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Codex How To benchmark",
    url: siteUrl.toString(),
    description:
      "A reproducible benchmark for measuring when Codex engineering skills improve token efficiency.",
    sameAs: repositoryUrl,
  };

  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
