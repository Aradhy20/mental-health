'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import api from '@/lib/api'
import AnimatedCard from '@/components/animations/AnimatedCard'

export default function WellnessPage() {
    const [moodInput, setMoodInput] = useState('')
    const [moodResult, setMoodResult] = useState<any>(null)
    const [moodHistory, setMoodHistory] = useState<any[]>([])
    const [journalPrompt, setJournalPrompt] = useState('')
    const [copingStrategies, setCopingStrategies] = useState('')
    const [checkinQuestions, setCheckinQuestions] = useState<string[]>([])
    const [activeTab, setActiveTab] = useState('mood')
    const [userId] = useState(1) // TODO: Get from auth

    useEffect(() => {
        loadMoodHistory()
    }, [])

    const loadMoodHistory = async () => {
        try {
            const data = await api.getMoodHistory(userId)
            setMoodHistory(data.history || [])
        } catch (error) {
            console.error('Failed to load mood history:', error)
        }
    }

    const handleMoodSubmit = async () => {
        if (!moodInput.trim()) return

        try {
            const result = await api.trackMood(userId, moodInput)
            setMoodResult(result)
            setMoodInput('')
            loadMoodHistory()
        } catch (error) {
            console.error('Failed to track mood:', error)
        }
    }

    const loadJournalingPrompt = async () => {
        try {
            const data = await api.getJournalingPrompt()
            setJournalPrompt(data.prompt)
        } catch (error) {
            console.error('Failed to load prompt:', error)
        }
    }

    const loadCopingStrategies = async (category: string) => {
        try {
            const data = await api.getCopingStrategies(category)
            setCopingStrategies(data.strategies)
        } catch (error) {
            console.error('Failed to load strategies:', error)
        }
    }

    const loadCheckinQuestions = async () => {
        try {
            const data = await api.getDailyCheckinQuestions()
            setCheckinQuestions(data.questions || [])
        } catch (error) {
            console.error('Failed to load questions:', error)
        }
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
                    <h1 className="text-2xl font-bold text-gray-900">Wellness Center</h1>
                    <p className="text-gray-600 mt-1">Daily check-ins, journaling, and coping strategies</p>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Tabs */}
                <div className="mb-8">
                    <div className="border-b border-gray-200">
                        <nav className="-mb-px flex space-x-8">
                            {[
                                { id: 'mood', label: 'Mood Tracking' },
                                { id: 'journal', label: 'Journaling' },
                                { id: 'coping', label: 'Coping Strategies' },
                                { id: 'checkin', label: 'Daily Check-in' }
                            ].map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === tab.id
                                            ? 'border-blue-600 text-blue-600'
                                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                        }`}
                                >
                                    {tab.label}
                                </button>
                            ))}
                        </nav>
                    </div>
                </div>

                {/* Mood Tracking Tab */}
                {activeTab === 'mood' && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                        <AnimatedCard>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">How are you feeling today?</h2>
                            <div className="space-y-4">
                                <textarea
                                    value={moodInput}
                                    onChange={(e) => setMoodInput(e.target.value)}
                                    placeholder="Describe your mood... (e.g., I'm feeling anxious, happy, stressed, etc.)"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                                    rows={3}
                                />
                                <button
                                    onClick={handleMoodSubmit}
                                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
                                >
                                    Track Mood
                                </button>
                            </div>

                            {moodResult && (
                                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                                    <p className="text-gray-900 font-medium">{moodResult.message}</p>
                                    <p className="text-sm text-gray-600 mt-2">Mood Level: <span className="font-medium capitalize">{moodResult.mood_level}</span></p>
                                    <p className="text-sm text-gray-600 mt-1">{moodResult.follow_up}</p>
                                </div>
                            )}
                        </AnimatedCard>

                        {/* Mood History */}
                        <AnimatedCard>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Mood History</h2>
                            <div className="space-y-3">
                                {moodHistory.length > 0 ? (
                                    moodHistory.map((entry, index) => (
                                        <div key={index} className="p-3 bg-gray-50 rounded-lg">
                                            <p className="text-sm text-gray-600">{new Date(entry.timestamp).toLocaleString()}</p>
                                            <p className="text-gray-900 mt-1">{entry.input}</p>
                                            <span className={`inline-block px-2 py-1 text-xs rounded mt-2 ${entry.mood === 'positive' ? 'bg-green-100 text-green-800' :
                                                    entry.mood === 'negative' ? 'bg-red-100 text-red-800' :
                                                        'bg-gray-100 text-gray-800'
                                                }`}>
                                                {entry.mood}
                                            </span>
                                        </div>
                                    ))
                                ) : (
                                    <p className="text-gray-500">No mood entries yet. Start tracking above!</p>
                                )}
                            </div>
                        </AnimatedCard>
                    </motion.div>
                )}

                {/* Journaling Tab */}
                {activeTab === 'journal' && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                        <AnimatedCard>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Journaling Prompts</h2>
                            <button
                                onClick={loadJournalingPrompt}
                                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium mb-6"
                            >
                                Get New Prompt
                            </button>

                            {journalPrompt && (
                                <div className="mt-6 p-6 bg-purple-50 rounded-lg border-l-4 border-purple-600">
                                    <p className="text-gray-900 whitespace-pre-wrap">{journalPrompt}</p>
                                </div>
                            )}

                            <div className="mt-6">
                                <label className="block text-sm font-medium text-gray-700 mb-2">Your Response</label>
                                <textarea
                                    placeholder="Take your time to reflect and write..."
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                                    rows={8}
                                />
                                <button className="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium">
                                    Save Entry
                                </button>
                            </div>
                        </AnimatedCard>
                    </motion.div>
                )}

                {/* Coping Strategies Tab */}
                {activeTab === 'coping' && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                        <AnimatedCard>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Coping Strategies</h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                                {['anxiety', 'stress', 'sadness', 'general'].map((category) => (
                                    <button
                                        key={category}
                                        onClick={() => loadCopingStrategies(category)}
                                        className="px-4 py-3 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 font-medium capitalize"
                                    >
                                        {category}
                                    </button>
                                ))}
                            </div>

                            {copingStrategies && (
                                <div className="p-6 bg-green-50 rounded-lg border-l-4 border-green-600">
                                    <pre className="whitespace-pre-wrap text-gray-900 font-sans">{copingStrategies}</pre>
                                </div>
                            )}
                        </AnimatedCard>
                    </motion.div>
                )}

                {/* Daily Check-in Tab */}
                {activeTab === 'checkin' && (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                        <AnimatedCard>
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Daily Check-in</h2>
                            <button
                                onClick={loadCheckinQuestions}
                                className="px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 font-medium mb-6"
                            >
                                Start Check-in
                            </button>

                            {checkinQuestions.length > 0 && (
                                <div className="space-y-4">
                                    {checkinQuestions.map((question, index) => (
                                        <div key={index} className="p-4 bg-yellow-50 rounded-lg">
                                            <p className="text-gray-900 font-medium mb-2">{question}</p>
                                            <input
                                                type="text"
                                                placeholder="Your answer..."
                                                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-yellow-500"
                                            />
                                        </div>
                                    ))}
                                    <button className="px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 font-medium">
                                        Submit Check-in
                                    </button>
                                </div>
                            )}
                        </AnimatedCard>
                    </motion.div>
                )}
            </main>
        </div>
    )
}
