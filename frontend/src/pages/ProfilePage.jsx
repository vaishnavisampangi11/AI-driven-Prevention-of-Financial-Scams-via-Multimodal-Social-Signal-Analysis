import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Check, Eye, EyeOff, KeyRound, ShieldAlert, Trash2, UserRound, X } from 'lucide-react'
import { profileApi } from '../services/api'
import AppLayout from '../components/AppLayout'

export default function ProfilePage() {
  const navigate = useNavigate()
  const [profile, setProfile] = useState({ name: '', email: '', created_at: '' })
  const [name, setName] = useState('')
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [passwordOpen, setPasswordOpen] = useState(false)
  const [passwordForm, setPasswordForm] = useState({ current_password: '', new_password: '', confirm_password: '' })
  const [passwordMessage, setPasswordMessage] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [showPasswords, setShowPasswords] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [deletePassword, setDeletePassword] = useState('')
  const [deleteError, setDeleteError] = useState('')
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const load = async () => {
      const response = await profileApi.get()
      setProfile(response.data.data)
      setName(response.data.data.name)
    }
    load().catch(console.error)
  }, [])

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setMessage('')
    setError('')
    try {
      const response = await profileApi.update({ name })
      setProfile((current) => ({ ...current, ...response.data.data }))
      localStorage.setItem('user_name', response.data.data.name)
      setMessage('Your profile has been updated.')
    } catch (err) { setError(err.response?.data?.detail || 'Unable to update your profile.') } finally { setSaving(false) }
  }

  const submitPassword = async (event) => {
    event.preventDefault()
    setPasswordMessage('')
    setPasswordError('')
    if (passwordForm.new_password.length < 8) return setPasswordError('Use at least 8 characters for your new password.')
    if (passwordForm.new_password !== passwordForm.confirm_password) return setPasswordError('The new passwords do not match.')
    try {
      await profileApi.updatePassword({ current_password: passwordForm.current_password, new_password: passwordForm.new_password })
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' })
      setPasswordMessage('Password updated successfully.')
      setPasswordOpen(false)
    } catch (err) { setPasswordError(err.response?.data?.detail || 'Unable to update your password.') }
  }

  const submitDelete = async (event) => {
    event.preventDefault()
    setDeleting(true)
    setDeleteError('')
    try {
      await profileApi.deleteAccount(deletePassword)
      localStorage.removeItem('token')
      localStorage.removeItem('user_name')
      navigate('/login', { replace: true })
    } catch (err) { setDeleteError(err.response?.data?.detail || 'Unable to delete your account.') } finally { setDeleting(false) }
  }

  return (
    <AppLayout title="My profile">
      <div className="profile-page-grid">
        <section className="card panel profile-sheet">
          <div className="profile-identity"><span className="profile-avatar"><UserRound size={29} strokeWidth={1.7} /></span><div><h2>{profile.name || 'Your account'}</h2><p>{profile.email}</p><span>Member since {profile.created_at ? new Date(profile.created_at).toLocaleDateString() : '—'}</span></div></div>
          <section className="profile-section"><h3>Account Information</h3><dl className="profile-details"><div><dt>Full Name</dt><dd>{profile.name}</dd></div><div><dt>Email</dt><dd>{profile.email}</dd></div><div><dt>Role</dt><dd>{profile.role || 'User'}</dd></div></dl><form className="profile-inline-edit" onSubmit={submit}><label htmlFor="profile-name">Edit name</label><div><input id="profile-name" value={name} onChange={(event) => setName(event.target.value)} autoComplete="name" required /><button className="secondary-btn" type="submit" disabled={saving}>{saving ? 'Saving...' : <><Check size={14} /> Save</>}</button></div>{message && <p className="form-success" role="status">{message}</p>}{error && <p className="form-error" role="alert">{error}</p>}</form></section>
          <section className="profile-section password-section"><div className="profile-section-heading"><h3>Change Password</h3><button className="secondary-btn password-toggle" type="button" onClick={() => { setPasswordOpen((open) => !open); setPasswordError(''); setPasswordMessage('') }}><KeyRound size={14} /> {passwordOpen ? 'Cancel' : 'Update Password'}</button></div>{passwordMessage && <p className="form-success" role="status">{passwordMessage}</p>}{passwordOpen && <form className="password-update-form" onSubmit={submitPassword}><div className="form-row"><label htmlFor="current-password">Current password</label><input id="current-password" type={showPasswords ? 'text' : 'password'} autoComplete="current-password" value={passwordForm.current_password} onChange={(event) => setPasswordForm({ ...passwordForm, current_password: event.target.value })} required /></div><div className="form-row"><label htmlFor="new-password">New password</label><input id="new-password" type={showPasswords ? 'text' : 'password'} autoComplete="new-password" value={passwordForm.new_password} onChange={(event) => setPasswordForm({ ...passwordForm, new_password: event.target.value })} required minLength={8} /></div><div className="form-row"><label htmlFor="confirm-password">Confirm new password</label><input id="confirm-password" type={showPasswords ? 'text' : 'password'} autoComplete="new-password" value={passwordForm.confirm_password} onChange={(event) => setPasswordForm({ ...passwordForm, confirm_password: event.target.value })} required /></div><label className="show-password-toggle"><input type="checkbox" checked={showPasswords} onChange={(event) => setShowPasswords(event.target.checked)} /> Show passwords <Eye size={13} /></label>{passwordError && <p className="form-error" role="alert">{passwordError}</p>}<button className="primary-btn" type="submit">Update password</button></form>}</section>
          <div className="profile-delete-row"><span><strong>Delete Account</strong><small>Remove your account and saved analysis history.</small></span><button className="delete-account-btn" type="button" onClick={() => { setDeleteOpen(true); setDeleteError('') }}><Trash2 size={15} /> Delete Account</button></div>
        </section>
      </div>
      {deleteOpen && <div className="account-modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget && !deleting) setDeleteOpen(false) }}><section className="account-delete-modal" role="dialog" aria-modal="true" aria-labelledby="delete-account-title"><button className="modal-close" type="button" aria-label="Close dialog" onClick={() => setDeleteOpen(false)}><X size={17} /></button><span className="delete-warning-icon"><ShieldAlert size={22} /></span><h2 id="delete-account-title">Delete your account?</h2><p>This permanently removes your profile, alerts, and analysis history. Enter your password to confirm.</p><form onSubmit={submitDelete}><div className="form-row"><label htmlFor="delete-password">Password</label><input id="delete-password" type="password" autoComplete="current-password" value={deletePassword} onChange={(event) => setDeletePassword(event.target.value)} required /></div>{deleteError && <p className="form-error" role="alert">{deleteError}</p>}<div className="modal-actions"><button className="secondary-btn" type="button" disabled={deleting} onClick={() => setDeleteOpen(false)}>Cancel</button><button className="delete-account-btn" type="submit" disabled={deleting}>{deleting ? 'Deleting...' : <><Trash2 size={14} /> Delete account</>}</button></div></form></section></div>}
    </AppLayout>
  )
}
