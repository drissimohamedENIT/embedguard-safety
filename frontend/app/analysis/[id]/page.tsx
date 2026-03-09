
"use client"

import { useParams } from "next/navigation"
import MainLayout from "@/components/layout/main-layout"
import ScorePanel from "@/components/analysis/score-panel"
import { useAnalysisSummary } from "@/hooks/useAnalysisSummary"

export default function AnalysisPage() {

  const params = useParams()

  const analysisId = Number(params.id)

  const { data, isLoading } = useAnalysisSummary(analysisId)

  return (
    <MainLayout>

      <h1 className="text-3xl font-bold mb-6">
        Analysis {analysisId}
      </h1>

      {isLoading && <p>Loading analysis summary...</p>}

      {data && (
        <>
          <ScorePanel summary={data} />
        </>
      )}

    </MainLayout>
  )
}