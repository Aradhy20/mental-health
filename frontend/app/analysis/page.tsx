'use client'

import React from 'react'
import { motion } from 'framer-motion'
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis,
  Tooltip as ReTooltip, LabelList
} from 'recharts'
import { BrainCircuit, ShieldCheck, Microscope, Zap, Database } from 'lucide-react'
import FloatingCard from '@/components/anti-gravity/FloatingCard'

const cognitiveData = [
  { subject: 'Attention', A: 120, B: 110, fullMark: 150 },
  { subject: 'Memory', A: 98, B: 130, fullMark: 150 },
  { subject: 'Reflection', A: 86, B: 130, fullMark: 150 },
  { subject: 'Emotional Intelligence', A: 99, B: 100, fullMark: 150 },
  { subject: 'Sleep Quality', A: 85, B: 90, fullMark: 150 },
  { subject: 'Social Engagement', A: 65, B: 85, fullMark: 150 },
]

const clusterData = [
  { x: 10, y: 30, z: 200, name: 'Calm State' },
  { x: 40, y: 50, z: 260, name: 'Flow State' },
  { x: 90, y: 15, z: 400, name: 'Anxiety Spike' },
  { x: 60, y: 80, z: 100, name: 'Reflection' },
]

export default function AnalysisPage() {
  return (
    <div className="space-y-8 pb-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="p-8 rounded-[2rem] bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-transparent border border-indigo-500/20"
      >
        <div className="flex flex-col md:flex-row items-center gap-8">
          <div className="w-20 h-20 rounded-2xl bg-indigo-500 flex items-center justify-center text-white shadow-xl shadow-indigo-500/20">
            <BrainCircuit size={40} />
          </div>
          <div className="flex-1">
            <h1 className="text-4xl font-display font-bold">Advanced Neural Analysis</h1>
            <p className="text-muted-foreground mt-2 max-w-2xl">
              Using state-of-the-art machine learning models to analyze your emotional patterns and cognitive metrics across multiple dimensions.
            </p>
          </div>
          <div className="flex gap-4">
            <div className="px-4 py-2 rounded-xl bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 text-center">
              <span className="block text-xs text-muted-foreground uppercase font-bold">Models Active</span>
              <span className="text-xl font-bold">12</span>
            </div>
            <div className="px-4 py-2 rounded-xl bg-white/50 dark:bg-black/20 border border-black/5 dark:border-white/10 text-center">
              <span className="block text-xs text-muted-foreground uppercase font-bold">Data Accuracy</span>
              <span className="text-xl font-bold text-green-500">98.4%</span>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Cognitive Radar Chart */}
        <FloatingCard className="lg:col-span-7 h-[500px]" delay={0.1}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-xl font-bold">Cognitive Profile</h3>
              <p className="text-sm text-muted-foreground">Multi-dimensional analysis of mental performance.</p>
            </div>
            <ShieldCheck className="text-green-500" size={24} />
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={cognitiveData}>
              <PolarGrid stroke="currentColor" opacity={0.1} />
              <PolarAngleAxis dataKey="subject" tick={{ fill: 'currentColor', opacity: 0.7, fontSize: 12 }} />
              <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
              <Radar
                name="Current Week"
                dataKey="A"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.4}
              />
              <Radar
                name="Historical Average"
                dataKey="B"
                stroke="#ec4899"
                fill="#ec4899"
                fillOpacity={0.1}
              />
            </RadarChart>
          </ResponsiveContainer>
        </FloatingCard>

        {/* Behavioral Clustering */}
        <FloatingCard className="lg:col-span-5 h-[500px]" delay={0.2}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-xl font-bold">State Clustering</h3>
              <p className="text-sm text-muted-foreground">AI identifies patterns in your emotional states.</p>
            </div>
            <Microscope className="text-indigo-400" size={24} />
          </div>
          <ResponsiveContainer width="100%" height="70%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <XAxis type="number" dataKey="x" name="Intensity" hide />
              <YAxis type="number" dataKey="y" name="Stability" hide />
              <ZAxis type="number" dataKey="z" range={[100, 1000]} name="Duration" />
              <ReTooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter name="States" data={clusterData} fill="#6366f1">
                {clusterData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 2 ? '#ef4444' : '#6366f1'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
          <div className="space-y-4 mt-4">
            {clusterData.map((item, i) => (
              <div key={i} className="flex items-center gap-4 text-sm">
                <div className={`w-3 h-3 rounded-full ${i === 2 ? 'bg-red-500' : 'bg-indigo-500'}`} />
                <span className="font-medium">{item.name}</span>
                <span className="text-muted-foreground ml-auto">Duration: {item.z}m</span>
              </div>
            ))}
          </div>
        </FloatingCard>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <FloatingCard>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-yellow-500/10 text-yellow-600">
              <Zap size={24} />
            </div>
            <h3 className="text-xl font-bold">Predictive Risk Analysis</h3>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Our Bayesian models predict a <span className="text-green-500 font-bold">low probability (12%)</span> of high stress levels in the next 48 hours based on your current recovery metrics and sleep consistency.
          </p>
          <div className="mt-6 p-4 rounded-xl bg-green-500/5 border border-green-500/10">
            <span className="text-xs font-bold text-green-600 uppercase">Recommendation</span>
            <p className="text-sm mt-1">Model suggests increasing non-focussed rest by 15% to maintain current stability.</p>
          </div>
        </FloatingCard>

        <FloatingCard>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-indigo-500/10 text-indigo-600">
              <Database size={24} />
            </div>
            <h3 className="text-xl font-bold">Data Sources & Fusion</h3>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <span className="block text-xl font-bold">Text</span>
              <span className="text-xs text-muted-foreground">BERT-based</span>
            </div>
            <div>
              <span className="block text-xl font-bold">Face</span>
              <span className="text-xs text-muted-foreground">CNN Model</span>
            </div>
            <div>
              <span className="block text-xl font-bold">Voice</span>
              <span className="text-xs text-muted-foreground">Spectrogram</span>
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-6 text-center italic">
            All analysis is computed on-device or in secure private nodes.
          </p>
        </FloatingCard>
      </div>
    </div>
  )
}