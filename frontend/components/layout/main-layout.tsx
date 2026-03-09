import Sidebar from "./sidebar"

export default function MainLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">

      <Sidebar />

      <main className="flex-1 bg-slate-950 text-white p-8 min-h-screen">
        {children}
      </main>

    </div>
  )
}