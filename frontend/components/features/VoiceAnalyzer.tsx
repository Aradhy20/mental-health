'use client'

import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import AnimatedCard from '@/components/animations/AnimatedCard'
import AnimatedButton from '@/components/animations/AnimatedButton'
import AnimatedSpinner from '@/components/animations/AnimatedSpinner'

interface VoiceAnalysisResult {
  stress_label: string
  stress_score: number
  confidence: number
}

const VoiceAnalyzer: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<VoiceAnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      mediaRecorderRef.current.onstop = async () => {
        setIsAnalyzing(true)
        try {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
          // In a real implementation, we would send this to the backend
          // For now, we'll simulate the analysis
          await simulateVoiceAnalysis(audioBlob)
        } catch (err) {
          setError('Failed to analyze voice recording')
          console.error(err)
        } finally {
          setIsAnalyzing(false)
        }
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (err) {
      setError('Failed to access microphone')
      console.error(err)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      // Stop all tracks to release microphone
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
    }
  }

  const simulateVoiceAnalysis = async (audioBlob: Blob) => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock analysis result based on audio size
    const audioSize = audioBlob.size
    const stressScore = Math.min(audioSize / 10000, 0.95)
    
    let stressLabel = 'calm'
    if (stressScore < 0.2) stressLabel = 'calm'
    else if (stressScore < 0.4) stressLabel = 'mild_stress'
    else if (stressScore < 0.6) stressLabel = 'moderate_stress'
    else if (stressScore < 0.8) stressLabel = 'high_stress'
    else stressLabel = 'anxiety'
    
    const confidence = Math.min(0.5 + (audioSize / 20000), 0.95)
    
    setResult({
      stress_label: stressLabel,
      stress_score: stressScore,
      confidence: confidence
    })
  }

  const getStressColor = (label: string) => {
    switch (label) {
      case 'calm': return 'bg-green-500'
      case 'mild_stress': return 'bg-yellow-500'
      case 'moderate_stress': return 'bg-orange-500'
      case 'high_stress': return 'bg-red-500'
      case 'anxiety': return 'bg-red-700'
      default: return 'bg-gray-500'
    }
  }

  const getStressLabel = (label: string) => {
    switch (label) {
      case 'calm': return 'Calm'
      case 'mild_stress': return 'Mild Stress'
      case 'moderate_stress': return 'Moderate Stress'
      case 'high_stress': return 'High Stress'
      case 'anxiety': return 'Anxiety'
      default: return label
    }
  }

  return (
    <AnimatedCard className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Voice Stress Analysis</h2>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      <div className="flex flex-col items-center justify-center py-8">
        <div className="relative mb-6">
          <motion.div
            className={`w-24 h-24 rounded-full ${isRecording ? 'bg-red-500' : 'bg-gray-300'} flex items-center justify-center`}
            animate={isRecording ? { scale: [1, 1.1, 1] } : {}}
            transition={{ duration: 1, repeat: isRecording ? Infinity : 0 }}
          >
            <svg 
              className="w-12 h-12 text-white" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
              />
            </svg>
          </motion.div>
          
          {isRecording && (
            <motion.div
              className="absolute inset-0 rounded-full bg-red-500 opacity-30"
              animate={{ scale: [1, 1.5], opacity: [0.3, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          )}
        </div>

        <p className="text-gray-600 mb-6 text-center">
          {isRecording 
            ? "Recording... Speak naturally about your feelings" 
            : "Click record to analyze your voice for stress indicators"}
        </p>

        <div className="flex gap-4">
          {!isRecording ? (
            <AnimatedButton
              onClick={startRecording}
              variant="primary"
              size="lg"
              disabled={isAnalyzing}
            >
              <svg 
                className="w-5 h-5 mr-2" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
                />
              </svg>
              Record
            </AnimatedButton>
          ) : (
            <AnimatedButton
              onClick={stopRecording}
              variant="outline"
              size="lg"
              disabled={isAnalyzing}
            >
              <svg 
                className="w-5 h-5 mr-2" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
                />
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" 
                />
              </svg>
              Stop
            </AnimatedButton>
          )}

          {isAnalyzing && (
            <div className="flex items-center">
              <AnimatedSpinner size="md" className="mr-2" />
              <span>Analyzing...</span>
            </div>
          )}
        </div>
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6 p-4 bg-gray-50 rounded-lg"
        >
          <h3 className="font-medium text-gray-900 mb-3">Analysis Results</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className={`inline-block px-3 py-1 rounded-full text-white text-sm ${getStressColor(result.stress_label)}`}>
                {getStressLabel(result.stress_label)}
              </div>
              <p className="text-xs text-gray-500 mt-1">Stress Level</p>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {(result.stress_score * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-gray-500 mt-1">Stress Score</p>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {(result.confidence * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-gray-500 mt-1">Confidence</p>
            </div>
          </div>
          
          <div className="mt-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Stress Indicator</span>
              <span className="font-medium">{(result.stress_score * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div 
                className={`h-2 rounded-full ${getStressColor(result.stress_label)}`}
                initial={{ width: 0 }}
                animate={{ width: `${result.stress_score * 100}%` }}
                transition={{ duration: 1 }}
              />
            </div>
          </div>
        </motion.div>
      )}

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">How it works</h4>
        <ul className="text-sm text-gray-600 list-disc pl-5 space-y-1">
          <li>Analyzes pitch, intensity, and jitter in your voice</li>
          <li>Detects stress patterns and emotional indicators</li>
          <li>Provides actionable insights for stress management</li>
        </ul>
      </div>
    </AnimatedCard>
  )
}

export default VoiceAnalyzer