"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchIssues } from "@/services/issues"

export function useIssues(analysisId: number, page: number) {

  return useQuery({
    queryKey: ["issues", analysisId, page],
    queryFn: () => fetchIssues(analysisId, page),
    enabled: !!analysisId
  })
}