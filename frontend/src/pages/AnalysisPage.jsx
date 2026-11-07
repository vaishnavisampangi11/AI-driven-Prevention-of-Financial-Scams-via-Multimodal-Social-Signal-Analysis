import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Camera, CheckCircle2, FileText, Globe, Link2, LockKeyhole, MessageSquareText, QrCode, ScanSearch, ShieldCheck, UploadCloud } from 'lucide-react'
import { analysisApi } from '../services/api'
import AppLayout from '../components/AppLayout'

const tabs = ['text', 'url', 'qr']
const tabIcons = { text: FileText, url: Link2, qr: QrCode }

export default function AnalysisPage() {
  const [searchParams] = useSearchParams()
  const cameraInputRef = useRef(null)
  const requestedMode = searchParams.get('mode')
  const [tab, setTab] = useState(tabs.includes(requestedMode) ? requestedMode : 'text')
  const [textForm, setTextForm] = useState({ input_text: '', source_type: 'Other' })
  const [urlForm, setUrlForm] = useState({ url: '' })
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const query = searchParams.get('query')
    if (!query) return
    if (/^https?:\/\//i.test(query)) {
      setTab('url')
      setUrlForm((current) => ({ ...current, url: query }))
    } else {
      setTab('text')
      setTextForm((current) => ({ ...current, input_text: query }))
    }
  }, [searchParams])

  const handleTextSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError(''); setResult(null)
    try {
      const response = await analysisApi.text(textForm)
      setResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to analyze message.')
    } finally { setLoading(false) }
  }

  const handleUrlSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError(''); setResult(null)
    try {
      const response = await analysisApi.url(urlForm)
      setResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to analyze URL.')
    } finally { setLoading(false) }
  }

  const analyzeQrFile = async (selectedFile) => {
    setLoading(true); setError(''); setResult(null)
    if (!selectedFile) { setError('Please select a QR image.'); setLoading(false); return }
    const formData = new FormData(); formData.append('file', selectedFile)
    try {
      const response = await analysisApi.qr(formData)
      setResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to analyze QR code.')
    } finally { setLoading(false) }
  }

  const handleQrSubmit = (event) => {
    event.preventDefault()
    analyzeQrFile(file)
  }

  const selectQrFile = (selectedFile) => {
    if (!selectedFile) return
    setFile(selectedFile)
    analyzeQrFile(selectedFile)
  }

  const modeContent = {
    text: { title: 'Analyze a message', description: 'Enter a message to detect scam language and requests.', Icon: MessageSquareText },
    url: { title: 'Check any URL', description: 'Check a website for phishing and malicious behavior.', Icon: Globe },
    qr: { title: 'Scan a QR code', description: 'Detect potential risks and extract safe information.', Icon: QrCode },
  }[tab]
  const AsideIcon = modeContent.Icon

  return (
    <AppLayout title={tab === 'url' ? 'URL Analysis' : tab === 'qr' ? 'QR Code Analysis' : 'Text / Message Analysis'}>
      <div className="analysis-page-grid">
        <section className="card panel analysis-workspace">
          <div className="page-intro"><h2>{tab === 'url' ? 'URL Analysis' : tab === 'qr' ? 'QR Code Analysis' : 'Text / Message Analysis'}</h2></div>
          <div className="analysis-tabs" role="tablist" aria-label="Analysis type">
            {tabs.map((item) => { const TabIcon = tabIcons[item]; return <button key={item} type="button" role="tab" aria-selected={tab === item} className={`tab-btn ${tab === item ? 'active' : ''}`} onClick={() => { setTab(item); setResult(null); setError('') }}><TabIcon size={15} strokeWidth={1.9} /> {item === 'text' ? 'Text / Message' : item === 'url' ? 'URL' : 'QR Code'}</button> })}
          </div>

          {tab === 'text' && <form className="analysis-form" onSubmit={handleTextSubmit}>
            <div className="form-row"><label htmlFor="input-text">Message content</label><textarea id="input-text" rows="7" maxLength="4000" value={textForm.input_text} onChange={(e) => setTextForm({ ...textForm, input_text: e.target.value })} placeholder="Paste a suspicious SMS, email, or chat message" required /><span className="field-hint">{textForm.input_text.length}/4000 characters</span></div>
            <div className="form-row"><label>Message type</label><div className="source-options">{['SMS', 'Email', 'Chat', 'Other'].map((source) => <label key={source} className={`source-option${textForm.source_type === source ? ' selected' : ''}`}><input type="radio" name="source_type" value={source} checked={textForm.source_type === source} onChange={() => setTextForm({ ...textForm, source_type: source })} />{source}</label>)}</div></div>
            <button className="primary-btn analysis-submit" disabled={loading}><ScanSearch size={16} /> {loading ? 'Analyzing message...' : 'Analyze Message'}</button>
          </form>}

          {tab === 'url' && <form className="analysis-form" onSubmit={handleUrlSubmit}>
            <div className="form-row"><label htmlFor="website-url">Website URL</label><input id="website-url" type="url" autoComplete="url" value={urlForm.url} onChange={(e) => setUrlForm({ url: e.target.value })} placeholder="https://example.com" required /><span className="field-hint">We inspect URL structure and known risk signals.</span></div>
            <div className="feature-strip"><span className="url-feature"><i><Link2 size={15} /></i>Length</span><span className="url-feature"><i><LockKeyhole size={15} /></i>HTTPS</span><span className="url-feature"><i><ScanSearch size={15} /></i>Subdomains</span><span className="url-feature"><i><ScanSearch size={15} /></i>Special Chars</span><span className="url-feature"><i><ShieldCheck size={15} /></i>Risk Keywords</span></div>
            <button className="primary-btn analysis-submit" disabled={loading}><ScanSearch size={16} /> {loading ? 'Analyzing URL...' : 'Analyze URL'}</button>
          </form>}

          {tab === 'qr' && <form className="analysis-form" onSubmit={handleQrSubmit}>
            <div className="form-row"><label htmlFor="qr-upload">QR code image</label><label className="upload-zone" htmlFor="qr-upload" onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.preventDefault(); const dropped = event.dataTransfer.files[0]; if (dropped?.type.startsWith('image/')) selectQrFile(dropped) }}><span className="upload-icon"><UploadCloud size={27} /></span><strong>{file ? file.name : 'Click to upload QR image'}</strong><span>or drag and drop</span><small>Supported formats: PNG, JPG, JPEG<br />Max file size: 5 MB</small><input id="qr-upload" type="file" accept="image/png,image/jpeg,image/webp" onChange={(event) => selectQrFile(event.target.files?.[0])} /></label></div>
            <div className="qr-or-divider"><span>OR</span></div>
            <input ref={cameraInputRef} className="camera-input" type="file" accept="image/*" capture="environment" aria-label="Capture QR code image" onChange={(event) => selectQrFile(event.target.files?.[0])} />
            <button className="primary-btn analysis-submit camera-button" type="button" disabled={loading} onClick={() => cameraInputRef.current?.click()}><Camera size={15} /> {loading ? 'Scanning QR code...' : 'Scan with Camera'}</button>
          </form>}

          {error && <div className="alert-box form-error" role="alert">{error}</div>}
          {result && <div className="result-card analysis-result"><div className="status-row"><div><div className="muted">Risk score</div><div className="result-score">{result.risk_score}<small>/100</small></div></div><span className={`badge ${(result.risk_level || '').toLowerCase().replace(/ /g, '-')}`}>{result.risk_level}</span></div><p><strong>Classification:</strong> {result.classification}</p><p><strong>Recommendation:</strong> {result.recommendation}</p><p><strong>Decision:</strong> {result.decision}</p><h3>Evidence</h3><ul className="evidence-list">{(result.evidence || []).map((item, index) => <li key={index}>{item}</li>)}</ul><p><strong>Explanation:</strong> {result.explanation}</p>{result.analysis_id && <Link className="secondary-btn" to={`/reports/${result.analysis_id}`}>View full report</Link>}</div>}
        </section>

        <aside className="analysis-aside">
          <section className={`card analysis-aside-card ${tab}-aside-card`}><div className={`analysis-illustration ${tab}-illustration`}><span><AsideIcon size={tab === 'qr' ? 54 : 46} strokeWidth={1.7} /></span>{tab === 'url' && <i className="illustration-search"><ScanSearch size={26} /></i>}{tab === 'text' && <i><CheckCircle2 size={17} /></i>}{tab === 'qr' && <i className="qr-frame-corners" />}</div><h3>{modeContent.title}</h3><p>{modeContent.description}</p></section>
          <section className="privacy-note"><span><ShieldCheck size={18} /></span><div><strong>Your data stays private</strong><p>Your analysis is saved to your account history.</p></div></section>
        </aside>
      </div>
    </AppLayout>
  )
}
