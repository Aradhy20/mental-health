'use client'

import React, { useState, useEffect, memo } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, Sparkles, Brain, Heart, Zap, TrendingUp, Activity } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/auth-store'
import { fadeIn, scaleIn, staggerContainer, staggerItem } from '@/lib/animations/presets'
import SpecialistGrid from '@/components/anti-gravity/SpecialistGrid'

// Optimized components
const FloatingCard = memo(({ children, className = '', delay = 0 }: any) => (
  <motion.div
    {...fadeIn}
    transition={{ ...fadeIn.transition, delay }}
    className={`glass-panel rounded-3xl p-6 gpu-accelerated ${className}`}
  >
    {children}
  </motion.div>
))
FloatingCard.displayName = 'FloatingCard'

const StatCard = memo(({ icon: Icon, label, value, color }: any) => (
  <FloatingCard className="flex items-center gap-4 hover:scale-105 transition-fast cursor-pointer">
    <div className={`p-3 rounded-2xl ${color}`}>
      <Icon size={24} />
    </div>
    <div>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-xs text-muted-foreground">{label}</p>
    </div>
  </FloatingCard>
))
StatCard.displayName = 'StatCard'

export default function OptimizedDashboard() {
  const user = useAuthStore((state) => state.user)
  const router = useRouter()
  const [greeting, setGreeting] = useState('Hey')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const hour = new Date().getHours()
    if (hour < 12) setGreeting('Good Morning')
    else if (hour < 18) setGreeting('Good Afternoon')
    else setGreeting('Good Evening')

    // Prefetch common routes for "Instant" feel
    router.prefetch('/chat')
    router.prefetch('/insights')
    router.prefetch('/mood')
    router.prefetch('/journal')
  }, [router])

  if (!mounted) return <div className="min-h-screen animate-pulse bg-black/5 rounded-[2.5rem]" />

  return (
    <div className="space-y-8 pb-12">
      {/* Hero Section */}
      <motion.div
        {...fadeIn}
        className="relative overflow-hidden rounded-[2.5rem] p-8 md:p-12 text-white min-h-[400px] flex items-center"
      >
        <div
          className="absolute inset-0 z-0 bg-cover bg-center transition-transform duration-1000 hover:scale-105"
          style={{ backgroundImage: "url('/images/hero.png')" }}
        />
        <div className="absolute inset-0 z-0 bg-gradient-to-br from-purple-500/80 via-pink-500/60 to-orange-500/40" />

        <div className="relative z-10 w-full">
          <motion.h1
            {...scaleIn}
            className="text-4xl md:text-6xl font-black mb-4 drop-shadow-lg"
          >
            {greeting}, {user?.full_name?.split(' ')[0] || 'Friend'}! 👋
          </motion.h1>
          <p className="text-lg md:text-xl opacity-90 mb-6 font-medium drop-shadow-md">
            Your mental wellness journey starts here. Let's make today mindful.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link href="/chat">
              <button className="px-8 py-4 bg-white text-purple-600 rounded-2xl font-bold hover:scale-105 transition-fast shadow-xl flex items-center gap-3">
                <Brain size={22} />
                Talk to AI
              </button>
            </Link>
            <Link href="/mood">
              <button className="px-8 py-4 bg-white/20 backdrop-blur-md rounded-2xl font-bold hover:scale-105 transition-fast border border-white/40 flex items-center gap-3 shadow-xl">
                <Heart size={22} />
                Log Mood
              </button>
            </Link>
          </div>
        </div>
      </motion.div>

      {/* Quick Stats */}
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="show"
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <motion.div variants={staggerItem}>
          <StatCard
            icon={Sparkles}
            label="Day Streak"
            value="12"
            color="bg-amber-500/10 text-amber-600"
          />
        </motion.div>
        <motion.div variants={staggerItem}>
          <StatCard
            icon={TrendingUp}
            label="Wellness"
            value="85%"
            color="bg-green-500/10 text-green-600"
          />
        </motion.div>
        <motion.div variants={staggerItem}>
          <StatCard
            icon={Activity}
            label="Mood Logs"
            value="128"
            color="bg-blue-500/10 text-blue-600"
          />
        </motion.div>
        <motion.div variants={staggerItem}>
          <StatCard
            icon={Zap}
            label="Energy"
            value="High"
            color="bg-purple-500/10 text-purple-600"
          />
        </motion.div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* AI Chat Card */}
        <Link href="/chat">
          <FloatingCard
            className="group cursor-pointer hover:scale-[1.02] transition-fast border-blue-500/20 relative overflow-hidden min-h-[220px]"
          >
            <div
              className="absolute inset-0 z-0 bg-cover bg-center opacity-20 group-hover:opacity-30 transition-opacity"
              style={{ backgroundImage: "url('/images/ai-companion.png')" }}
            />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-blue-500 rounded-2xl shadow-lg shadow-blue-500/20 text-white">
                  <Brain size={28} />
                </div>
                <ArrowRight className="text-blue-500 group-hover:translate-x-2 transition-fast" />
              </div>
              <h3 className="text-2xl font-bold mb-2">AI Companion</h3>
              <p className="text-muted-foreground">
                Chat with your personal mental health assistant powered by advanced AI
              </p>
            </div>
          </FloatingCard>
        </Link>

        {/* Insights Card */}
        <Link href="/insights">
          <FloatingCard className="group cursor-pointer hover:scale-[1.02] transition-fast bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/20 min-h-[220px]">
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-green-500 rounded-2xl shadow-lg shadow-green-500/20 text-white">
                <TrendingUp size={28} />
              </div>
              <ArrowRight className="text-green-500 group-hover:translate-x-2 transition-fast" />
            </div>
            <h3 className="text-2xl font-bold mb-2">Your Insights</h3>
            <p className="text-muted-foreground">
              Discover patterns and trends in your emotional wellbeing
            </p>
          </FloatingCard>
        </Link>

        {/* Journal Card */}
        <Link href="/journal">
          <FloatingCard className="group cursor-pointer hover:scale-[1.02] transition-fast bg-gradient-to-br from-pink-500/10 to-rose-500/10 border-pink-500/20 min-h-[220px]">
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-pink-500 rounded-2xl shadow-lg shadow-pink-500/20 text-white">
                <Heart size={28} />
              </div>
              <ArrowRight className="text-pink-500 group-hover:translate-x-2 transition-fast" />
            </div>
            <h3 className="text-2xl font-bold mb-2">Daily Journal</h3>
            <p className="text-muted-foreground">
              Express your thoughts and feelings in a safe space
            </p>
          </FloatingCard>
        </Link>

        {/* Meditation Card */}
        <Link href="/meditation">
          <FloatingCard
            className="group cursor-pointer hover:scale-[1.02] transition-fast border-purple-500/20 relative overflow-hidden min-h-[220px]"
          >
            <div
              className="absolute inset-0 z-0 bg-cover bg-center opacity-20 group-hover:opacity-30 transition-opacity"
              style={{ backgroundImage: "url('/images/meditation.png')" }}
            />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-purple-500 rounded-2xl shadow-lg shadow-purple-500/20 text-white">
                  <Zap size={28} />
                </div>
                <ArrowRight className="text-purple-500 group-hover:translate-x-2 transition-fast" />
              </div>
              <h3 className="text-2xl font-bold mb-2">Meditation</h3>
              <p className="text-muted-foreground">
                Guided breathing exercises to calm your mind
              </p>
            </div>
          </FloatingCard>
        </Link>
      </div>

      {/* Specialists Section - Professional & Trustworthy */}
      <motion.div variants={staggerItem}>
        <SpecialistGrid />
      </motion.div>

      {/* Quick Tip */}
      <motion.div variants={staggerItem}>
        <FloatingCard className="bg-gradient-to-r from-amber-500/10 to-orange-500/10 border-amber-500/20">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-amber-500 rounded-full">
              <Sparkles size={24} className="text-white" />
            </div>
            <div>
              <h4 className="font-bold text-lg">Daily Tip</h4>
              <p className="text-muted-foreground">
                Taking just 5 minutes to breathe deeply can reduce stress by 40%
              </p>
            </div>
          </div>
        </FloatingCard>
      </motion.div>
    </div>
  )
}