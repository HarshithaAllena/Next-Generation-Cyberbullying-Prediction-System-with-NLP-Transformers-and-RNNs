import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  CheckCircle, 
  AlertOctagon, 
  Ban,
  TrendingUp,
  Brain
} from 'lucide-react'
import { ClassifyResponse } from '../api/types'
import clsx from 'clsx'

interface ResultCardProps {
  result: ClassifyResponse
}

const labelConfig: Record<string, { icon: typeof AlertTriangle; color: string; bgColor: string }> = {
  bullying: { icon: AlertOctagon, color: 'text-red-400', bgColor: 'bg-red-500/20' },
  harassment: { icon: AlertTriangle, color: 'text-amber-400', bgColor: 'bg-amber-500/20' },
  hate_speech: { icon: Ban, color: 'text-orange-400', bgColor: 'bg-orange-500/20' },
  not_bullying: { icon: CheckCircle, color: 'text-green-400', bgColor: 'bg-green-500/20' },
}

export default function ResultCard({ result }: ResultCardProps) {
  const config = labelConfig[result.predicted_label] || labelConfig.not_bullying
  const Icon = config.icon
  const confidence = result.confidence * 100

  const sortedProbs = Object.entries(result.probabilities)
    .sort(([, a], [, b]) => b - a)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="glass-card rounded-2xl overflow-hidden"
    >
      {/* Header with result */}
      <div className={clsx("p-6", config.bgColor)}>
        <div className="flex items-center justify-between">
          <motion.div 
            className="flex items-center gap-4"
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <motion.div
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Icon className={clsx("w-12 h-12", config.color)} />
            </motion.div>
            <div>
              <h3 className={clsx("text-2xl font-bold capitalize", config.color)}>
                {result.predicted_label.replace('_', ' ')}
              </h3>
              <p className="text-sm text-slate-400">
                {result.is_high_confidence ? 'High confidence detection' : 'Moderate confidence'}
              </p>
            </div>
          </motion.div>

          <motion.div
            className="text-right"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="text-4xl font-bold gradient-text">
              {confidence.toFixed(1)}%
            </div>
            <p className="text-sm text-slate-400">Confidence</p>
          </motion.div>
        </div>

        {/* Confidence bar */}
        <motion.div 
          className="mt-4 h-2 bg-slate-700/50 rounded-full overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <motion.div
            className="h-full bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400"
            initial={{ width: 0 }}
            animate={{ width: `${confidence}%` }}
            transition={{ duration: 0.8, delay: 0.5, ease: "easeOut" }}
          />
        </motion.div>
      </div>

      {/* Probability breakdown */}
      <div className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-slate-400" />
          <h4 className="text-sm font-semibold text-slate-300">Probability Breakdown</h4>
        </div>

        <div className="space-y-3">
          {sortedProbs.map(([label, prob], index) => {
            const isPredicted = label === result.predicted_label
            const itemConfig = labelConfig[label] || labelConfig.not_bullying
            
            return (
              <motion.div
                key={label}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className={clsx(
                  "flex items-center gap-3 p-3 rounded-lg transition-colors",
                  isPredicted ? itemConfig.bgColor : "bg-slate-800/30"
                )}
              >
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className={clsx("font-medium capitalize", isPredicted ? itemConfig.color : "text-slate-400")}>
                      {label.replace('_', ' ')}
                    </span>
                    <span className={clsx("font-mono", isPredicted ? "text-white" : "text-slate-500")}>
                      {(prob * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-700/50 rounded-full overflow-hidden">
                    <motion.div
                      className={clsx("h-full rounded-full", isPredicted ? "bg-gradient-to-r from-cyan-400 to-purple-400" : "bg-slate-600")}
                      initial={{ width: 0 }}
                      animate={{ width: `${prob * 100}%` }}
                      transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                    />
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Model info */}
        <motion.div
          className="mt-6 pt-4 border-t border-slate-700/50 flex items-center gap-2 text-sm text-slate-500"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <Brain className="w-4 h-4" />
          <span>Model version: {result.model_version}</span>
        </motion.div>
      </div>
    </motion.div>
  )
}
