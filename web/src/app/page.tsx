'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import {
  ChatBubbleLeftRightIcon,
  CodeBracketIcon,
  MagnifyingGlassIcon,
  DocumentTextIcon,
  CogIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

export default function HomePage() {
  const tools = [
    {
      name: 'AI Review',
      description: 'Get comprehensive AI-powered code reviews with suggestions',
      icon: ChatBubbleLeftRightIcon,
      href: '/tools/review',
      color: 'bg-blue-500'
    },
    {
      name: 'Describe PR',
      description: 'Auto-generate PR descriptions, titles, and summaries',
      icon: DocumentTextIcon,
      href: '/tools/describe',
      color: 'bg-green-500'
    },
    {
      name: 'Code Improve',
      description: 'Get AI suggestions for improving your code quality',
      icon: CodeBracketIcon,
      href: '/tools/improve',
      color: 'bg-purple-500'
    },
    {
      name: 'Ask Questions',
      description: 'Ask questions about your PR and get detailed answers',
      icon: MagnifyingGlassIcon,
      href: '/tools/ask',
      color: 'bg-orange-500'
    }
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold text-gray-900 sm:text-6xl">
          AI-Powered PR Reviews
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
          Enhance your code review process with intelligent AI analysis.
          Get comprehensive feedback, suggestions, and insights for better code quality.
        </p>
        <div className="mt-8 flex items-center justify-center gap-x-6">
          <Link
            href="/dashboard"
            className="rounded-lg bg-primary-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-primary-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Get Started
            <ArrowRightIcon className="ml-2 h-5 w-5 inline" />
          </Link>
          <Link
            href="/docs"
            className="text-base font-semibold leading-6 text-gray-900 hover:text-primary-600"
          >
            Learn more →
          </Link>
        </div>
      </motion.div>

      {/* Tools Grid */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {tools.map((tool, index) => (
          <Link key={tool.name} href={tool.href}>
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className={`w-12 h-12 ${tool.color} rounded-lg flex items-center justify-center mb-4`}>
                <tool.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {tool.name}
              </h3>
              <p className="text-gray-600 text-sm">
                {tool.description}
              </p>
            </motion.div>
          </Link>
        ))}
      </motion.div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8"
      >
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900">
            Why Choose PR-Insight?
          </h2>
          <p className="mt-4 text-gray-600">
            Built for developers, by developers
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CogIcon className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Fast & Efficient
            </h3>
            <p className="text-gray-600">
              Get AI-powered reviews in seconds, not hours
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CodeBracketIcon className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Multi-Platform
            </h3>
            <p className="text-gray-600">
              Support for GitHub, GitLab, Bitbucket, and Azure DevOps
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <ChatBubbleLeftRightIcon className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Customizable
            </h3>
            <p className="text-gray-600">
              Tailor AI behavior to your team's specific needs
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
