import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '../globals.css'
import Layout from '../components/Layout'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'PR-Insight - AI-Powered Code Review Platform',
  description: 'Enhance your code review process with intelligent AI analysis. Get comprehensive feedback, suggestions, and insights for better code quality.',
  keywords: 'AI, code review, pull request, automation, GitHub, GitLab, Bitbucket',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Layout>{children}</Layout>
      </body>
    </html>
  )
}
