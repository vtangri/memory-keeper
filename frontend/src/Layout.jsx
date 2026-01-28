import React from 'react';
import { Outlet, NavLink, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Sparkles, Heart, Compass, LayoutDashboard, MessageCircle } from 'lucide-react';

const Layout = () => {
  return (
    <div className="min-h-screen relative flex flex-col bg-pattern">
      {/* Decorative Orbs */}
      <div className="fixed top-0 left-1/4 w-[500px] h-[500px] bg-brand-200/20 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div className="fixed bottom-0 right-1/4 w-[500px] h-[500px] bg-sage-500/10 rounded-full blur-[120px] pointer-events-none animate-pulse-slow font-delay-2000"></div>

      {/* Floating Navigation */}
      <header className="sticky top-6 z-50 px-6 max-w-7xl mx-auto w-full">
        <nav className="glass py-4 px-8 rounded-[2rem] flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-12 h-12 bg-gradient-to-br from-brand-600 to-brand-400 rounded-2xl flex items-center justify-center shadow-premium group-hover:rotate-12 transition-transform duration-500">
              <Sparkles className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent leading-none">
                Memory Keeper
              </h1>
              <span className="text-[10px] font-bold tracking-[0.2em] text-sage-500 uppercase">Legacy Engine</span>
            </div>
          </Link>

          <div className="hidden md:flex items-center space-x-10">
            <NavLink to="/" className={({ isActive }) => `nav-link flex items-center space-x-2 ${isActive ? 'nav-link-active' : ''}`}>
              <MessageCircle size={18} />
              <span>Converse</span>
            </NavLink>
            <NavLink to="/dashboard" className={({ isActive }) => `nav-link flex items-center space-x-2 ${isActive ? 'nav-link-active' : ''}`}>
              <LayoutDashboard size={18} />
              <span>Exploration</span>
            </NavLink>
          </div>

          <div className="flex items-center space-x-4">
            <button className="hidden lg:flex items-center space-x-2 text-slate-400 hover:text-slate-600 transition-colors">
              <Compass size={20} />
            </button>
            <button className="w-10 h-10 rounded-full border border-slate-200 flex items-center justify-center hover:bg-white transition-all overflow-hidden shadow-sm">
              <div className="w-full h-full bg-gradient-to-br from-indigo-100 to-brand-100 flex items-center justify-center text-brand font-bold text-xs">
                SK
              </div>
            </button>
          </div>
        </nav>
      </header>

      <main className="flex-grow max-w-7xl mx-auto w-full px-6 py-12 relative z-10">
        <Outlet />
      </main>

      <footer className="py-20 bg-slate-900 text-slate-300 relative z-0 mt-20">
        <div className="max-w-7xl mx-auto px-10 grid grid-cols-1 md:grid-cols-3 gap-16">
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
               <Sparkles className="text-brand-400" size={32} />
               <h2 className="text-3xl font-bold text-white">Memory Keeper</h2>
            </div>
            <p className="text-slate-400 text-lg leading-relaxed text-balance">
              Technology bridging generations, preserving the warmth of every story ever told.
            </p>
          </div>
          
          <div className="flex flex-col space-y-4">
            <h3 className="text-white font-bold text-lg uppercase tracking-widest text-sage-500">Journey</h3>
            <Link to="/" className="hover:text-white transition-colors">Start a Story</Link>
            <Link to="/dashboard" className="hover:text-white transition-colors">Family Archive</Link>
            <Link to="/guide" className="hover:text-white transition-colors">Getting Started</Link>
          </div>

          <div className="flex flex-col space-y-4">
             <h3 className="text-white font-bold text-lg uppercase tracking-widest text-sage-500">Legacy</h3>
             <p className="text-slate-400">Join our mission to document every life story.</p>
             <div className="flex items-center space-x-2 text-rose-400 bg-rose-400/10 w-fit px-4 py-2 rounded-full font-bold text-sm">
               <Heart size={16} fill="currentColor" />
               <span>Made with Love</span>
             </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-10 mt-20 pt-10 border-t border-white/5 text-sm text-slate-500 flex justify-between items-center">
          <p>© {new Date().getFullYear()} Memory Keeper. All rights reserved.</p>
          <div className="flex space-x-6">
            <span>Privacy</span>
            <span>Terms</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
