import React from 'react';
import { motion } from 'framer-motion';
import { Book, Layers, Users, TrendingUp, Calendar, ArrowRight, Play, Download, Search, Filter } from 'lucide-react';
import Timeline from './Timeline';

import { Link } from 'react-router-dom';
import axios from 'axios';

const PerspectiveCard = ({ children, className, onClick }) => (
  <motion.div 
    whileHover={{ rotateX: 2, rotateY: 2, y: -5 }}
    transition={{ type: "spring", stiffness: 400, damping: 30 }}
    className={clsx("glass rounded-[2.5rem] p-8 shadow-premium", className)}
    onClick={onClick}
  >
    {children}
  </motion.div>
);

const clsx = (...args) => args.filter(Boolean).join(' ');

const Dashboard = () => {
  const [stats, setStats] = React.useState([]);
  const [timelineEvents, setTimelineEvents] = React.useState([]);
  const [stories, setStories] = React.useState([]);

  // Icon mapping
  const iconMap = {
    "Book": Book,
    "Layers": Layers,
    "Users": Users
  };

  React.useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [storiesRes, statsRes, timelineRes] = await Promise.all([
          axios.get('http://localhost:8000/api/v1/stories'),
          axios.get('http://localhost:8000/api/v1/dashboard/stats'),
          axios.get('http://localhost:8000/api/v1/dashboard/timeline')
        ]);
        
        setStories(storiesRes.data);
        
        // Transform stats to include components
        const transformedStats = statsRes.data.map(stat => ({
            ...stat,
            icon: iconMap[stat.icon] || Book // fallback
        }));
        setStats(transformedStats);
        
        setTimelineEvents(timelineRes.data);
        
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      }
    };
    fetchDashboardData();
  }, []);


  return (
    <div className="space-y-16 animate-in fade-in slide-in-from-bottom-10 duration-1000">
      {/* Header with Search */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8 py-6">
        <div className="space-y-3">
          <h2 className="text-6xl font-bold tracking-tighter text-slate-900">Archive</h2>
          <p className="text-xl text-slate-500 font-medium">Your life's work, beautifully organized.</p>
        </div>
        
        <div className="flex items-center gap-4">
           <div className="relative group">
              <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-brand transition-colors" size={20} />
              <input 
                type="text" 
                placeholder="Search memories..."
                className="pl-16 pr-8 py-5 bg-white shadow-premium rounded-3xl outline-none w-full lg:w-96 border border-white focus:border-brand/20 transition-all font-medium"
              />
           </div>
           <button className="p-5 bg-white shadow-premium rounded-3xl text-slate-400 hover:text-brand transition-all border border-white">
              <Filter size={24} />
           </button>
        </div>
      </div>

      {/* Hero Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {stats.map((stat, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="group glass p-8 rounded-[3rem] space-y-6 hover:bg-white transition-colors"
          >
            <div className={clsx("w-16 h-16 rounded-2xl flex items-center justify-center text-white shadow-lg", stat.color)}>
              <stat.icon size={32} />
            </div>
            <div className="space-y-1">
              <p className="text-sm font-bold text-slate-400 uppercase tracking-[0.2em]">{stat.label}</p>
              <h3 className="text-5xl font-bold text-slate-900">{stat.value}</h3>
            </div>
            <div className="flex items-center text-xs font-bold text-slate-500 bg-slate-50 w-fit px-4 py-1.5 rounded-full border border-slate-100">
              <TrendingUp size={14} className="mr-2 text-sage-500" />
              {stat.trend}
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Main Content: Story Feed */}
        <div className="lg:col-span-8 space-y-10">
           <div className="flex items-center justify-between px-2">
              <h3 className="text-3xl font-bold flex items-center gap-3">
                 <Calendar className="text-brand" />
                 Recent Narratives
              </h3>
              <button className="group flex items-center gap-2 text-brand font-bold hover:gap-4 transition-all">
                 View History <ArrowRight size={18} />
              </button>
           </div>

           <div className="space-y-6">
              {stories.map((story, i) => (
                <Link to={`/story/${story.id}`} key={story.id}>
                  <PerspectiveCard className="group cursor-pointer mb-6 hover:border-brand/30 transition-colors">
                    <div className="flex flex-col md:flex-row md:items-center gap-8">
                      <div className="w-24 h-24 bg-brand-50 rounded-[2rem] flex-shrink-0 flex items-center justify-center text-brand group-hover:bg-brand group-hover:text-white transition-all duration-500 shadow-inner">
                        <Play size={40} fill="currentColor" />
                      </div>
                      <div className="flex-grow space-y-2">
                        <div className="flex items-center gap-3 text-xs font-bold uppercase tracking-widest text-slate-400">
                            <span>{story.date}</span>
                            <span className="w-1 h-1 bg-slate-200 rounded-full"></span>
                            <span>{story.duration} recorded</span>
                        </div>
                        <h4 className="text-3xl font-bold text-slate-800 group-hover:text-brand transition-colors">
                            {story.title}
                        </h4>
                        <div className="flex flex-wrap gap-2 pt-2">
                            {story.topics.map(tag => (
                              <span key={tag} className="px-4 py-1.5 bg-slate-100 text-slate-500 rounded-full text-[10px] font-bold uppercase tracking-wider">{tag}</span>
                            ))}
                        </div>
                      </div>
                      <button className="md:opacity-0 group-hover:opacity-100 p-4 rounded-2xl bg-white border border-slate-100 text-slate-400 hover:text-brand hover:border-brand/20 transition-all shadow-sm">
                        <ArrowRight size={24} />
                      </button>
                    </div>
                  </PerspectiveCard>
                </Link>
              ))}
           </div>
        </div>

        {/* Sidebar: Rich Timeline */}
        <div className="lg:col-span-4 space-y-8">
           <div className="glass p-10 rounded-[3.5rem] bg-gradient-to-b from-white to-brand-50/30 sticky top-32">
              <div className="flex items-center justify-between mb-10">
                 <h3 className="text-3xl font-bold">Heritage</h3>
                 <div className="p-3 bg-brand-50 text-brand rounded-2xl">
                    <TrendingUp size={24} />
                 </div>
              </div>

              <Timeline events={timelineEvents} />

              <div className="mt-12 p-8 bg-slate-900 rounded-[2rem] space-y-6 text-white relative overflow-hidden group">
                 <div className="absolute top-0 right-0 w-32 h-32 bg-brand/30 blur-3xl group-hover:bg-brand/50 transition-colors"></div>
                 <div className="relative space-y-4">
                    <h4 className="text-xl font-bold leading-tight">Generate your Storybook</h4>
                    <p className="text-slate-400 text-sm leading-relaxed">
                       Compile your digital narratives into a beautiful physical heirloom.
                    </p>
                    <button className="w-full py-4 bg-brand rounded-xl font-bold hover:bg-brand-600 transition-all shadow-lg shadow-brand/20">
                       Start Production
                    </button>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
