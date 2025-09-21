'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import {
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  CodeBracketIcon,
  MagnifyingGlassIcon,
  WrenchScrewdriverIcon,
  ShieldCheckIcon,
  ClipboardDocumentListIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline'

export default function ToolsPage() {
  const tools = [
    {
      name: 'AI Review',
      description: 'Comprehensive code review with security analysis, performance insights, and best practice suggestions.',
      icon: ChatBubbleLeftRightIcon,
      href: '/tools/review',
      category: 'Core',
      color: 'bg-blue-500',
      features: ['Security Analysis', 'Performance Review', 'Code Quality', 'Best Practices']
    },
    {
      name: 'Describe PR',
      description: 'Auto-generate detailed PR descriptions, titles, and summaries based on code changes.',
      icon: DocumentTextIcon,
      href: '/tools/describe',
      category: 'Documentation',
      color: 'bg-green-500',
      features: ['Auto Title', 'Summary Generation', 'Code Walkthrough', 'Label Suggestions']
    },
    {
      name: 'Code Improve',
      description: 'Get AI-powered suggestions for improving code quality, efficiency, and maintainability.',
      icon: CodeBracketIcon,
      href: '/tools/improve',
      category: 'Enhancement',
      color: 'bg-purple-500',
      features: ['Code Suggestions', 'Refactoring Ideas', 'Performance Tips', 'Style Improvements']
    },
    {
      name: 'Ask Questions',
      description: 'Ask specific questions about your PR and get detailed, context-aware answers.',
      icon: MagnifyingGlassIcon,
      href: '/tools/ask',
      category: 'Interaction',
      color: 'bg-orange-500',
      features: ['Context-Aware Q&A', 'Code Explanation', 'Architecture Insights', 'Troubleshooting']
    },
    {
      name: 'Test Generation',
      description: 'Generate comprehensive unit tests for your code changes automatically.',
      icon: ShieldCheckIcon,
      href: '/tools/test',
      category: 'Testing',
      color: 'bg-red-500',
      features: ['Unit Test Generation', 'Test Coverage Analysis', 'Mock Data Creation', 'Test Scenarios']
    },
    {
      name: 'Documentation',
      description: 'Auto-generate documentation for methods, classes, and functions in your PR.',
      icon: ClipboardDocumentListIcon,
      href: '/tools/docs',
      category: 'Documentation',
      color: 'bg-indigo-500',
      features: ['API Documentation', 'Method Docs', 'Class Documentation', 'Usage Examples']
    }
  ]

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900">PR Analysis Tools</h1>
        <p className="mt-4 text-gray-600 max-w-2xl mx-auto">
          Powerful AI-driven tools to enhance your code review process and improve code quality
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        {tools.map((tool, index) => (
          <motion.div
            key={tool.name}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 ${tool.color} rounded-lg flex items-center justify-center`}>
                <tool.icon className="h-6 w-6 text-white" />
              </div>
              <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full">
                {tool.category}
              </span>
            </div>

            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {tool.name}
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              {tool.description}
            </p>

            <div className="space-y-2 mb-6">
              <h4 className="text-sm font-medium text-gray-900">Features:</h4>
              <ul className="space-y-1">
                {tool.features.map((feature, idx) => (
                  <li key={idx} className="text-sm text-gray-600 flex items-center">
                    <div className="w-1.5 h-1.5 bg-primary-600 rounded-full mr-2" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            <Link
              href={tool.href}
              className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors text-center block"
            >
              Try {tool.name}
            </Link>
          </motion.div>
        ))}
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="flex items-center justify-center space-x-2 bg-gray-50 hover:bg-gray-100 px-4 py-3 rounded-lg transition-colors">
            <WrenchScrewdriverIcon className="h-5 w-5 text-gray-600" />
            <span className="text-gray-700">Bulk Analysis</span>
          </button>
          <button className="flex items-center justify-center space-x-2 bg-gray-50 hover:bg-gray-100 px-4 py-3 rounded-lg transition-colors">
            <CpuChipIcon className="h-5 w-5 text-gray-600" />
            <span className="text-gray-700">Custom Prompts</span>
          </button>
          <button className="flex items-center justify-center space-x-2 bg-gray-50 hover:bg-gray-100 px-4 py-3 rounded-lg transition-colors">
            <ShieldCheckIcon className="h-5 w-5 text-gray-600" />
            <span className="text-gray-700">Security Scan</span>
          </button>
        </div>
      </motion.div>
    </div>
  )
}
