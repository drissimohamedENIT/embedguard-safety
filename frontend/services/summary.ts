
import { api } from "./api"
import { AnalysisSummary } from "@/types/summary"

export async function fetchAnalysisSummary(
  analysisId: number
): Promise<AnalysisSummary> {

  const response = await api.get(`/analyze/${analysisId}/summary`)

  return response.data
}