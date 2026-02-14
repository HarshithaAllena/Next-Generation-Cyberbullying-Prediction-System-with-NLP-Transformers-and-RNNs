import { useState } from 'react'
import { AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import InputPanel from './components/InputPanel'
import ResultCard from './components/ResultCard'
import HistoryPanel from './components/HistoryPanel'
import { ClassifyResponse } from './api/types'

function App() {
  const [result, setResult] = useState<ClassifyResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [history, setHistory] = useState<Array<{text: string; result: ClassifyResponse}>>([])

  const handleAnalyze = async (text: string) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, include_explanation: false })
      })
      const data = await response.json()
      setResult(data)
      setHistory(prev => [{ text, result: data }, ...prev.slice(0, 9)])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleHistoryClick = (_text: string, result: ClassifyResponse) => {
    setResult(result)
  }

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <InputPanel onAnalyze={handleAnalyze} isLoading={isLoading} />
            <AnimatePresence mode="wait">
              {result && (
                <ResultCard result={result} key="result" />
              )}
            </AnimatePresence>
          </div>
          
          <div className="lg:col-span-1">
            <HistoryPanel history={history} onSelect={handleHistoryClick} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
