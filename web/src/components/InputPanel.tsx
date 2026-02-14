import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Sparkles, AlertTriangle } from 'lucide-react'

interface InputPanelProps {
  onAnalyze: (text: string) => void
  isLoading: boolean
}

export default function InputPanel({ onAnalyze, isLoading }: InputPanelProps) {
  const [text, setText] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (text.trim() && !isLoading) {
      onAnalyze(text.trim())
    }
  }

  const charCount = text.length
  const maxChars = 5000

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      className="glass-card rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-5 h-5 text-cyan-400" />
        <h2 className="text-lg font-semibold text-white">Analyze Content</h2>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="relative">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value.slice(0, maxChars))}
            placeholder="Enter text to analyze for cyberbullying, harassment, or hate speech..."
            className="w-full h-48 bg-dark-bg/50 border border-dark-border rounded-xl p-4 text-white placeholder-slate-500 resize-none transition-all duration-300"
            disabled={isLoading}
          />
          
          <AnimatePresence>
            {charCount > maxChars * 0.9 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="absolute bottom-3 right-3 flex items-center gap-1 text-amber-400 text-sm"
              >
                <AlertTriangle className="w-4 h-4" />
                <span>{charCount}/{maxChars}</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="flex items-center justify-between mt-4">
          <span className="text-sm text-slate-400">
            {charCount} / {maxChars} characters
          </span>
          
          <motion.button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02, boxShadow: "0 0 30px rgba(14, 165, 233, 0.4)" }}
            whileTap={{ scale: 0.98 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            {isLoading ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Analyze</span>
              </>
            )}
          </motion.button>
        </div>
      </form>
    </motion.div>
  )
}
