'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import ReviewInterface from '../components/ReviewInterface'
import {
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  CodeBracketIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline'

export default function ToolsInterface() {
  const [activeTool, setActiveTool] = useState('review')

  const tools = [
    {
      id: 'review',
      name: 'AI Review',
      description: 'Comprehensive code review with AI analysis',
      icon: ChatBubbleLeftRightIcon,
      component: ReviewInterface
    },
    {
      id: 'describe',
      name: 'Describe PR',
      description: 'Auto-generate PR descriptions and summaries',
      icon: DocumentTextIcon,
      component: () => <div className="text-center py-12 text-gray-500">Coming Soon</div>
    },
    {
      id: 'improve',
      name: 'Code Improve',
      description: 'Get suggestions for code improvements',
      icon: CodeBracketIcon,
      component: () => <div className="text-center py-12 text-gray-500">Coming Soon</div>
    },
    {
      id: 'ask',
      name: 'Ask Questions',
      description: 'Ask questions about your PR',
      icon: MagnifyingGlassIcon,
      component: () => <div className="text-center py-12 text-gray-500">Coming Soon</div>
    }
  ]

  const activeToolData = tools.find(tool => tool.id === activeTool)

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-between items-center"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900">PR Analysis Tools</h1>
          <p className="mt-2 text-gray-600">
            Choose a tool to analyze your pull request
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Tool Selection Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-1"
        >
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Tools</h2>
            <div className="space-y-2">
              {tools.map((tool) => (
                <button
                  key={tool.id}
                  onClick={() => setActiveTool(tool.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                    activeTool === tool.id
                      ? 'bg-primary-50 text-primary-700 border border-primary-200'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <tool.icon className="h-5 w-5" />
                  <div>
                    <div className="font-medium">{tool.name}</div>
                    <div className="text-sm text-gray-500">{tool.description}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tool Interface */}
        <motion.div
          key={activeTool}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-3"
        >
          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <activeToolData.icon className="h-6 w-6 text-primary-600" />
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {activeToolData.name}
                  </h2>
                  <p className="text-gray-600">
                    {activeToolData.description}
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6">
              <activeToolData.component />
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
