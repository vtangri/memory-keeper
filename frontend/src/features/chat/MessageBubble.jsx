import React from 'react';
import { User, Sparkles, Volume2, Bookmark, Heart } from 'lucide-react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

const MessageBubble = ({ message }) => {
  const isAi = message.sender === 'ai';

  return (
    <div className={clsx(
      "flex w-full group",
      isAi ? "justify-start" : "justify-end"
    )}>
      <div className={clsx(
        "flex max-w-[80%] items-start gap-4",
        !isAi && "flex-row-reverse"
      )}>
        {/* Avatar with Glow */}
        <div className="relative flex-shrink-0 mt-1">
          {isAi && (
            <div className="absolute inset-0 bg-brand-400 blur-lg opacity-40 animate-pulse"></div>
          )}
          <div className={clsx(
            "relative w-12 h-12 rounded-2xl flex items-center justify-center shadow-lg transform transition-transform group-hover:scale-110 duration-500",
            isAi ? "bg-white border border-slate-100" : "bg-brand gradient-br"
          )}>
            {isAi ? <Sparkles size={22} className="text-brand" /> : <User size={22} className="text-white" />}
          </div>
        </div>

        {/* Bubble Structure */}
        <div className="flex flex-col space-y-2">
          <div className={clsx(
            "relative px-8 py-5 rounded-[2rem] text-lg font-medium leading-[1.6]",
            isAi 
              ? "bg-white text-slate-700 shadow-sm border border-slate-100 rounded-tl-none font-normal" 
              : "bg-brand text-white shadow-premium rounded-tr-none"
          )}>
            {message.text}
            
            {/* Bubble Corner Decor */}
            <div className={clsx(
              "absolute top-0 w-8 h-8 pointer-events-none",
              isAi ? "-left-4 text-white" : "-right-4 text-brand"
            )}>
               <svg viewBox="0 0 100 100" className="w-full h-full fill-currentColor">
                 <path d={isAi ? "M100 0 L100 100 Q100 0 0 0 Z" : "M0 0 L0 100 Q0 0 100 0 Z"} />
               </svg>
            </div>
          </div>

          {/* Message Actions */}
          <div className={clsx(
            "flex items-center space-x-4 px-2 py-1 opacity-0 group-hover:opacity-100 transition-all duration-300",
            !isAi && "flex-row-reverse space-x-reverse"
          )}>
            <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
            {isAi && (
              <div className="flex items-center space-x-4">
                <button className="flex items-center space-x-1.5 text-[11px] font-bold text-slate-400 hover:text-brand transition-colors">
                  <Volume2 size={14} /> <span>Listen</span>
                </button>
                <button className="flex items-center space-x-1.5 text-[11px] font-bold text-slate-400 hover:text-sage-500 transition-colors">
                  <Bookmark size={14} /> <span>Save</span>
                </button>
              </div>
            )}
            {!isAi && (
               <button className="flex items-center space-x-1.5 text-[11px] font-bold text-slate-400 hover:text-rose-400 transition-colors">
                 <Heart size={14} /> <span>Favorite</span>
               </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
