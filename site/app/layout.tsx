import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { headers } from "next/headers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("host") ?? "localhost";
  const protocol =
    requestHeaders.get("x-forwarded-proto") ??
    (host.startsWith("localhost") ? "http" : "https");
  const imageUrl = `${protocol}://${host}/og.png`;

  return {
    title: "Codex Skill Benchmark — Codex How To",
    description:
      "Explore six controlled GPT-5.6-sol runs showing when an engineering skill helped—and when it added overhead.",
    icons: {
      icon: "/favicon.svg",
      shortcut: "/favicon.svg",
    },
    openGraph: {
      title: "Do Codex skills save tokens? It depends.",
      description:
        "Six controlled GPT-5.6-sol runs reveal a task-size boundary worth replicating.",
      type: "website",
      images: [
        {
          url: imageUrl,
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
      images: [imageUrl],
    },
  };
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
