'use client'

import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import AnimatedCard from '@/components/animations/AnimatedCard'
import AnimatedButton from '@/components/animations/AnimatedButton'
import AnimatedSpinner from '@/components/animations/AnimatedSpinner'

interface FaceAnalysisResult {
  emotion_label: string
  emotion_score: number
  confidence: number
}

const FaceAnalyzer: React.FC = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<FaceAnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Validate file type
      if (!file.type.match('image.*')) {
        setError('Please select an image file')
        return
      }

      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
      
      // Clear previous results
      setResult(null)
      setError(null)
    }
  }

  const triggerFileSelect = () => {
    fileInputRef.current?.click()
  }

  const analyzeFace = async () => {
    if (!imagePreview) {
      setError('Please select an image first')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock analysis result
      const emotions = ['Happy', 'Sad', 'Angry', 'Surprised', 'Fearful', 'Disgusted', 'Neutral']
      const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)]
      const emotionScore = Math.random() * 0.5 + 0.3 // Between 0.3 and 0.8
      const confidence = Math.random() * 0.3 + 0.7 // Between 0.7 and 1.0
      
      setResult({
        emotion_label: randomEmotion,
        emotion_score: emotionScore,
        confidence: confidence
      })
    } catch (err) {
      setError('Failed to analyze facial expression')
      console.error(err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getEmotionColor = (emotion: string) => {
    switch (emotion.toLowerCase()) {
      case 'happy': return 'bg-yellow-400'
      case 'sad': return 'bg-blue-400'
      case 'angry': return 'bg-red-500'
      case 'surprised': return 'bg-purple-400'
      case 'fearful': return 'bg-gray-400'
      case 'disgusted': return 'bg-green-500'
      case 'neutral': return 'bg-gray-300'
      default: return 'bg-gray-300'
    }
  }

  return (
    <AnimatedCard className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Facial Expression Analysis</h2>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      <div className="flex flex-col md:flex-row gap-6">
        <div className="flex-1">
          <div 
            className="border-2 border-dashed border-gray-300 rounded-lg h-64 flex flex-col items-center justify-center cursor-pointer hover:border-gray-400 transition-colors"
            onClick={triggerFileSelect}
          >
            {imagePreview ? (
              <img 
                src={imagePreview} 
                alt="Preview" 
                className="h-full w-full object-contain rounded-lg"
              />
            ) : (
              <>
                <svg 
                  className="w-12 h-12 text-gray-400 mb-2" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" 
                  />
                </svg>
                <p className="text-gray-500">Click to upload face photo</p>
                <p className="text-gray-400 text-sm mt-1">or drag and drop</p>
              </>
            )}
          </div>
          
          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            accept="image/*"
            onChange={handleFileSelect}
          />
          
          <div className="mt-4 flex gap-3">
            <AnimatedButton
              onClick={triggerFileSelect}
              variant="outline"
              className="flex-1"
            >
              Choose Photo
            </AnimatedButton>
            
            <AnimatedButton
              onClick={analyzeFace}
              variant="primary"
              className="flex-1"
              disabled={isAnalyzing || !imagePreview}
            >
              {isAnalyzing ? (
                <>
                  <AnimatedSpinner size="sm" className="mr-2" />
                  Analyzing
                </>
              ) : (
                'Analyze Face'
              )}
            </AnimatedButton>
          </div>
        </div>
        
        <div className="flex-1">
          {result ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="h-full flex flex-col"
            >
              <h3 className="font-medium text-gray-900 mb-3">Analysis Results</h3>
              
              <div className="flex-1 flex flex-col items-center justify-center bg-gray-50 rounded-lg p-6">
                <div className={`w-24 h-24 rounded-full ${getEmotionColor(result.emotion_label)} flex items-center justify-center mb-4`}>
                  <span className="text-3xl">
                    {result.emotion_label === 'Happy' && '😊'}
                    {result.emotion_label === 'Sad' && '😢'}
                    {result.emotion_label === 'Angry' && '😠'}
                    {result.emotion_label === 'Surprised' && '😲'}
                    {result.emotion_label === 'Fearful' && '😨'}
                    {result.emotion_label === 'Disgusted' && '🤢'}
                    {result.emotion_label === 'Neutral' && '😐'}
                  </span>
                </div>
                
                <h4 className="text-2xl font-bold text-gray-900 mb-2">
                  {result.emotion_label}
                </h4>
                
                <div className="w-full max-w-xs">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Confidence</span>
                    <span className="font-medium">{(result.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <motion.div 
                      className={`h-2 rounded-full ${getEmotionColor(result.emotion_label)}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${result.confidence * 100}%` }}
                      transition={{ duration: 1 }}
                    />
                  </div>
                  
                  <div className="flex justify-between text-sm mt-4 mb-1">
                    <span className="text-gray-600">Emotion Intensity</span>
                    <span className="font-medium">{(result.emotion_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <motion.div 
                      className={`h-2 rounded-full ${getEmotionColor(result.emotion_label)}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${result.emotion_score * 100}%` }}
                      transition={{ duration: 1 }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center bg-gray-50 rounded-lg p-6 text-center">
              <svg 
                className="w-12 h-12 text-gray-400 mb-3" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" 
                />
              </svg>
              <h3 className="font-medium text-gray-900 mb-1">Ready to Analyze</h3>
              <p className="text-gray-500 text-sm">
                Upload a clear photo of your face to detect emotions
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">How it works</h4>
        <ul className="text-sm text-gray-600 list-disc pl-5 space-y-1">
          <li>Detects facial landmarks and expressions</li>
          <li>Identifies 7 primary emotions with confidence scores</li>
          <li>Works best with frontal, well-lit photos</li>
        </ul>
      </div>
    </AnimatedCard>
  )
}

export default FaceAnalyzer