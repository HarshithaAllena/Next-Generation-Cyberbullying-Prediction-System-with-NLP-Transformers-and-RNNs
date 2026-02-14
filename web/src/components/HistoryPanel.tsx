import { motion, AnimatePresence } from 'framer-motion'
import { Clock, Trash2, MessageSquare } from 'lucide-react'
import { ClassifyResponse } from '../api/types'
import clsx from 'clsx'

interface HistoryItem {
  text: string
  result: ClassifyResponse
}

interface HistoryPanelProps {
  history: HistoryItem[]
  onSelect: (text: string, result: ClassifyResponse) => void
}

const labelColors: Record<string, string> = {
  bullying: 'text-red-400',
  harassment: 'text-amber-400',
  hate_speech: 'text-orange-400',
  not_bullying: 'text-green-400',
}

export default function HistoryPanel({ history, onSelect }: HistoryPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-card rounded-2xl p-6 h-fit sticky top-24"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-slate-400" />
          <h2 className="text-lg font-semibold text-white">Recent Analyses</h2>
        </div>
        {history.length > 0 && (
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="p-2 text-slate-400 hover:text-red-400 transition-colors"
            title="Clear history"
          >
            <Trash2 className="w-4 h-4" />
          </motion.button>
        )}
      </div>

      <AnimatePresence mode="popLayout">
        {history.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center py-8"
          >
            <MessageSquare className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-500 text-sm">No analyses yet</p>
            <p className="text-slate-600 text-xs mt-1">Your history will appear here</p>
          </motion.div>
        ) : (
          <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
            {history.map((item, index) => {
              const colorClass = labelColors[item.result.predicted_label] || labelColors.not_bullying
              const preview = item.text.length > 60 ? item.text.slice(0, 60) + '...' : item.text
              
              return (
                <motion.button
                  key={item.result.text_id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => onSelect(item.text, item.result)}
                  className="w-full text-left p-3 rounded-xl bg-slate-800/30 hover:bg-slate-800/60 transition-all group"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <p className="text-sm text-slate-300 line-clamp-2 mb-2">
                    {preview}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className={clsx("text-xs font-medium capitalize", colorClass)}>
                      {item.result.predicted_label.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-slate-500">
                      {(item.result.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </motion.button>
              )
            })}
          </div>
        )}
      </AnimatePresence>

      {history.length > 0 && (
        <motion.div
          className="mt-4 pt-4 border-t border-slate-700/50 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <p className="text-xs text-slate-500">
            {history.length} analysis{history.length !== 1 ? 's' : ''} stored
          </p>
        </motion.div>
      )}
    </motion.div>
  )
}
