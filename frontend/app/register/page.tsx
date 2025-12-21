'use client'

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import FloatingCard from '@/components/anti-gravity/FloatingCard'
import { User, Mail, Lock, ArrowRight, Loader2 } from 'lucide-react'
import { useAuthStore } from '@/lib/store/auth-store'

export default function RegisterPage() {
    const router = useRouter()
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState('')
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        full_name: ''
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)
        setError('')

        // Prefetch login to speed up the next step
        router.prefetch('/login')

        try {
            const response = await fetch('http://127.0.0.1:8001/v1/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            })

            if (!response.ok) {
                const data = await response.json()
                throw new Error(data.detail || 'Registration failed')
            }

            // Success redirect
            router.replace('/login')
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
                        Join MindfulAI
                    </h1>
                    <p className="text-muted-foreground mt-2">Begin your wellness journey today.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {error && (
                        <div className="p-3 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 text-sm text-center">
                            {error}
                        </div>
                    )}

                    <div className="space-y-2">
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
                            <input
                                type="text"
                                placeholder="Username"
                                required
                                value={formData.username}
                                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                className="w-full pl-10 pr-4 py-3 bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 rounded-xl focus:ring-2 focus:ring-serenity-400 outline-none transition-all"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
                            <input
                                type="text"
                                placeholder="Full Name"
                                value={formData.full_name}
                                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                className="w-full pl-10 pr-4 py-3 bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 rounded-xl focus:ring-2 focus:ring-serenity-400 outline-none transition-all"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
                            <input
                                type="email"
                                placeholder="Email Address"
                                required
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                className="w-full pl-10 pr-4 py-3 bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 rounded-xl focus:ring-2 focus:ring-serenity-400 outline-none transition-all"
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
                            <input
                                type="password"
                                placeholder="Password"
                                required
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                className="w-full pl-10 pr-4 py-3 bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 rounded-xl focus:ring-2 focus:ring-serenity-400 outline-none transition-all"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full py-3 bg-serenity-500 dark:bg-aurora-500 text-white rounded-xl font-medium shadow-lg hover:opacity-90 active:scale-95 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : 'Create Account'}
                        {!isLoading && <ArrowRight size={20} />}
                    </button>
                </form>

                <div className="mt-6 text-center text-sm text-muted-foreground">
                    Already have an account?{' '}
                    <Link href="/login" className="text-serenity-600 dark:text-aurora-400 font-medium hover:underline">
                        Sign in
                    </Link>
                </div>
            </FloatingCard>
        </div>
    )
}
