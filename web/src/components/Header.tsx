import { motion } from 'framer-motion'
import { Shield, ShieldCheck } from 'lucide-react'

export default function Header() {
  return (
    <motion.header 
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="glass sticky top-0 z-50 border-b border-slate-700/50"
    >
      <div className="container mx-auto px-4 py-4 max-w-6xl">
        <div className="flex items-center justify-between">
          <motion.div 
            className="flex items-center gap-3"
            whileHover={{ scale: 1.02 }}
            transition={{ type: "spring", stiffness: 400 }}
          >
            <div className="relative">
              <Shield className="w-10 h-10 text-cyan-400" strokeWidth={1.5} />
              <ShieldCheck className="w-5 h-5 text-purple-400 absolute -bottom-1 -right-1" />
            </div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">CyberShield</h1>
              <p className="text-xs text-slate-400">AI-Powered Content Safety</p>
            </div>
          </motion.div>
          
          <motion.div 
            className="flex items-center gap-2 text-sm text-slate-400"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            <span>System Online</span>
          </motion.div>
        </div>
      </div>
    </motion.header>
  )
}
