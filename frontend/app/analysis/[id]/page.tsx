"use client"

import { useParams } from "next/navigation"

import MainLayout from "@/components/layout/main-layout"

import ScorePanel from "@/components/analysis/score-panel"
import FileTree from "@/components/analysis/file-tree"

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

      {isLoading && (
        <p className="text-slate-400">
          Loading analysis summary...
        </p>
      )}

      {data && (
        <>

          {/* Score panel */}
          <ScorePanel summary={data} />

          {/* Main explorer layout */}
          <div className="grid grid-cols-4 gap-6">

            {/* File explorer */}
            <div className="col-span-1">

              <FileTree analysisId={analysisId} />

            </div>

            {/* Issues panel (next step) */}
            <div className="col-span-3">

              <div className="p-6 bg-slate-900 border border-slate-800 rounded-lg">

                <h2 className="text-xl font-semibold mb-4">
                  Issues
                </h2>

                <p className="text-slate-400">
                  Issues table will appear here in the next step.
                </p>

              </div>

            </div>

          </div>

        </>
      )}

    </MainLayout>
  )
}