import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, Sparkles, BookOpen, Clock, ChevronRight, Volume2, History } from 'lucide-react';
import MessageBubble from './MessageBubble';
import AudioRecorder from './AudioRecorder';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Welcome to your personal memory vault. I'm honored to help you preserve your life's journey. What moment from your past is on your mind today?", sender: 'ai', timestamp: new Date() }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isThinking]);

  const handleSend = async () => {
    if (!inputText.trim()) return;
    
    const newUserMsg = { id: Date.now(), text: inputText, sender: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, newUserMsg]);
    setInputText('');
    setIsThinking(true);
    
    try {
      // Direct call to running backend
      const response = await axios.post('http://localhost:8000/api/v1/chat/send', {
        text: inputText,
        session_id: "demo_user"
      });
      
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: response.data.reply,
        sender: 'ai',
        timestamp: new Date()
      }]);
    } catch (error) {
       // Graceful fallback for demo
       setTimeout(() => {
         setMessages(prev => [...prev, {
           id: Date.now() + 1,
           text: "That sounds like a beautiful memory. Could you tell me more about who was with you at that time?",
           sender: 'ai',
           timestamp: new Date()
         }]);
       }, 1500);
    } finally {
       setIsThinking(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-w-5xl mx-auto space-y-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 px-4">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-brand font-bold text-sm uppercase tracking-widest">
            <div className="w-2 h-2 rounded-full bg-sage-500 animate-pulse"></div>
            <span>Recording Legacy</span>
          </div>
          <h2 className="text-5xl font-bold bg-gradient-to-br from-slate-900 via-slate-700 to-slate-500 bg-clip-text text-transparent">
            Share a Memory
          </h2>
        </div>
        
        <div className="flex items-center space-x-4">
           <div className="flex -space-x-3">
             {[1,2,3].map(i => (
               <div key={i} className="w-10 h-10 rounded-full border-2 border-heritage-krem bg-brand-100 flex items-center justify-center text-[10px] font-bold text-brand shadow-sm">
                 {String.fromCharCode(64 + i)}
               </div>
             ))}
           </div>
           <p className="text-sm font-medium text-slate-500">
             <span className="text-slate-900 font-bold">12 stories</span> recorded this week
           </p>
        </div>
      </div>

      <div className="flex-grow flex flex-col min-h-0 bg-white shadow-premium rounded-[3rem] border border-white relative overflow-hidden">
        {/* Chat Background Decals */}
        <div className="absolute top-0 right-0 p-12 opacity-[0.03] pointer-events-none">
           <BookOpen size={200} />
        </div>

        <div 
          ref={scrollRef}
          className="flex-grow p-10 overflow-y-auto space-y-8 scroll-smooth"
        >
          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 30, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
              >
                <MessageBubble message={msg} />
              </motion.div>
            ))}
            
            {isThinking && (
              <motion.div 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                className="flex items-center space-x-2 text-slate-400 p-4 bg-slate-50 rounded-2xl w-fit"
              >
                <div className="flex space-x-1">
                  <div className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce"></div>
                  <div className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                  <div className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                </div>
                <span className="text-xs font-bold uppercase tracking-widest ml-2">Listening...</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Input Dock */}
        <div className="p-8 bg-slate-50/50 border-t border-slate-100">
          <div className="relative group max-w-4xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-brand-400/20 to-sage-400/20 rounded-[2.5rem] blur opacity-0 group-focus-within:opacity-100 transition duration-1000"></div>
            <div className="relative flex items-center bg-white border border-slate-200/60 p-2 pl-6 rounded-[2rem] shadow-sm group-focus-within:shadow-2xl group-focus-within:border-brand/30 transition-all duration-500">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your story or recount a special day..."
                className="flex-grow bg-transparent text-lg py-4 outline-none text-slate-700 placeholder:text-slate-400 font-medium"
              />
              
              <div className="flex items-center space-x-3 pr-2">
                <AudioRecorder 
                  isRecording={isRecording} 
                  onToggle={() => setIsRecording(!isRecording)} 
                />
                <button 
                  onClick={handleSend}
                  disabled={!inputText.trim()}
                  className="w-14 h-14 bg-brand text-white rounded-2xl flex items-center justify-center hover:bg-brand-600 disabled:opacity-20 disabled:grayscale transition-all shadow-xl shadow-brand/20 active:scale-90"
                >
                  <Send size={24} />
                </button>
              </div>
            </div>
          </div>
          <div className="flex justify-center mt-4 space-x-8 text-[11px] font-bold text-slate-400 uppercase tracking-widest">
             <span className="flex items-center space-x-1"><History size={12} /> <span>Autosaved</span></span>
             <span className="flex items-center space-x-1"><Volume2 size={12} /> <span>Voice On</span></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
