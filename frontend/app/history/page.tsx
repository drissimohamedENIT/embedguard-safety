"use client"

import MainLayout from "@/components/layout/main-layout"
import HistoryTable from "@/components/analysis/history-table"

export default function HistoryPage() {

  return (
    <MainLayout>

      <h1 className="text-3xl font-bold mb-8">
        Scan History
      </h1>

      <HistoryTable />

    </MainLayout>
  )
}