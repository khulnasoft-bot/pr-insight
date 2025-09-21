'use client'

import { motion } from 'framer-motion'
import {
  CogIcon,
  KeyIcon,
  GlobeAltIcon,
  BellIcon
} from '@heroicons/react/24/outline'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-between items-center"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-2 text-gray-600">
            Configure your PR-Insight preferences and integrations
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* API Configuration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <KeyIcon className="h-6 w-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">API Configuration</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Backend API URL
              </label>
              <input
                type="url"
                defaultValue="http://localhost:8000"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="http://localhost:8000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Key
              </label>
              <input
                type="password"
                placeholder="Enter your API key"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>
        </motion.div>

        {/* Git Provider Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <GlobeAltIcon className="h-6 w-6 text-green-600" />
            <h2 className="text-xl font-semibold text-gray-900">Git Providers</h2>
          </div>
          <div className="space-y-3">
            {['GitHub', 'GitLab', 'Bitbucket', 'Azure DevOps'].map((provider) => (
              <label key={provider} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <span className="text-gray-700">{provider}</span>
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              </label>
            ))}
          </div>
        </motion.div>

        {/* Notification Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <BellIcon className="h-6 w-6 text-orange-600" />
            <h2 className="text-xl font-semibold text-gray-900">Notifications</h2>
          </div>
          <div className="space-y-3">
            <label className="flex items-center">
              <input type="checkbox" className="mr-3 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-gray-700">Email notifications for completed analyses</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-gray-700">Slack notifications</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3 rounded border-gray-300 text-primary-600 focus:ring-primary-500" />
              <span className="text-gray-700">Webhook notifications</span>
            </label>
          </div>
        </motion.div>

        {/* Advanced Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center space-x-3 mb-4">
            <CogIcon className="h-6 w-6 text-purple-600" />
            <h2 className="text-xl font-semibold text-gray-900">Advanced</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Analysis Timeout (seconds)
              </label>
              <input
                type="number"
                defaultValue="300"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max File Size (MB)
              </label>
              <input
                type="number"
                defaultValue="10"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              Save Settings
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
