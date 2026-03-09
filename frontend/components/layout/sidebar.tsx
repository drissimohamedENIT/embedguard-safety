import Link from "next/link"
import { LayoutDashboard, Upload, History } from "lucide-react"

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-slate-900 text-white p-4">
      <h1 className="text-xl font-bold mb-8">EmbedGuard</h1>

      <nav className="space-y-4">

        <Link href="/dashboard" className="flex items-center gap-2 hover:text-blue-400">
          <LayoutDashboard size={18} />
          Dashboard
        </Link>

        <Link href="/scan" className="flex items-center gap-2 hover:text-blue-400">
          <Upload size={18} />
          New Scan
        </Link>

        <Link href="/history" className="flex items-center gap-2 hover:text-blue-400">
          <History size={18} />
          Scan History
        </Link>

      </nav>
    </div>
  )
}