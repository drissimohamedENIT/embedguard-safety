"use client"

import { useState } from "react"
import { useIssues } from "@/hooks/useIssues"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

interface Props {
  analysisId: number
}

export default function IssuesTable({ analysisId }: Props) {

  const [page, setPage] = useState(1)

  const { data, isLoading } = useIssues(analysisId, page)

  if (isLoading) {
    return <p className="text-slate-400">Loading issues...</p>
  }

  return (
    <div>

      <Table>

        <TableHeader>
          <TableRow>
            <TableHead>Severity</TableHead>
            <TableHead>Rule</TableHead>
            <TableHead>File</TableHead>
            <TableHead>Line</TableHead>
            <TableHead>Message</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>

          {data?.issues.map((issue) => (

            <TableRow key={issue.id}>

              <TableCell>
                <Badge>{issue.severity}</Badge>
              </TableCell>

              <TableCell>{issue.rule}</TableCell>

              <TableCell className="truncate">
                {issue.file}
              </TableCell>

              <TableCell>{issue.line}</TableCell>

              <TableCell className="max-w-lg truncate">
                {issue.message}
              </TableCell>

            </TableRow>

          ))}

        </TableBody>

      </Table>

      <div className="flex justify-between mt-4">

        <button
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
        >
          Previous
        </button>

        <span>Page {page}</span>

        <button
          onClick={() => setPage((p) => p + 1)}
        >
          Next
        </button>

      </div>

    </div>
  )
}