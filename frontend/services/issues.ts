import { api } from "./api"
import { IssuesResponse } from "@/types/issues"

export async function fetchIssues(
  analysisId: number,
  page = 1
): Promise<IssuesResponse> {

  const response = await api.get(
    `/analyze/${analysisId}/issues?page=${page}`
  )

  return response.data
}