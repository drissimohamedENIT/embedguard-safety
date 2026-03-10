import { api } from "./api"
import { AnalysisFilesResponse } from "@/types/files"

export async function fetchAnalysisFiles(
  analysisId: number
): Promise<AnalysisFilesResponse> {

  const response = await api.get(`/analyze/${analysisId}/files`)

  return response.data
}