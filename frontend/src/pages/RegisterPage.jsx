import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { CheckCircle2, Eye, EyeOff, LockKeyhole, ShieldCheck } from 'lucide-react'
import { authApi } from '../services/api'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '', confirmPassword: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.')
      return
    }
    setLoading(true)
    setError('')
    try {
      await authApi.register({ name: form.name, email: form.email, password: form.password })
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-layout">
        <section className="auth-story register-story">
          <Link className="auth-brand" to="/login"><span className="shield-mark"><ShieldCheck size={20} /></span><span>SafeScan</span></Link>
          <div className="auth-art" aria-hidden="true"><div className="art-shield"><span><LockKeyhole size={52} strokeWidth={1.8} /></span></div><i className="art-orbit orbit-one" /><i className="art-orbit orbit-two" /><i className="art-spark spark-one" /><i className="art-spark spark-two" /></div>
          <div className="auth-story-copy"><h2>Join SafeScan</h2><p>Create your account and start protecting yourself from financial scams.</p><div className="auth-features"><span><CheckCircle2 size={15} /> Real-time AI analysis</span><span><CheckCircle2 size={15} /> Detailed explanations</span><span><CheckCircle2 size={15} /> Personalized alerts</span><span><CheckCircle2 size={15} /> Secure and private</span></div></div>
        </section>
        <section className="auth-form-panel">
          <div className="auth-form-inner register-form-inner">
            <div className="auth-mobile-brand"><span className="shield-mark"><ShieldCheck size={20} /></span> SafeScan</div>
            <div className="auth-form-brand"><span className="shield-mark"><ShieldCheck size={20} /></span><div><strong>SafeScan</strong><small>Detect · Analyze · Stay Safe</small></div></div>
            <h1>Create account</h1>
            <p className="auth-subtitle">Get started in a few steps</p>
            <form onSubmit={handleSubmit}>
              <div className="form-row"><label htmlFor="name">Full name</label><input id="name" name="name" autoComplete="name" value={form.name} onChange={handleChange} placeholder="Enter your full name" required /></div>
              <div className="form-row"><label htmlFor="email">Email address</label><input id="email" type="email" name="email" autoComplete="email" value={form.email} onChange={handleChange} placeholder="Enter your email" required /></div>
              <div className="form-row"><label htmlFor="password">Password</label><div className="password-field"><input id="password" type={showPassword ? 'text' : 'password'} name="password" autoComplete="new-password" value={form.password} onChange={handleChange} placeholder="Create a strong password" required /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword(!showPassword)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div></div>
              <div className="form-row"><label htmlFor="confirmPassword">Confirm password</label><input id="confirmPassword" type={showPassword ? 'text' : 'password'} name="confirmPassword" autoComplete="new-password" value={form.confirmPassword} onChange={handleChange} placeholder="Confirm your password" required /></div>
              {error && <div className="alert-box auth-error">{error}</div>}
              <label className="remember-check terms-check"><input type="checkbox" required /> I agree to the Terms &amp; Conditions</label>
              <button className="primary-btn auth-submit" type="submit" disabled={loading}>{loading ? 'Creating account...' : 'Create account'}</button>
            </form>
            <p className="auth-switch">Already have an account? <Link to="/login">Log in</Link></p>
          </div>
        </section>
      </div>
    </div>
  )
}
