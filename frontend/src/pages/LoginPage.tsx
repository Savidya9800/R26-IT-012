// frontend/src/pages/LoginPage.tsx

import { useState } from "react"
import { Eye, EyeOff, Lock, Mail } from "lucide-react"
import { login } from "../services/authApi"
import { useAuth } from '../contexts/AuthContext'

type UserRole = "Clinician" | "Student" | "Admin"

export default function LoginPage() {
  const [selectedRole, setSelectedRole] = useState<UserRole>("Student")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [rememberMe, setRememberMe] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const roles: UserRole[] = ["Clinician", "Student", "Admin"]

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      await login(email, password)
      // Redirect to dashboard (you'll need to set up routing)
      window.location.href = '/dashboard'
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen bg-linear-to-br from-blue-50 via-cyan-50 to-blue-100">
      <section className="relative flex-col justify-between hidden p-12 overflow-hidden text-white bg-linear-to-br from-blue-900 via-blue-800 to-cyan-900 lg:flex lg:w-1/2">
        <div className="absolute bottom-0 right-0 rounded-full h-96 w-96 bg-cyan-400 opacity-10 blur-3xl" />

        <div className="relative z-10">
          <div className="inline-block mb-8">
            <span className="px-4 py-2 text-sm font-semibold border rounded-lg border-cyan-300 text-cyan-300">
              CLINICAL STANDARD V2.4
            </span>
          </div>

          <h1 className="mb-4 text-5xl font-bold leading-tight">
            Intelligence that empowers{" "}
            <span className="text-cyan-300">Precision Care.</span>
          </h1>

          <p className="max-w-md text-lg leading-relaxed text-blue-100">
            The Cardio Gastro AI transforms high-stakes medical data into
            clinical insights for modern practitioners.
          </p>
        </div>

        <div className="relative z-10 flex gap-12">
          <div>
            <div className="text-4xl font-bold text-cyan-300">99.8%</div>
            <div className="mt-2 text-sm tracking-wide text-blue-200 uppercase">
              Accuracy Rating
            </div>
          </div>

          <div>
            <div className="text-4xl font-bold text-cyan-300">1.2ms</div>
            <div className="mt-2 text-sm tracking-wide text-blue-200 uppercase">
              Response Latency
            </div>
          </div>
        </div>
      </section>

      <section className="flex flex-col justify-between w-full p-8 sm:p-12 lg:w-1/2">
        <form onSubmit={handleLogin} className="w-full max-w-md mx-auto">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900">
              Cardio Gastro AI
            </h2>
            <p className="mt-1 text-gray-500">Secure Access Portal</p>
          </div>

          <div className="mb-8">
            <label className="block mb-4 text-xs font-semibold tracking-wider text-gray-700 uppercase">
              Identity Profile
            </label>

            <div className="grid grid-cols-3 gap-3">
              {roles.map((role) => (
                <button
                  key={role}
                  type="button"
                  onClick={() => setSelectedRole(role)}
                  className={`rounded-lg px-4 py-3 text-sm font-medium transition-all ${
                    selectedRole === role
                      ? "bg-blue-600 text-white shadow-lg"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-5">
            <label className="block mb-2 text-xs font-semibold tracking-wider text-gray-700 uppercase">
              Institutional Email
            </label>

            <div className="relative">
              <Mail className="absolute left-4 top-3.5 text-gray-400" size={18} />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@university.edu"
                className="w-full py-3 pl-12 pr-4 transition border border-gray-300 rounded-lg focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          <div className="mb-5">
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-semibold tracking-wider text-gray-700 uppercase">
                Password
              </label>

              <a
                href="#recover"
                className="text-sm font-medium text-blue-600 hover:text-blue-700"
              >
                Recover Keys
              </a>
            </div>

            <div className="relative">
              <Lock className="absolute left-4 top-3.5 text-gray-400" size={18} />

              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full py-3 pl-12 pr-12 transition border border-gray-300 rounded-lg focus:border-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />

              <button
                type="button"
                onClick={() => setShowPassword((value) => !value)}
                className="absolute right-4 top-3.5 text-gray-400 hover:text-gray-600"
                aria-label="Toggle password visibility"
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          {error && (
            <div className="p-3 mb-4 text-sm text-red-700 border border-red-200 rounded-lg bg-red-50">
              {error}
            </div>
          )}

          <div className="flex items-center mb-6">
            <input
              type="checkbox"
              id="remember"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded cursor-pointer focus:ring-blue-500"
            />

            <label
              htmlFor="remember"
              className="ml-3 text-sm text-gray-700 cursor-pointer"
            >
              Remember this workstation for 24 hours
            </label>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center justify-center w-full gap-2 px-4 py-3 font-semibold text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-blue-400"
          >
            {isLoading ? (
              <>
                <span className="w-5 h-5 border-2 border-white rounded-full animate-spin border-t-transparent" />
                Initializing...
              </>
            ) : (
              <>
                Initialize Session
                <span>→</span>
              </>
            )}
          </button>

          <div className="flex items-center justify-center gap-2 mt-4 text-xs text-gray-600">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            Protected by Multi-Factor Authentication
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              New to the platform?{" "}
              <a
                href="#request"
                className="font-semibold text-blue-600 hover:text-blue-700"
              >
                Request institutional access.
              </a>
            </p>
          </div>
        </form>

        <footer className="w-full pt-6 mt-8 border-t border-gray-200">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex gap-6 text-xs text-gray-600">
              <a
                href="#status"
                className="font-medium tracking-wider uppercase hover:text-gray-900"
              >
                System Status
              </a>
              <a
                href="#privacy"
                className="font-medium tracking-wider uppercase hover:text-gray-900"
              >
                Privacy Protocol
              </a>
              <a
                href="#support"
                className="font-medium tracking-wider uppercase hover:text-gray-900"
              >
                Support
              </a>
            </div>

            <div className="flex items-center gap-2 text-xs text-green-700">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="font-semibold">AES-256 ACTIVE</span>
            </div>
          </div>
        </footer>
      </section>
    </main>
  )
}