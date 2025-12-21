import './globals.css'
import type { Metadata } from 'next'
import { Inter, Outfit } from 'next/font/google'
import { ThemeProvider } from 'next-themes'
import dynamic from 'next/dynamic'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' })

// Dynamic imports for heavy components to speed up initial load
const AnimatedSidebar = dynamic(() => import('@/components/anti-gravity/AnimatedSidebar'), {
  ssr: false,
  loading: () => <div className="w-[280px] h-screen bg-white/5 dark:bg-black/5 animate-pulse hidden md:block" />
})
const MobileBottomNav = dynamic(() => import('@/components/layout/MobileBottomNav'), { ssr: false })
const ParallaxBackground = dynamic(() => import('@/components/anti-gravity/ParallaxBackground'), { ssr: false })
const AuthGuard = dynamic(() => import('@/components/auth/AuthGuard'), { ssr: false })

export const metadata: Metadata = {
  title: 'MindfulAI - Anti-Gravity Wellness',
  description: 'Next-generation mental health tracking with AI',
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#f4f7f5' },
    { media: '(prefers-color-scheme: dark)', color: '#1e0b5e' },
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${outfit.variable} font-sans antialiased overflow-x-hidden`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <AuthGuard>
            <div className="flex min-h-screen relative">
              <ParallaxBackground />

              <AnimatedSidebar />

              <main className="flex-1 relative z-10 pb-24 md:pb-8 px-4 md:px-8 pt-6 md:pt-8 max-w-7xl mx-auto w-full">
                {children}
              </main>

              <MobileBottomNav />
            </div>
          </AuthGuard>
        </ThemeProvider>
      </body>
    </html>
  )
}
