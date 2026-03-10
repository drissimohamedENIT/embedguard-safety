"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchAnalysisFiles } from "@/services/files"

export function useAnalysisFiles(analysisId: number) {

  return useQuery({
    queryKey: ["analysis-files", analysisId],
    queryFn: () => fetchAnalysisFiles(analysisId),
    enabled: !!analysisId
  })
}