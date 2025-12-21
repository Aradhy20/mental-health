'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import FloatingCard from '@/components/anti-gravity/FloatingCard'
import { User, Lock, ArrowRight, Loader2 } from 'lucide-react'
import { useAuthStore } from '@/lib/store/auth-store'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function LoginPage() {
  const router = useRouter()
  const login = useAuthStore((state) => state.login)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    // Prefetch dashboard in advance to speed up redirect
    router.prefetch('/')

    try {
      const response = await fetch('http://127.0.0.1:8001/v1/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: formData.username,
          password: formData.password,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Login failed')
      }

      const data = await response.json()

      // Fetch User Details immediately
      const userResponse = await fetch('http://127.0.0.1:8001/v1/users/me', {
        headers: { Authorization: `Bearer ${data.access_token}` }
      })

      if (userResponse.ok) {
        const userData = await userResponse.json()
        login({
          user_id: userData.user_id.toString(),
          username: userData.username,
          email: userData.email,
          full_name: userData.full_name
        }, data.access_token)
      } else {
        login({ user_id: '1', username: formData.username, email: '' }, data.access_token)
      }

      // Instant redirect
      router.replace('/')
    } catch (err: any) {
      setError(err.message)
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <FloatingCard className="w-full max-w-md bg-white/80 dark:bg-black/40 backdrop-blur-xl border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-display font-bold bg-clip-text text-transparent bg-gradient-to-r from-serenity-600 to-serenity-400 dark:from-aurora-300 dark:to-aurora-500">
            Welcome Back
          </h1>
          <p className="text-muted-foreground mt-2">Continue your journey to mindfulness.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="p-3 rounded-xl bg-destructive/10 text-destructive text-sm text-center">
              {error}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
              <Input
                id="username"
                type="text"
                placeholder="Enter your username"
                required
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="pl-10"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="pl-10"
              />
            </div>
          </div>

          <Button
            type="submit"
            disabled={isLoading}
            className="w-full"
            size="lg"
          >
            {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
            Sign In
            {!isLoading && <ArrowRight className="ml-2 h-4 w-4" />}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link href="/register" className="text-primary font-medium hover:underline">
            Create Account
          </Link>
        </div>
      </FloatingCard>
    </div>
  )
}