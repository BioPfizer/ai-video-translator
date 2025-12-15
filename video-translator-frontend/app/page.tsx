'use client'

import { useState, useEffect } from 'react'
import { BackgroundRipple } from '@/components/ui/background-ripple'
import { FileUpload } from '@/components/ui/file-upload'
import { SearchBar } from '@/components/ui/search-bar'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { motion, AnimatePresence } from 'framer-motion'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

type TabType = 'upload' | 'url'

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabType>('upload')
  const [file, setFile] = useState<File | null>(null)
  const [url, setUrl] = useState('')
  // const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('zh-CN')
  const [languages, setLanguages] = useState<any[]>([])
  const [status, setStatus] = useState('')
  const [progress, setProgress] = useState(0)
  const [resultVideo, setResultVideo] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [detectedLang, setDetectedLang] = useState<string | null>(null)
  const [lowConfidenceWarning, setLowConfidenceWarning] = useState(false)
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const handleSubmit = async () => {
    if (!file && !url) {
      alert('Please upload a video or enter a URL')
      return
    }

    setIsProcessing(true)
    setStatus('Uploading...')
    setProgress(10)
    setError(null)
    setDetectedLang(null)
    setLowConfidenceWarning(false)

    try {
      const formData = new FormData()
      
      if (activeTab === 'upload' && file) {
        formData.append('file', file)
      } else if (activeTab === 'url') {
        alert('URL feature coming soon! Use upload for now.')
        setIsProcessing(false)
        return
      }
      
      // formData.append('source_lang', sourceLang)
      formData.append('target_lang', targetLang)

      setStatus('Translating video...')
      setProgress(30)

      const response = await fetch(`${API_URL}/api/translate-video`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Translation failed')
      }

      // Extract detected language from headers
      const detectedLanguage = response.headers.get('X-Detected-Language')
      const confidence = parseFloat(response.headers.get('X-Language-Confidence') || '1.0')

      if (detectedLanguage) {
        setDetectedLang(detectedLanguage)
      }

       // Check for low confidence
      if (confidence < 0.7) {
        setLowConfidenceWarning(true)
      }

      setProgress(90)
      setStatus('Creating preview...')

      const blob = await response.blob()
      const videoUrl = URL.createObjectURL(blob)
      
      setResultVideo(videoUrl)
      setStatus('✓ Translation complete!')
      setProgress(100)

    } catch (error: any) {
      setError(error.message || 'Translation failed') // SET error
      setStatus('')
      setProgress(0)
    } finally {
      setIsProcessing(false)
    }
  }

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const response = await fetch(`${API_URL}/api/languages/video`)
        const data = await response.json()
        setLanguages(data.languages)
      } catch (error) {
        console.error('Failed to fetch languages:', error)
        // Fallback to default languages
        setLanguages([
          { code: 'en', name: 'English', native_name: 'English', flag: '🇬🇧' },
          { code: 'zh-CN', name: 'Chinese (Simplified)', native_name: '简体中文', flag: '🇨🇳' },
          { code: 'ms', name: 'Malay', native_name: 'Bahasa Melayu', flag: '🇲🇾' },
        ])
      }
    }
    
    fetchLanguages()
  }, [])

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Background */}
      <BackgroundRipple />

      {/* Content */}
      <div className="relative min-h-screen flex flex-col">
        
        {/* Hero Section */}
        <motion.div 
          className="flex-shrink-0 pt-20 pb-12 text-center px-6 pointer-events-none"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Badge className="mb-4 bg-cyan-500/20 text-cyan-400 border-cyan-500/30 px-4 py-1 pointer-events-auto">
            AI-Powered Translation
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">
            Video Translator
          </h1>
          
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Translate any video to <span className="text-cyan-400 font-semibold">100+ languages</span> in seconds
            <br />with AI-powered speech recognition and synthesis
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="flex-grow flex items-start justify-center px-6 pb-20 z-10">
          <motion.div
            className="w-full max-w-4xl pointer-events-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Card className="bg-slate-900/80 backdrop-blur-xl border-slate-800 shadow-2xl">
              <div className="p-8">
                
                {/* Tab Selector */}
                <div className="flex gap-3 mb-8">
                  <Button
                    onClick={() => setActiveTab('upload')}
                    variant={activeTab === 'upload' ? 'default' : 'outline'}
                    className={`flex-1 h-14 text-base font-semibold ${
                      activeTab === 'upload'
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700'
                        : 'border-slate-700 hover:border-slate-600 hover:bg-slate-800'
                    }`}
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    Upload Video
                  </Button>
                  
                  {/* <Button
                    onClick={() => setActiveTab('url')}
                    variant={activeTab === 'url' ? 'default' : 'outline'}
                    className={`flex-1 h-14 text-base font-semibold ${
                      activeTab === 'url'
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700'
                        : 'border-slate-700 hover:border-slate-600 hover:bg-slate-800'
                    }`}
                  >
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                    From URL
                  </Button> */}
                </div>

                {/* Content Area */}
                <AnimatePresence mode="wait">
                  {activeTab === 'upload' ? (
                    <motion.div
                      key="upload"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <FileUpload onChange={setFile} />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="url"
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <SearchBar
                        value={url}
                        onChange={setUrl}
                        onSubmit={handleSubmit}
                      />
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Language Selection */}
                <motion.div 
                  className="grid grid-cols-2 gap-6 mt-8"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  {/* Source Lang Dropdown */} 
                  {/* <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-3">
                      From Language
                    </label>
                    <Select value={sourceLang} onValueChange={setSourceLang}>
                      <SelectTrigger className="h-12 bg-slate-800/50 border-slate-700 text-slate-200">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="en">🇬🇧 English</SelectItem>
                        <SelectItem value="zh-CN">🇨🇳 Chinese</SelectItem>
                        <SelectItem value="ms">🇲🇾 Malay</SelectItem>
                      </SelectContent>
                    </Select>
                  </div> */}

                  {/* Auto-detect info */}
                  <div className="flex items-center gap-2 text-sm text-slate-400 bg-slate-800/30 rounded-lg p-3 border border-slate-700/50">
                    <svg className="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span>Source language will be automatically detected</span>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-3">
                      Translate To
                    </label>
                    <Select value={targetLang} onValueChange={setTargetLang}>
                      <SelectTrigger className="h-12 bg-slate-800/50 border-slate-700 text-slate-200 w-full">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700 max-h-[300px] overflow-y-auto">
                        {languages.map((lang) => (
                          <SelectItem key={lang.code} value={lang.code}>
                            {lang.flag} {lang.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </motion.div>

                {/* Translate Button */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <Button
                    onClick={handleSubmit}
                    disabled={isProcessing || (!file && !url)}
                    className="w-full mt-8 h-14 text-lg font-bold bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-cyan-500/25"
                  >
                    {isProcessing ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Processing...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Translate Video
                      </>
                    )}
                  </Button>
                </motion.div>

                {/* ERROR ALERT */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-6"
                    >
                      <Alert variant="destructive" className="border-red-500/50 bg-red-500/10">
                        <svg
                          className="h-4 w-4"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                        <AlertTitle className="text-red-400 font-semibold">Error</AlertTitle>
                        <AlertDescription className="text-red-300">
                          {error}
                        </AlertDescription>
                        <button
                          onClick={() => setError(null)}
                          className="absolute top-2 right-2 text-red-400 hover:text-red-300"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </Alert>
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {/* Low Confidence Warning */}
                <AnimatePresence>
                  {lowConfidenceWarning && !error && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-6"
                    >
                      <Alert className="border-amber-500/50 bg-amber-500/10">
                        <svg
                          className="h-4 w-4 text-amber-400"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                          />
                        </svg>
                        <AlertTitle className="text-amber-400 font-semibold">Mixed Language Detected</AlertTitle>
                        <AlertDescription className="text-amber-300">
                          This video may contain multiple languages. Translation accuracy might be affected.
                        </AlertDescription>
                        <button
                          onClick={() => setLowConfidenceWarning(false)}
                          className="absolute top-2 right-2 text-amber-400 hover:text-amber-300"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </Alert>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Progress Section */}
                <AnimatePresence>
                  {status && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-8"
                    >
                      <Card className="bg-slate-800/50 border-slate-700 p-6">
                        <div className="flex items-center justify-between mb-4">
                          <span className="text-slate-300 font-medium">{status}</span>
                          <span className="text-cyan-400 font-bold">{progress}%</span>
                        </div>
                        <Progress value={progress} className="h-2" />
                      </Card>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Result Video */}
                <AnimatePresence>
                  {resultVideo && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 20 }}
                      className="mt-8"
                    >
                      <Card className="bg-slate-800/50 border-slate-700 p-6">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-xl font-bold text-white">
                             Translated Video
                          </h3>
                          <div className="flex gap-2"> 
                            <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                              Ready
                            </Badge>
                            {detectedLang && (
                              <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30">
                                From: {detectedLang === 'en' ? '🇬🇧 EN' : detectedLang === 'zh-CN' ? '🇨🇳 ZH' : '🇲🇾 MS'}
                              </Badge>
                            )}
                          </div>
                        </div>
                        
                        <video
                          src={resultVideo}
                          controls
                          className="w-full rounded-lg shadow-2xl"
                        />
                        
                        <Button
                          asChild
                          className="w-full mt-4 h-12 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                        >
                          <a href={resultVideo} download="translated_video.mp4">
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Download Video
                          </a>
                        </Button>
                      </Card>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </Card>

            {/* Footer */}
            <motion.div
              className="text-center mt-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              <p className="text-slate-500 text-sm">
                Powered by <span className="text-cyan-400">Deepgram</span>, <span className="text-blue-400">Google Translate</span>, and <span className="text-purple-400">Edge-TTS</span>
              </p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  )

  
}
