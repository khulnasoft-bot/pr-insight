import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface PRReviewRequest {
  repository_url: string
  pr_number: number
  include_security_scan?: boolean
  include_performance_analysis?: boolean
}

export interface PRReviewResponse {
  id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result?: any
  error?: string
}

export interface ToolResult {
  id: string
  tool_name: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result?: any
  created_at: string
  updated_at: string
}

class PRInsightAPI {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  async reviewPR(request: PRReviewRequest): Promise<PRReviewResponse> {
    const response = await axios.post(`${this.baseURL}/api/review`, request)
    return response.data
  }

  async getReviewStatus(reviewId: string): Promise<PRReviewResponse> {
    const response = await axios.get(`${this.baseURL}/api/review/${reviewId}`)
    return response.data
  }

  async describePR(repository_url: string, pr_number: number): Promise<PRReviewResponse> {
    const response = await axios.post(`${this.baseURL}/api/describe`, {
      repository_url,
      pr_number
    })
    return response.data
  }

  async improveCode(repository_url: string, pr_number: number): Promise<PRReviewResponse> {
    const response = await axios.post(`${this.baseURL}/api/improve`, {
      repository_url,
      pr_number
    })
    return response.data
  }

  async askQuestion(repository_url: string, pr_number: number, question: string): Promise<PRReviewResponse> {
    const response = await axios.post(`${this.baseURL}/api/ask`, {
      repository_url,
      pr_number,
      question
    })
    return response.data
  }

  async getToolsHistory(): Promise<ToolResult[]> {
    const response = await axios.get(`${this.baseURL}/api/tools/history`)
    return response.data
  }

  async getToolResult(toolId: string): Promise<ToolResult> {
    const response = await axios.get(`${this.baseURL}/api/tools/${toolId}`)
    return response.data
  }
}

export const api = new PRInsightAPI()
