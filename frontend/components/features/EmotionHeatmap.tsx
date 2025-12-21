'use client'

import React from 'react'
import { motion } from 'framer-motion'

interface HeatmapData {
  date: string
  emotion: string
  intensity: number
}

interface EmotionColorMap {
  [key: string]: string
}

const EmotionHeatmap = () => {
  // Mock data for the heatmap
  const heatmapData: HeatmapData[] = [
    { date: '2023-05-01', emotion: 'happy', intensity: 8 },
    { date: '2023-05-02', emotion: 'calm', intensity: 6 },
    { date: '2023-05-03', emotion: 'anxious', intensity: 4 },
    { date: '2023-05-04', emotion: 'sad', intensity: 3 },
    { date: '2023-05-05', emotion: 'excited', intensity: 9 },
    { date: '2023-05-06', emotion: 'angry', intensity: 2 },
    { date: '2023-05-07', emotion: 'peaceful', intensity: 7 },
    { date: '2023-05-08', emotion: 'stressed', intensity: 5 },
    { date: '2023-05-09', emotion: 'content', intensity: 7 },
    { date: '2023-05-10', emotion: 'frustrated', intensity: 3 },
    { date: '2023-05-11', emotion: 'hopeful', intensity: 8 },
    { date: '2023-05-12', emotion: 'overwhelmed', intensity: 4 },
    { date: '2023-05-13', emotion: 'grateful', intensity: 9 },
    { date: '2023-05-14', emotion: 'lonely', intensity: 3 },
    { date: '2023-05-15', emotion: 'motivated', intensity: 8 },
    { date: '2023-05-16', emotion: 'exhausted', intensity: 2 },
    { date: '2023-05-17', emotion: 'optimistic', intensity: 7 },
    { date: '2023-05-18', emotion: 'worried', intensity: 4 },
    { date: '2023-05-19', emotion: 'accomplished', intensity: 8 },
    { date: '2023-05-20', emotion: 'disappointed', intensity: 3 },
    { date: '2023-05-21', emotion: 'relieved', intensity: 7 },
  ]

  const emotionColors: EmotionColorMap = {
    happy: 'bg-green-500',
    calm: 'bg-blue-400',
    anxious: 'bg-yellow-500',
    sad: 'bg-blue-700',
    excited: 'bg-yellow-400',
    angry: 'bg-red-600',
    peaceful: 'bg-indigo-400',
    stressed: 'bg-orange-500',
    content: 'bg-green-400',
    frustrated: 'bg-red-500',
    hopeful: 'bg-green-300',
    overwhelmed: 'bg-purple-600',
    grateful: 'bg-green-600',
    lonely: 'bg-gray-600',
    motivated: 'bg-green-500',
    exhausted: 'bg-gray-800',
    optimistic: 'bg-green-400',
    worried: 'bg-yellow-600',
    accomplished: 'bg-green-700',
    disappointed: 'bg-blue-800',
    relieved: 'bg-green-300',
  }

  const getIntensityColor = (intensity: number) => {
    if (intensity >= 8) return 'bg-opacity-100'
    if (intensity >= 6) return 'bg-opacity-80'
    if (intensity >= 4) return 'bg-opacity-60'
    if (intensity >= 2) return 'bg-opacity-40'
    return 'bg-opacity-20'
  }

  // Group data by week for display
  const groupedData = heatmapData.reduce((acc: {[key: string]: HeatmapData[]}, item) => {
    const week = item.date.substring(0, 7) // Year-Month
    if (!acc[week]) {
      acc[week] = []
    }
    acc[week].push(item)
    return acc
  }, {})

  return (
    <div className="glass-card rounded-3xl p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Emotion Heatmap</h2>
        <div className="text-sm text-gray-500">Last 30 days</div>
      </div>

      <div className="overflow-x-auto">
        <div className="min-w-full">
          {Object.entries(groupedData).map(([week, weekData]) => (
            <div key={week} className="mb-8 last:mb-0">
              <h3 className="text-lg font-medium text-gray-800 mb-4">{week}</h3>
              <div className="grid grid-cols-7 gap-2">
                {weekData.map((day, index) => (
                  <motion.div
                    key={index}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="relative group"
                  >
                    <div
                      className={`w-10 h-10 rounded-lg ${emotionColors[day.emotion] || 'bg-gray-300'} ${getIntensityColor(day.intensity)} flex items-center justify-center cursor-pointer transition-all duration-200`}
                    >
                      <span className="text-xs font-medium text-white">
                        {day.date.split('-')[2]}
                      </span>
                    </div>
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                      <div className="font-medium capitalize">{day.emotion}</div>
                      <div className="text-gray-300">Intensity: {day.intensity}/10</div>
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="font-medium text-gray-900 mb-3">Emotion Legend</h3>
        <div className="flex flex-wrap gap-2">
          {Object.entries(emotionColors).slice(0, 8).map(([emotion, color]) => (
            <div key={emotion} className="flex items-center">
              <div className={`w-4 h-4 rounded ${color} bg-opacity-80 mr-2`}></div>
              <span className="text-sm text-gray-700 capitalize">{emotion}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-xl">
        <h4 className="font-medium text-blue-900 mb-2">Insight</h4>
        <p className="text-sm text-blue-800">
          You tend to feel more positive emotions on weekends. Consider scheduling 
          challenging tasks for weekdays when you typically feel more energized.
        </p>
      </div>
    </div>
  )
}

export default EmotionHeatmap