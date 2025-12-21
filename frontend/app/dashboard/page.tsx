'use client'

import React from 'react'
import { motion } from 'framer-motion'
import DashboardCard from '@/components/ui/DashboardCard'
import MoodTracker from '@/components/features/MoodTracker'
import RecommendationCarousel from '@/components/features/RecommendationCarousel'
import EmotionHeatmap from '@/components/features/EmotionHeatmap'
import FloatingActionButton from '@/components/ui/FloatingActionButton'

const DashboardPage = () => {
  // Mock data for dashboard cards
  const wellnessScore = 78
  const streakDays = 12
  const entriesThisWeek = 24

  // Floating action button actions
  const fabActions = [
    {
      id: 'mood',
      label: 'Log Mood',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      onClick: () => console.log('Log mood clicked')
    },
    {
      id: 'journal',
      label: 'Write Journal',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
      onClick: () => console.log('Write journal clicked')
    },
    {
      id: 'breathing',
      label: 'Breathing Exercise',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
      onClick: () => console.log('Breathing exercise clicked')
    }
  ]

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card rounded-3xl p-6"
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Good morning, Sarah!</h1>
            <p className="text-gray-600 mt-1">Here's your mental wellness overview for today</p>
          </div>
          <div className="mt-4 md:mt-0">
            <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-medium hover:shadow-lg transition-all">
              Log Mood Entry
            </button>
          </div>
        </div>
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
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
          trend={{ value: 5, isPositive: true }}
        />

        <DashboardCard
          title="Current Streak"
          value={`${streakDays} days`}
          description="Consecutive check-ins"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
          trend={{ value: 2, isPositive: true }}
        />

        <DashboardCard
          title="This Week"
          value={entriesThisWeek}
          description="Entries logged"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          }
        />

        <DashboardCard
          title="Current Mood"
          value="Balanced"
          description="Based on recent entries"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
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
        mainIcon={
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        }
        mainLabel="Quick Actions"
      />
    </div>
  )
}

export default DashboardPage