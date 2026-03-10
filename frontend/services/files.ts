import { api } from "./api"

export interface AnalysisFile {
  file: string
  issues: number
}

export interface AnalysisFilesResponse {
  analysis_id: number
  files: AnalysisFile[]
}

export async function fetchAnalysisFiles(
  analysisId: number
): Promise<AnalysisFilesResponse> {

  const response = await api.get(`/analyze/${analysisId}/files`)

  return response.data
}