"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchAnalysisSummary } from "@/services/summary"

export function useAnalysisSummary(analysisId: number) {

  return useQuery({
    queryKey: ["analysis-summary", analysisId],
    queryFn: () => fetchAnalysisSummary(analysisId),
    enabled: !!analysisId
  })
}