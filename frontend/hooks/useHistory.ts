"use client"

import { useQuery } from "@tanstack/react-query"
import { fetchAnalysisHistory } from "@/services/history"

export function useHistory() {
  return useQuery({
    queryKey: ["analysis-history"],
    queryFn: fetchAnalysisHistory,
    refetchInterval: 10000
  })
}