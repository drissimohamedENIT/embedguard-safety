export interface AnalysisSummary {
  analysis_id: number
  score: number
  total_issues: number
  severity_distribution: Record<string, number>
  criticality_distribution: Record<string, number>
  category_distribution: Record<string, number>
}