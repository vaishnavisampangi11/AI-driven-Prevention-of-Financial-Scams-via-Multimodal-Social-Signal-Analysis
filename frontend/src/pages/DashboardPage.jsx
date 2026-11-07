import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { BadgeAlert, CircleAlert, Link2, MessageSquareText, QrCode, ScanSearch, ShieldCheck, TriangleAlert } from 'lucide-react'
import { dashboardApi } from '../services/api'
import AppLayout from '../components/AppLayout'

const defaultSummary = {
  total: 0,
  safe: 0,
  suspicious: 0,
  high_risk: 0,
  critical: 0,
  recent_analyses: [],
  recent_alerts: [],
}

const relativeTime = (value) => {
  const minutes = Math.max(0, Math.floor((Date.now() - new Date(value).getTime()) / 60000))
  if (minutes < 60) return `${minutes} min${minutes === 1 ? '' : 's'} ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hr${hours === 1 ? '' : 's'} ago`
  const days = Math.floor(hours / 24)
  return `${days} day${days === 1 ? '' : 's'} ago`
}

export default function DashboardPage() {
  const [summary, setSummary] = useState(defaultSummary)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const response = await dashboardApi.summary()
        setSummary(response.data.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const riskBreakdown = useMemo(() => {
    const total = summary.total || 1
    return [
      { label: 'Safe', value: summary.safe, percent: Math.round((summary.safe / total) * 100) },
      { label: 'Suspicious', value: summary.suspicious, percent: Math.round((summary.suspicious / total) * 100) },
      { label: 'High Risk', value: summary.high_risk, percent: Math.round((summary.high_risk / total) * 100) },
      { label: 'Critical', value: summary.critical, percent: Math.round((summary.critical / total) * 100) },
    ]
  }, [summary])

  const [safeEnd, suspiciousEnd, highRiskEnd, criticalEnd] = riskBreakdown.reduce((ends, item) => {
    ends.push((ends.at(-1) || 0) + item.percent)
    return ends
  }, [])
  const distributionStyle = summary.total
    ? { background: `conic-gradient(#12d6ad 0 ${riskBreakdown[0].percent}%, #ffb42f ${riskBreakdown[0].percent}% ${suspiciousEnd}%, #ff6949 ${suspiciousEnd}% ${highRiskEnd}%, #f52d61 ${highRiskEnd}% ${criticalEnd}%, #152a4b ${criticalEnd}% 100%)` }
    : { background: '#152a4b' }

  return (
    <AppLayout title="Dashboard">
      <div className="container dashboard-container">
        <section className="dashboard-welcome">
          <div><h2>Welcome back{localStorage.getItem('user_name') ? `, ${localStorage.getItem('user_name')}` : ''}! <span aria-hidden="true">👋</span></h2><p>Here’s what’s happening with your scam detection system.</p></div>
        </section>
        <section className="hero-grid">
          {[
            { label: 'Total analyses', value: summary.total, Icon: ScanSearch, tone: 'blue', detail: 'Scans completed' },
            { label: 'Safe', value: summary.safe, Icon: ShieldCheck, tone: 'green', detail: 'Low risk' },
            { label: 'Suspicious', value: summary.suspicious, Icon: CircleAlert, tone: 'amber', detail: 'Review recommended' },
            { label: 'High risk', value: summary.high_risk, Icon: TriangleAlert, tone: 'orange', detail: 'Action recommended' },
            { label: 'Critical', value: summary.critical, Icon: BadgeAlert, tone: 'red', detail: 'Immediate attention' },
          ].map((item) => <div key={item.label} className="card metric-stat"><div className="metric-stat-top"><span className="tiny-label">{item.label}</span><span className={`metric-icon ${item.tone}`}><item.Icon size={17} strokeWidth={2} /></span></div><strong>{item.value}</strong><span className="muted">{item.detail}</span></div>)}
        </section>

        <section className="dashboard-panels">
          <div className="card panel distribution-panel">
            <div className="panel-header"><h3>Risk Distribution</h3></div>
            <div className="distribution-content"><div className="distribution-ring" style={distributionStyle}><div><strong>{summary.total}</strong><span>Total</span></div></div><div className="distribution-legend">{riskBreakdown.map((item) => <div key={item.label}><span className={`dot ${item.label.toLowerCase().replace(/\s+/g, '-')}`} /><span>{item.label}</span><strong>{item.percent}%</strong></div>)}</div></div>
          </div>

          <div className="card panel recent-analysis-panel">
            <div className="panel-header"><h3>Recent Analyses</h3><Link className="secondary-btn" to="/history">View all</Link></div>
            {loading ? <div className="empty-state">Loading analyses...</div> : <div className="recent-table-wrap"><table className="recent-table"><thead><tr><th>Type</th><th>Result</th><th>Risk</th><th>Time</th></tr></thead><tbody>{summary.recent_analyses.length ? summary.recent_analyses.slice(0, 5).map((item) => <tr key={item.id}><td>{item.input_type}</td><td><span className={`badge ${(item.risk_level || '').toLowerCase().replace(/ /g, '-')}`}>{item.risk_level}</span></td><td>{item.risk_score}</td><td>{relativeTime(item.created_at)}</td></tr>) : <tr><td colSpan="4" className="table-empty">No recent analyses.</td></tr>}</tbody></table></div>}
          </div>

          <div className="card panel recent-alerts-panel">
            <div className="panel-header"><h3>Recent Alerts</h3><Link className="secondary-btn" to="/alerts">View all</Link></div>
            <div className="dashboard-alert-list">{summary.recent_alerts.length ? summary.recent_alerts.slice(0, 4).map((item) => <div key={item.id} className="dashboard-alert-item"><span className={`dashboard-alert-icon ${item.severity.toLowerCase()}`}><TriangleAlert size={15} /></span><div><strong>{item.severity} SCAM ALERT</strong><p>{item.message}</p><time>{relativeTime(item.created_at)}</time></div></div>) : <div className="empty-state">No recent alerts.</div>}</div>
          </div>
        </section>

        <section className="quick-analysis"><h3>Quick Analysis</h3><div className="quick-analysis-actions"><Link className="quick-analysis-button quick-text" to="/analysis?mode=text"><MessageSquareText size={17} /> Analyze Text / Message</Link><Link className="quick-analysis-button quick-url" to="/analysis?mode=url"><Link2 size={17} /> Analyze URL</Link><Link className="quick-analysis-button quick-qr" to="/analysis?mode=qr"><QrCode size={17} /> Scan QR Code</Link></div></section>
      </div>
    </AppLayout>
  )
}
