'use client'

import React from 'react'
import { motion } from 'framer-motion'
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis,
  Tooltip as ReTooltip, Cell
} from 'recharts'
import { BrainCircuit, ShieldCheck, Microscope, Zap, Database, Activity, Sparkles } from 'lucide-react'
import FloatingCard from '@/components/anti-gravity/FloatingCard'
import FaceAnalyzer from '@/components/features/FaceAnalyzer'
import VoiceAnalyzer from '@/components/features/VoiceAnalyzer'
import { useAuthStore } from '@/lib/store/auth-store'

const cognitiveData = [
  { subject: 'Attention', A: 120, B: 110, fullMark: 150 },
  { subject: 'Memory', A: 98, B: 130, fullMark: 150 },
  { subject: 'Reflection', A: 86, B: 130, fullMark: 150 },
  { subject: 'Logic', A: 99, B: 100, fullMark: 150 },
  { subject: 'Sleep', A: 85, B: 90, fullMark: 150 },
  { subject: 'Social', A: 65, B: 85, fullMark: 150 },
]

const clusterData = [
  { x: 10, y: 30, z: 200, name: 'Calm State' },
  { x: 40, y: 50, z: 260, name: 'Flow State' },
  { x: 90, y: 15, z: 400, name: 'Anxiety Spike' },
  { x: 60, y: 80, z: 100, name: 'Reflection' },
]

export default function AnalysisPage() {
  const { user } = useAuthStore()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null;

  return (
    <div className="space-y-10 pb-20">
      {/* Hub Header */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        className="p-8 rounded-[2.5rem] bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-transparent border border-white/5 relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 p-8 opacity-10">
          <BrainCircuit size={160} />
        </div>

        <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
          <div className="w-24 h-24 rounded-3xl bg-indigo-600 flex items-center justify-center text-white shadow-2xl shadow-indigo-600/40">
            <Activity size={48} />
          </div>
          <div className="flex-1 text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[10px] font-bold tracking-widest uppercase mb-3">
              <Sparkles size={12} />
              Neural Diagnostics Hub
            </div>
            <h1 className="text-5xl font-display font-bold text-white tracking-tight">AI Intuition Engine</h1>
            <p className="text-slate-400 mt-2 max-w-2xl font-medium">
              Welcome, {user?.full_name || 'Seeker'}. Our cognitive models are analyzing your multi-modal data streams for real-time wellness insights.
            </p>
          </div>
          <div className="flex gap-4">
            <div className="px-6 py-3 rounded-2xl bg-white/5 border border-white/10 text-center backdrop-blur-md">
              <span className="block text-[10px] text-slate-500 uppercase font-bold tracking-widest">Confidence</span>
              <span className="text-2xl font-display font-bold text-emerald-400">98.4%</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Live Lab Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4">
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-slate-500 uppercase tracking-[0.3em] pl-2">Vocal Scan</h2>
          <VoiceAnalyzer />
        </div>
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-slate-500 uppercase tracking-[0.3em] pl-2">Visual Scan</h2>
          <FaceAnalyzer />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Cognitive Radar Chart */}
        <FloatingCard className="lg:col-span-7 aspect-square md:aspect-auto md:h-[500px] glass-panel border-white/5" delay={0.1}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-xl font-bold text-white">Cognitive Profile</h3>
              <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">Multi-model Synthesis</p>
            </div>
            <ShieldCheck className="text-emerald-500" size={24} />
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={cognitiveData}>
              <PolarGrid stroke="rgba(255,255,255,0.05)" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 'bold' }} />
              <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
              <Radar
                name="Current State"
                dataKey="A"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.3}
              />
              <Radar
                name="Baseline"
                dataKey="B"
                stroke="#ec4899"
                fill="#ec4899"
                fillOpacity={0.05}
              />
            </RadarChart>
          </ResponsiveContainer>
        </FloatingCard>

        {/* Behavioral Clustering */}
        <FloatingCard className="lg:col-span-5 h-[500px] glass-panel border-white/5" delay={0.2}>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-xl font-bold text-white">State Clustering</h3>
              <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">Self-Organizing Map (SOM)</p>
            </div>
            <Microscope className="text-indigo-400" size={24} />
          </div>
          <ResponsiveContainer width="100%" height="70%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <XAxis type="number" dataKey="x" name="Intensity" hide />
              <YAxis type="number" dataKey="y" name="Stability" hide />
              <ZAxis type="number" dataKey="z" range={[100, 1000]} name="Duration" />
              <ReTooltip
                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                itemStyle={{ color: '#fff', fontSize: '10px', fontWeight: 'bold' }}
              />
              <Scatter name="States" data={clusterData}>
                {clusterData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 2 ? '#f43f5e' : '#6366f1'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 gap-4 mt-6">
            {clusterData.map((item, i) => (
              <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
                <div className={`w-2 h-2 rounded-full ${i === 2 ? 'bg-rose-500 shadow-[0_0_8px_#f43f5e]' : 'bg-indigo-500'}`} />
                <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">{item.name}</span>
              </div>
            ))}
          </div>
        </FloatingCard>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <FloatingCard className="glass-panel border-white/5 relative overflow-hidden">
          <div className="absolute -right-4 -bottom-4 opacity-5">
            <Zap size={120} />
          </div>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-amber-500/10 text-amber-500">
              <Zap size={24} />
            </div>
            <h3 className="text-xl font-bold text-white">Predictive Risk Matrix</h3>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            Our Bayesian inference engine predicts a <span className="text-emerald-400 font-bold underline decoration-emerald-400/30">low probability (12%)</span> of stress escalation in the next cycle.
          </p>
          <div className="mt-8 p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20">
            <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-[0.2em] block mb-2">Recommendation</span>
            <p className="text-sm text-slate-200">Maintain current non-focussed rest cycles. Recovery metrics are optimal.</p>
          </div>
        </FloatingCard>

        <FloatingCard className="glass-panel border-white/5">
          <div className="flex items-center gap-4 mb-6">
            <div className="p-3 rounded-2xl bg-indigo-500/10 text-indigo-400">
              <Database size={24} />
            </div>
            <h3 className="text-xl font-bold text-white">Data Source Fusion</h3>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
              <span className="block text-lg font-display font-bold text-white">Text</span>
              <span className="text-[8px] text-slate-500 font-bold uppercase tracking-widest">BERT-RAG</span>
            </div>
            <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
              <span className="block text-lg font-display font-bold text-white">Face</span>
              <span className="text-[8px] text-slate-500 font-bold uppercase tracking-widest">ResNet CNN</span>
            </div>
            <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
              <span className="block text-lg font-display font-bold text-white">Voice</span>
              <span className="text-[8px] text-slate-500 font-bold uppercase tracking-widest">SpectroV3</span>
            </div>
          </div>
          <div className="mt-8 flex items-center justify-center gap-2">
            <ShieldCheck size={14} className="text-emerald-400" />
            <span className="text-[10px] text-slate-600 font-bold uppercase tracking-[0.3em]">Encrypted Analysis Nodes</span>
          </div>
        </FloatingCard>
      </div>
    </div>
  )
}
