import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { ArrowLeft, Calendar, Clock, Tag, Play, Pause, Download, Share2 } from 'lucide-react';

const StoryDetail = () => {
  const { id } = useParams();
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const fetchStory = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/v1/stories/${id}`);
        setStory(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch story", error);
        setLoading(false);
      }
    };
    fetchStory();
  }, [id]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-heritage-krem">
         <div className="flex space-x-2">
            <div className="w-3 h-3 bg-brand rounded-full animate-bounce"></div>
            <div className="w-3 h-3 bg-brand rounded-full animate-bounce delay-100"></div>
            <div className="w-3 h-3 bg-brand rounded-full animate-bounce delay-200"></div>
         </div>
      </div>
    );
  }

  if (!story) return <div className="text-center py-20">Story not found.</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
      <Link to="/dashboard" className="flex items-center text-slate-500 hover:text-brand transition-colors font-bold w-fit">
        <ArrowLeft size={20} className="mr-2" /> Back to Archives
      </Link>

      {/* Hero Section */}
      <div className="glass p-10 rounded-[3rem] relative overflow-hidden">
        {/* Decorative Background */}
        <div className="absolute -right-20 -top-20 w-64 h-64 bg-brand-100/50 rounded-full blur-[80px]"></div>
        
        <div className="relative z-10 space-y-6">
          <div className="flex flex-wrap gap-3">
             {story.topics.map(topic => (
               <span key={topic} className="px-4 py-1.5 bg-white/60 border border-white text-slate-600 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm">
                 {topic}
               </span>
             ))}
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-slate-900 leading-tight">
            {story.title}
          </h1>

          <div className="flex items-center gap-6 text-slate-500 font-medium pt-2">
            <div className="flex items-center gap-2">
              <Calendar size={18} className="text-brand" />
              <span>{story.date}</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={18} className="text-sage-500" />
              <span>{story.duration} recording</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content & Audio Player */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-8">
          <div className="bg-white p-10 rounded-[2.5rem] shadow-premium leading-relaxed text-lg text-slate-700 font-serif">
             <p className="first-letter:text-6xl first-letter:font-bold first-letter:float-left first-letter:mr-3 first-letter:text-brand">
               {story.content}
             </p>
          </div>
        </div>

        <div className="space-y-6">
          {/* Audio Card */}
          <div className="glass p-6 rounded-[2rem] space-y-4">
             <h3 className="font-bold text-slate-900 uppercase tracking-widest text-sm">Voice Record</h3>
             <div className="flex items-center justify-between bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
                <button 
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="w-12 h-12 bg-brand text-white rounded-full flex items-center justify-center hover:bg-brand-600 transition-colors shadow-lg shadow-brand/20"
                >
                  {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" className="ml-1" />}
                </button>
                <div className="flex-grow mx-4 h-1 bg-slate-100 rounded-full overflow-hidden">
                   <div className="h-full bg-brand w-1/3 rounded-full"></div>
                </div>
                <span className="text-xs font-bold text-slate-400">04:12</span>
             </div>
          </div>

          {/* Actions */}
          <div className="grid grid-cols-2 gap-4">
             <button className="flex flex-col items-center justify-center p-6 bg-white rounded-[2rem] shadow-sm hover:shadow-md transition-all text-slate-600 hover:text-brand border border-slate-100">
                <Download size={24} className="mb-2" />
                <span className="text-xs font-bold uppercase">Download</span>
             </button>
             <button className="flex flex-col items-center justify-center p-6 bg-white rounded-[2rem] shadow-sm hover:shadow-md transition-all text-slate-600 hover:text-brand border border-slate-100">
                <Share2 size={24} className="mb-2" />
                <span className="text-xs font-bold uppercase">Share</span>
             </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoryDetail;
