'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { PlayIcon, ArrowPathIcon } from '@heroicons/react/24/outline'
import { api, PRReviewRequest } from '../lib/api'

export default function ReviewInterface() {
  const [formData, setFormData] = useState<PRReviewRequest>({
    repository_url: '',
    pr_number: 0,
    include_security_scan: false,
    include_performance_analysis: false
  })
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string>('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await api.reviewPR(formData)
      setResult(response)

      // Poll for status updates if needed
      if (response.status === 'pending' || response.status === 'processing') {
        const interval = setInterval(async () => {
          const statusResponse = await api.getReviewStatus(response.id)
          setResult(statusResponse)

          if (statusResponse.status === 'completed' || statusResponse.status === 'failed') {
            clearInterval(interval)
            setIsLoading(false)
          }
        }, 2000)

        setTimeout(() => clearInterval(interval), 30000) // Stop polling after 30 seconds
      } else {
        setIsLoading(false)
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to start review')
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200"
      >
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900">AI Code Review</h2>
          <p className="mt-2 text-gray-600">
            Get comprehensive AI-powered analysis of your pull request
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="repository_url" className="block text-sm font-medium text-gray-700 mb-2">
                Repository URL
              </label>
              <input
                type="url"
                id="repository_url"
                value={formData.repository_url}
                onChange={(e) => setFormData({...formData, repository_url: e.target.value})}
                placeholder="https://github.com/owner/repo"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label htmlFor="pr_number" className="block text-sm font-medium text-gray-700 mb-2">
                Pull Request Number
              </label>
              <input
                type="number"
                id="pr_number"
                value={formData.pr_number || ''}
                onChange={(e) => setFormData({...formData, pr_number: parseInt(e.target.value)})}
                placeholder="123"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              Analysis Options
            </label>
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.include_security_scan}
                  onChange={(e) => setFormData({...formData, include_security_scan: e.target.checked})}
                  className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                Security Scan
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.include_performance_analysis}
                  onChange={(e) => setFormData({...formData, include_performance_analysis: e.target.checked})}
                  className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                Performance Analysis
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <ArrowPathIcon className="h-5 w-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <PlayIcon className="h-5 w-5" />
                <span>Start Review</span>
              </>
            )}
          </button>
        </form>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-6 border-t border-red-200 bg-red-50"
          >
            <p className="text-red-800">{error}</p>
          </motion.div>
        )}

        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-6 border-t border-gray-200"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Review Status: {result.status}
            </h3>

            {result.result && (
              <div className="bg-gray-50 rounded-lg p-4">
                <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                  {JSON.stringify(result.result, null, 2)}
                </pre>
              </div>
            )}
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}
