'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Activity, Plus, Smile, Book, Wind } from 'lucide-react'
import DashboardCard from '@/components/ui/DashboardCard'
import MoodTracker from '@/components/features/MoodTracker'
import RecommendationCarousel from '@/components/features/RecommendationCarousel'
import EmotionHeatmap from '@/components/features/EmotionHeatmap'
import FloatingActionButton from '@/components/ui/FloatingActionButton'
import { useAuthStore } from '@/lib/store/auth-store'

const DashboardPage = () => {
  const { user } = useAuthStore()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null;
  const wellnessScore = 78
  const streakDays = 12
  const entriesThisWeek = 24

  const fabActions = [
    {
      id: 'mood',
      label: 'Log Mood',
      icon: <Smile size={18} />,
      onClick: () => console.log('Log mood clicked')
    },
    {
      id: 'journal',
      label: 'Write Journal',
      icon: <Book size={18} />,
      onClick: () => console.log('Write journal clicked')
    },
    {
      id: 'breathing',
      label: 'Breathing Exercise',
      icon: <Wind size={18} />,
      onClick: () => console.log('Breathing exercise clicked')
    }
  ]

  return (
    <div className="space-y-10 pb-20">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        className="p-8 rounded-[2.5rem] bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-transparent border border-white/5 relative overflow-hidden"
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between relative z-10 gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[10px] font-bold tracking-widest uppercase mb-3">
              <Activity size={12} className="animate-pulse" />
              System Pulse: Optimal
            </div>
            <h1 className="text-4xl font-display font-bold text-white tracking-tight">
              Greetings, {user?.full_name || 'Seeker'}
            </h1>
            <p className="text-slate-400 mt-2 font-medium">Your neural synchronization is at 94% efficiency today.</p>
          </div>
          <div>
            <button className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold tracking-widest uppercase text-sm transition-all shadow-xl shadow-indigo-600/20 flex items-center gap-2">
              <Plus size={18} />
              INITIATE SCAN
            </button>
          </div>
        </div>
        <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl" />
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <DashboardCard
          title="Wellness Score"
          value={`${wellnessScore}%`}
          description="Overall mental health"
          icon={<Activity size={24} />}
          trend={{ value: 5, isPositive: true }}
        />

        <DashboardCard
          title="Current Streak"
          value={`${streakDays} days`}
          description="Consecutive check-ins"
          icon={<Activity size={24} />}
          trend={{ value: 2, isPositive: true }}
        />

        <DashboardCard
          title="This Week"
          value={entriesThisWeek}
          description="Entries logged"
          icon={<Activity size={24} />}
        />

        <DashboardCard
          title="Current Mood"
          value="Balanced"
          description="Based on recent entries"
          icon={<Smile size={24} />}
        />
      </motion.div>

      {/* Mood Tracker and Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <MoodTracker />
        <RecommendationCarousel />
      </div>

      {/* Emotion Heatmap */}
      <EmotionHeatmap />

      {/* Floating Action Button */}
      <FloatingActionButton
        actions={fabActions}
        mainIcon={<Plus size={24} />}
        mainLabel="Quick Actions"
      />
    </div>
  )
}

export default DashboardPage