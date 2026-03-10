"use client"

import { useAnalysisFiles } from "@/hooks/useAnalysisFiles"
import { Card } from "@/components/ui/card"

interface FileTreeProps {
  analysisId: number
}

export default function FileTree({ analysisId }: FileTreeProps) {

  const { data, isLoading } = useAnalysisFiles(analysisId)

  if (isLoading) {
    return (
      <Card className="p-4 bg-slate-900 border-slate-800">
        <p className="text-slate-400">Loading files...</p>
      </Card>
    )
  }

  return (
    <Card className="p-4 bg-slate-900 border-slate-800 h-full overflow-auto">

      <h2 className="text-lg font-semibold mb-4">
        Files
      </h2>

      <div className="space-y-2">

        {data?.files.map((file) => (

          <div
            key={file.file}
            className="flex justify-between items-center p-2 rounded hover:bg-slate-800 cursor-pointer"
          >

            <span className="truncate">
              {file.file}
            </span>

            <span className="text-sm text-slate-400">
              {file.issues}
            </span>

          </div>

        ))}

      </div>

    </Card>
  )
}