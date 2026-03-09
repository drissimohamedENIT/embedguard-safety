
"use client"

import Link from "next/link"
import { useHistory } from "@/hooks/useHistory"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

export default function HistoryTable() {

  const { data, isLoading } = useHistory()

  if (isLoading) {
    return <p>Loading scan history...</p>
  }

  return (
    <Table>

      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Project</TableHead>
          <TableHead>Score</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Date</TableHead>
          <TableHead>Open</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>

        {data?.map((analysis) => (

          <TableRow key={analysis.analysis_id}>

            <TableCell>{analysis.analysis_id}</TableCell>

            <TableCell className="max-w-[300px] truncate">
              {analysis.filename}
            </TableCell>

            <TableCell>{analysis.score}</TableCell>

            <TableCell>
              <StatusBadge status={analysis.status} />
            </TableCell>

            <TableCell>
              {new Date(analysis.created_at).toLocaleString()}
            </TableCell>

            <TableCell>
              <Link
                href={`/analysis/${analysis.analysis_id}`}
                className="text-blue-400 hover:underline"
              >
                View
              </Link>
            </TableCell>

          </TableRow>

        ))}

      </TableBody>

    </Table>
  )
}

function StatusBadge({ status }: { status: string }) {

  if (status === "completed")
    return <Badge className="bg-green-600">completed</Badge>

  if (status === "failed")
    return <Badge className="bg-red-600">failed</Badge>

  return <Badge className="bg-yellow-600">processing</Badge>
}