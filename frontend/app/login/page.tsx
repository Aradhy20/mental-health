'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Mail, Lock, Phone, ArrowRight, Loader2, KeyRound, Smartphone, Mail as MailIcon } from 'lucide-react';
import { authAPI } from '@/lib/api';
import { useAuthStore } from '@/lib/store/auth-store';

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.login);
  const [loginMode, setLoginMode] = useState<'email' | 'phone'>('email');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1); // Step 1: Request, Step 2: Verify (for phone)

  const [emailData, setEmailData] = useState({ email: '', password: '' });
  const [phoneData, setPhoneData] = useState({ phone: '', otp: '' });

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await authAPI.login(emailData);
      setAuth(response.data.user, response.data.token);
      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRequestOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await authAPI.requestOTP(phoneData.phone);
      if (response.data.debug_otp) {
        // DEV: Show OTP to user since SMS is not real
        setError(`DEV MODE CODE: ${response.data.debug_otp}`);
      }
      setStep(2);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Could not send OTP');
    } finally {
      setIsLoading(false);
    }
  };


  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    try {
      const response = await authAPI.verifyOTP(phoneData.phone, phoneData.otp);
      setAuth(response.data.user, response.data.token);
      router.push('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Invalid or expired OTP');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#0A0A0F]">

      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-purple-600/5 rounded-full blur-[120px] -z-10" />
      <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[120px] -z-10" />

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md"
      >
        <div className="glass-panel p-8 md:p-10 rounded-3xl border border-white/10 shadow-2xl relative">

          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-gray-400 text-sm">Select your preferred access protocol.</p>
          </div>

          {/* Login Mode Switcher */}
          <div className="flex p-1 bg-white/5 rounded-xl mb-8 border border-white/5">
            <button
              onClick={() => { setLoginMode('email'); setStep(1); setError(''); }}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-lg text-sm font-bold transition-all ${loginMode === 'email' ? 'bg-white text-black shadow-lg' : 'text-gray-400 hover:text-white'}`}
            >
              <MailIcon size={16} /> Email
            </button>
            <button
              onClick={() => { setLoginMode('phone'); setStep(1); setError(''); }}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-lg text-sm font-bold transition-all ${loginMode === 'phone' ? 'bg-white text-black shadow-lg' : 'text-gray-400 hover:text-white'}`}
            >
              <Smartphone size={16} /> Mobile OTP
            </button>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className={`p-3 mb-6 rounded-lg border text-xs text-center font-medium ${error.includes('DEV MODE')
                  ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                  : 'bg-red-500/10 border-red-500/20 text-red-400'
                }`}
            >
              {error}
            </motion.div>
          )}

          <AnimatePresence mode="wait">
            {loginMode === 'email' ? (
              <motion.form
                key="email-form"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                onSubmit={handleEmailLogin}
                className="space-y-6"
              >
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Email Terminal</label>
                    <div className="relative group">
                      <MailIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 group-focus-within:text-purple-400" size={18} />
                      <input
                        type="email"
                        placeholder="identity@protocol.com"
                        value={emailData.email}
                        onChange={(e) => setEmailData({ ...emailData, email: e.target.value })}
                        className="w-full pl-11 pr-4 py-4 rounded-2xl glass-input focus:outline-none text-sm"
                        required
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Access Key</label>
                    <div className="relative group">
                      <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 group-focus-within:text-purple-400" size={18} />
                      <input
                        type="password"
                        placeholder="••••••••"
                        value={emailData.password}
                        onChange={(e) => setEmailData({ ...emailData, password: e.target.value })}
                        className="w-full pl-11 pr-4 py-4 rounded-2xl glass-input focus:outline-none text-sm"
                        required
                      />
                    </div>
                  </div>
                </div>
                <button type="submit" disabled={isLoading} className="w-full py-4 rounded-2xl bg-white text-black font-black hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
                  {isLoading ? <Loader2 className="animate-spin" /> : 'SIGN IN WITH PASSWORD'}
                  {!isLoading && <ArrowRight size={18} />}
                </button>
              </motion.form>
            ) : (
              <motion.form
                key="phone-form"
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                onSubmit={step === 1 ? handleRequestOTP : handleVerifyOTP}
                className="space-y-6"
              >
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Mobile Terminal</label>
                    <div className="relative group">
                      <Smartphone className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 group-focus-within:text-blue-400" size={18} />
                      <input
                        type="tel"
                        placeholder="+91-XXXXX-XXXXX"
                        disabled={step === 2}
                        value={phoneData.phone}
                        onChange={(e) => setPhoneData({ ...phoneData, phone: e.target.value })}
                        className="w-full pl-11 pr-4 py-4 rounded-2xl glass-input focus:outline-none text-sm disabled:opacity-50"
                        required
                      />
                    </div>
                  </div>

                  {step === 2 && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-2">
                      <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-1">Verification Code (OTP)</label>
                      <div className="relative group">
                        <KeyRound className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 group-focus-within:text-green-400" size={18} />
                        <input
                          type="text"
                          placeholder="6-Digit Code"
                          value={phoneData.otp}
                          onChange={(e) => setPhoneData({ ...phoneData, otp: e.target.value })}
                          className="w-full pl-11 pr-4 py-4 rounded-2xl glass-input focus:outline-none text-sm"
                          required
                          maxLength={6}
                        />
                      </div>
                      <p className="text-[10px] text-gray-500 mt-1 ml-1 cursor-pointer hover:text-white" onClick={() => setStep(1)}>Didn't get code? Resend Request</p>
                    </motion.div>
                  )}
                </div>

                <button type="submit" disabled={isLoading} className="w-full py-4 rounded-2xl bg-white text-black font-black hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
                  {isLoading ? <Loader2 className="animate-spin" /> : (step === 1 ? 'REQUEST OTP' : 'VERIFY & SIGN IN')}
                  {!isLoading && <ArrowRight size={18} />}
                </button>
              </motion.form>
            )}
          </AnimatePresence>

          <div className="mt-10 text-center text-sm text-gray-500">
            No professional account?{' '}
            <Link href="/register" className="text-white hover:text-purple-400 transition-colors font-bold border-b border-white/10 pb-0.5">
              Request Enrollment
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}