'use client'

import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { MapPin, Star, Phone, ShieldCheck, ChevronRight } from 'lucide-react'
import FloatingCard from './FloatingCard'

interface Doctor {
    doctor_id: number
    name: string
    specialization: string
    address: string
    rating: number
    contact: string
}

export default function SpecialistGrid() {
    const [doctors, setDoctors] = useState<Doctor[]>([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchDoctors = async () => {
            try {
                // Fetching with empty specialization to get all seeded doctors
                const response = await fetch('http://localhost:8006/v1/doctor/specialists?specialization=')
                if (response.ok) {
                    const data = await response.json()
                    setDoctors(data.doctors.slice(0, 3)) // Show top 3
                }
            } catch (err) {
                console.error('Failed to fetch doctors:', err)
            } finally {
                setIsLoading(false)
            }
        }
        fetchDoctors()
    }, [])

    if (isLoading) return <div className="h-48 animate-pulse bg-black/5 rounded-3xl" />
    if (doctors.length === 0) return null

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between px-2">
                <h3 className="text-xl font-bold flex items-center gap-2">
                    <ShieldCheck size={20} className="text-serenity-600" />
                    Trusted Specialists Nearby
                </h3>
                <button className="text-xs font-bold text-serenity-600 uppercase tracking-widest flex items-center gap-1 hover:gap-2 transition-all">
                    View All <ChevronRight size={14} />
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {doctors.map((doctor, i) => (
                    <FloatingCard key={doctor.doctor_id} delay={i * 0.1} className="group hover:bg-white dark:hover:bg-white/5 transition-all">
                        <div className="flex flex-col h-full">
                            <div className="flex justify-between items-start mb-4">
                                <div className="w-12 h-12 rounded-2xl bg-serenity-500/10 flex items-center justify-center text-serenity-600">
                                    <Star size={24} fill={doctor.rating > 4.5 ? "currentColor" : "none"} />
                                </div>
                                <div className="flex items-center gap-1 text-sm font-bold bg-amber-500/10 text-amber-600 px-2 py-1 rounded-lg">
                                    <Star size={12} fill="currentColor" />
                                    {doctor.rating}
                                </div>
                            </div>

                            <h4 className="font-bold text-lg group-hover:text-serenity-600 transition-colors truncate">
                                {doctor.name}
                            </h4>
                            <p className="text-xs text-serenity-600 font-bold uppercase tracking-tighter mb-4">
                                {doctor.specialization}
                            </p>

                            <div className="space-y-2 mt-auto">
                                <div className="flex items-start gap-2 text-xs text-muted-foreground">
                                    <MapPin size={14} className="shrink-0 mt-0.5" />
                                    <span className="line-clamp-1">{doctor.address}</span>
                                </div>
                                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                    <Phone size={14} className="shrink-0" />
                                    <span>{doctor.contact}</span>
                                </div>
                            </div>
                        </div>
                    </FloatingCard>
                ))}
            </div>
        </div>
    )
}
