import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { CheckCircle2, CircleDot, Eye, EyeOff, LockKeyhole, ShieldCheck } from 'lucide-react'
import { authApi } from '../services/api'

export default function LoginPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const response = await authApi.login(form)
      localStorage.setItem('token', response.data.data.token)
      localStorage.setItem('user_name', response.data.data.user.name)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-layout">
        <section className="auth-story">
          <Link className="auth-brand" to="/login"><span className="shield-mark"><ShieldCheck size={20} /></span><span>SafeScan</span></Link>
          <div className="auth-art" aria-hidden="true"><div className="art-shield"><span><LockKeyhole size={52} strokeWidth={1.8} /></span></div><i className="art-orbit orbit-one" /><i className="art-orbit orbit-two" /><i className="art-spark spark-one" /><i className="art-spark spark-two" /></div>
          <div className="auth-story-copy"><h2>Stop scams<br />before they happen.</h2><p>AI-powered detection for a safer digital tomorrow.</p><div className="auth-features"><span><CircleDot size={15} /> Detect suspicious messages</span><span><CircleDot size={15} /> Check malicious URLs</span><span><CircleDot size={15} /> Scan QR codes</span><span><CircleDot size={15} /> Get risk analysis and alerts</span></div></div>
        </section>
        <section className="auth-form-panel">
          <div className="auth-form-inner">
            <div className="auth-mobile-brand"><span className="shield-mark"><ShieldCheck size={20} /></span> SafeScan</div>
            <div className="auth-form-brand"><span className="shield-mark"><ShieldCheck size={20} /></span><div><strong>SafeScan</strong><small>Detect · Analyze · Stay Safe</small></div></div>
            <h1>Welcome back</h1>
            <p className="auth-subtitle">Log in to your account</p>
            <form onSubmit={handleSubmit}>
              <div className="form-row"><label htmlFor="email">Email address</label><input id="email" type="email" name="email" autoComplete="email" value={form.email} onChange={handleChange} placeholder="Enter your email" required /></div>
              <div className="form-row"><label htmlFor="password">Password</label><div className="password-field"><input id="password" type={showPassword ? 'text' : 'password'} name="password" autoComplete="current-password" value={form.password} onChange={handleChange} placeholder="Enter your password" required /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword(!showPassword)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div></div>
              {error && <div className="alert-box auth-error">{error}</div>}
              <div className="auth-options"><label className="remember-check"><input type="checkbox" /> Remember me</label><Link to="/register">Need an account?</Link></div>
              <button className="primary-btn auth-submit" type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Log in'}</button>
            </form>
            <p className="auth-switch">New to SafeScan? <Link to="/register">Create an account</Link></p>
          </div>
        </section>
      </div>
    </div>
  )
}
