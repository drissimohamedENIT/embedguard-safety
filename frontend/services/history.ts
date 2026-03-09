import { api } from "./api"
import { AnalysisHistory } from "@/types/analysis"

export async function fetchAnalysisHistory(): Promise<AnalysisHistory[]> {
  const response = await api.get("/analyze/history?limit=50")
  return response.data
}