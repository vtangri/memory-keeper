import React from 'react';
import { motion } from 'framer-motion';

const Timeline = ({ events }) => {
  return (
    <div className="relative border-l-2 border-slate-100 ml-4 space-y-12 pb-4">
      {events.map((event, idx) => (
        <motion.div 
          key={idx} 
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ delay: idx * 0.1 }}
          className="relative pl-12 group"
        >
          {/* Circular Marker */}
          <div className="absolute -left-[11px] top-0 w-5 h-5 rounded-full bg-white border-2 border-brand group-hover:bg-brand group-hover:scale-125 transition-all duration-500 shadow-sm z-10" />
          
          <div className="space-y-2">
            <span className="text-sm font-black text-brand uppercase tracking-[0.2em]">{event.year}</span>
            <h4 className="text-xl font-bold text-slate-800 group-hover:text-brand transition-colors">
              {event.title}
            </h4>
            <p className="text-slate-500 font-medium leading-relaxed group-hover:text-slate-700 transition-colors">
              {event.desc}
            </p>
          </div>

          {/* Connective Line Decal */}
          {idx !== events.length - 1 && (
            <div className="absolute left-[-1px] top-5 w-px h-12 bg-gradient-to-b from-brand/50 to-transparent opacity-0 group-hover:opacity-100 transition-all"></div>
          )}
        </motion.div>
      ))}
    </div>
  );
};

export default Timeline;
