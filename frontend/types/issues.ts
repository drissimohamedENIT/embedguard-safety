export interface Issue {
  id: number
  file: string
  line: number
  column: number
  severity: string
  message: string
  rule: string
  category: string
  criticality: string
}

export interface IssuesResponse {
  analysis_id: number
  page: number
  page_size: number
  total_issues: number
  issues: Issue[]
}