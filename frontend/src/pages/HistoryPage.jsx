import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronLeft, ChevronRight, Eye, Plus } from 'lucide-react'
import { historyApi } from '../services/api'
import AppLayout from '../components/AppLayout'

export default function HistoryPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('All types')
  const [riskFilter, setRiskFilter] = useState('All results')
  const [dateFilter, setDateFilter] = useState('Last 7 days')
  const pageSize = 8

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const response = await historyApi.list(page, pageSize)
        setItems(response.data.data.items)
        setTotal(response.data.data.total)
      } catch (err) { console.error(err) } finally { setLoading(false) }
    }
    load()
  }, [page])

  const filteredItems = items.filter((item) => {
    const matchesSearch = `${item.input_type} ${item.classification} ${item.risk_level} ${item.recommendation}`.toLowerCase().includes(search.toLowerCase())
    const matchesType = typeFilter === 'All types' || item.input_type.toLowerCase() === typeFilter.toLowerCase()
    const matchesRisk = riskFilter === 'All results' || item.risk_level.toLowerCase() === riskFilter.toLowerCase()
    const age = Date.now() - new Date(item.created_at).getTime()
    const dateLimit = dateFilter === 'Last 7 days' ? 7 : dateFilter === 'Last 30 days' ? 30 : Infinity
    const matchesDate = age <= dateLimit * 24 * 60 * 60 * 1000
    return matchesSearch && matchesType && matchesRisk && matchesDate
  })
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const firstVisiblePage = Math.max(1, Math.min(page - 2, totalPages - 4))
  const visiblePages = Array.from({ length: Math.min(5, totalPages) }, (_, index) => firstVisiblePage + index)

  return (
    <AppLayout title="Analysis history">
      <section className="card panel history-panel">
        <div className="panel-header"><div><h3>Analysis History</h3></div></div>
        <div className="history-toolbar">
          <select aria-label="Filter by type" value={typeFilter} onChange={(event) => setTypeFilter(event.target.value)}><option>All types</option><option>TEXT</option><option>URL</option><option>QR</option></select>
          <select aria-label="Filter by risk" value={riskFilter} onChange={(event) => setRiskFilter(event.target.value)}><option>All results</option><option>SAFE</option><option>SUSPICIOUS</option><option>HIGH RISK</option><option>CRITICAL</option></select>
          <select aria-label="Filter by date" value={dateFilter} onChange={(event) => setDateFilter(event.target.value)}><option>Last 7 days</option><option>Last 30 days</option><option>All time</option></select>
          <input aria-label="Search analyses" type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by content..." />
        </div>
        <div className="table-scroll"><table className="table history-table">
          <thead><tr><th>Date &amp; Time</th><th>Type</th><th>Classification</th><th>Risk Score</th><th>Risk Level</th><th>Action</th><th>Details</th></tr></thead>
          <tbody>{loading ? <tr><td colSpan="7" className="table-empty">Loading analysis history...</td></tr> : filteredItems.length ? filteredItems.map((item) => <tr key={item.id}><td>{new Date(item.created_at).toLocaleString()}</td><td>{item.input_type}</td><td><span className={`classification-pill ${(item.classification || '').toLowerCase()}`}>{item.classification}</span></td><td><span className="score-pill">{item.risk_score}</span></td><td><span className={`badge ${(item.risk_level || '').toLowerCase().replace(/ /g, '-')}`}>{item.risk_level}</span></td><td>{item.recommendation}</td><td><Link className="table-view" to={`/reports/${item.id}`} aria-label={`View report ${item.id}`} title="View report">View</Link></td></tr>) : <tr><td colSpan="7" className="table-empty">No analyses match these filters.</td></tr>}</tbody>
        </table></div>
        <div className="table-pagination"><span>Showing {total ? (page - 1) * pageSize + 1 : 0}-{Math.min(page * pageSize, total)} of {total}</span><div><button type="button" aria-label="Previous page" disabled={page <= 1} onClick={() => setPage(page - 1)}><ChevronLeft size={15} /></button>{visiblePages.map((pageNumber) => <button key={pageNumber} type="button" className={pageNumber === page ? 'current' : ''} aria-current={pageNumber === page ? 'page' : undefined} onClick={() => setPage(pageNumber)}>{pageNumber}</button>)}<button type="button" aria-label="Next page" disabled={page >= totalPages} onClick={() => setPage(page + 1)}><ChevronRight size={15} /></button></div></div>
      </section>
    </AppLayout>
  )
}
