"use client"

import { Card } from "@/components/ui/card"
import { AnalysisSummary } from "@/types/summary"

interface Props {
  summary: AnalysisSummary
}

export default function ScorePanel({ summary }: Props) {

  return (
    <div className="grid grid-cols-4 gap-6 mb-8">

      <Card className="p-6 bg-slate-900 border-slate-800">
        <p className="text-sm text-slate-400">Safety Score</p>
        <p className="text-4xl font-bold mt-2">
          {summary.score}
        </p>
      </Card>

      <Card className="p-6 bg-slate-900 border-slate-800">
        <p className="text-sm text-slate-400">Total Issues</p>
        <p className="text-4xl font-bold mt-2">
          {summary.total_issues}
        </p>
      </Card>

      <Card className="p-6 bg-slate-900 border-slate-800">
        <p className="text-sm text-slate-400">Severity Types</p>
        <p className="text-2xl mt-2">
          {Object.keys(summary.severity_distribution).length}
        </p>
      </Card>

      <Card className="p-6 bg-slate-900 border-slate-800">
        <p className="text-sm text-slate-400">Categories</p>
        <p className="text-2xl mt-2">
          {Object.keys(summary.category_distribution).length}
        </p>
      </Card>

    </div>
  )
}