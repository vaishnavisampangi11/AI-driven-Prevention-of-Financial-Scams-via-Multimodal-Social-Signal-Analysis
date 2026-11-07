import { useEffect, useState } from 'react'
import { Bell, CircleAlert, Siren, TriangleAlert } from 'lucide-react'
import { Link } from 'react-router-dom'
import { alertsApi } from '../services/api'
import AppLayout from '../components/AppLayout'

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([])
  const [filter, setFilter] = useState('All')
  useEffect(() => {
    const load = async () => {
      try {
        const response = await alertsApi.list()
        setAlerts(response.data.data)
      } catch (err) { console.error(err) }
    }
    load()
  }, [])

  const markRead = async (id) => {
    try {
      await alertsApi.markRead(id)
      setAlerts((prev) => prev.map((alert) => alert.id === id ? { ...alert, is_read: true } : alert))
    } catch (err) { console.error(err) }
  }

  const markAllRead = async () => {
    const unread = alerts.filter((alert) => !alert.is_read)
    try {
      await Promise.all(unread.map((alert) => alertsApi.markRead(alert.id)))
      setAlerts((previous) => previous.map((alert) => ({ ...alert, is_read: true })))
    } catch (err) { console.error(err) }
  }

  const visibleAlerts = alerts.filter((alert) => filter === 'All' || (filter === 'Unread' ? !alert.is_read : alert.is_read))
  const unreadCount = alerts.filter((alert) => !alert.is_read).length
  const readCount = alerts.length - unreadCount
  const relativeTime = (value) => {
    const minutes = Math.max(0, Math.floor((Date.now() - new Date(value).getTime()) / 60000))
    if (minutes < 60) return `${minutes} min${minutes === 1 ? '' : 's'} ago`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours} hr${hours === 1 ? '' : 's'} ago`
    const days = Math.floor(hours / 24)
    return `${days} day${days === 1 ? '' : 's'} ago`
  }
  const severityLabel = (severity) => severity === 'MEDIUM' ? 'SUSPICIOUS' : severity === 'HIGH' ? 'HIGH RISK' : severity

  return (
    <AppLayout title="Alerts & notifications">
      <section className="card panel alerts-panel">
        <div className="panel-header"><div><h3>Alerts &amp; Notifications</h3></div><button className="text-action" type="button" disabled={!unreadCount} onClick={markAllRead}>Mark all as read ›</button></div>
        <div className="alert-filters" role="tablist" aria-label="Filter alerts">{['All', 'Unread', 'Read'].map((item) => <button key={item} type="button" role="tab" aria-selected={filter === item} className={filter === item ? 'active' : ''} onClick={() => setFilter(item)}>{item} <span className="alert-tab-count">{item === 'All' ? alerts.length : item === 'Unread' ? unreadCount : readCount}</span></button>)}</div>
        <div className="alerts-list">{visibleAlerts.length ? visibleAlerts.map((alert) => { const AlertIcon = alert.severity === 'CRITICAL' ? Siren : alert.severity === 'HIGH' ? TriangleAlert : CircleAlert; return <article key={alert.id} className={`alert-item${alert.is_read ? ' is-read' : ''}`}><span className={`alert-symbol ${alert.severity.toLowerCase()}`}><AlertIcon size={17} strokeWidth={2} /></span><div className="alert-item-copy"><div className="alert-item-heading"><strong>{severityLabel(alert.severity)} SCAM ALERT</strong>{!alert.is_read && <span className="unread-dot" />}</div><p>{alert.message}</p><time>{relativeTime(alert.created_at)}</time></div><div className="alert-item-actions">{alert.analysis_id ? <Link className={`alert-view ${alert.severity.toLowerCase()}`} to={`/reports/${alert.analysis_id}`} onClick={() => { if (!alert.is_read) markRead(alert.id) }}>View</Link> : <button className="alert-view" type="button" onClick={() => markRead(alert.id)}>{alert.is_read ? 'Read' : 'View'}</button>}</div></article> }) : <div className="empty-state"><Bell size={20} /> No {filter.toLowerCase()} alerts.</div>}</div>
      </section>
    </AppLayout>
  )
}
