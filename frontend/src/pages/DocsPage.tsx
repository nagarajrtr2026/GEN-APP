import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { ChevronRight, Terminal, Copy, CheckCircle, ArrowUp, ChevronDown, Rocket, LayoutTemplate, Database, Lock, Search, BookOpen, Layers, Code, Play } from 'lucide-react';
import { GlowCard } from '../components/ui/GlowCard';
import { AnimatedButton } from '../components/ui/AnimatedButton';

const sections = [
  { id: 'intro', title: '1. Introduction', icon: <BookOpen size={18} /> },
  { id: 'how-it-works', title: '2. How It Works', icon: <Layers size={18} /> },
  { id: 'features', title: '3. Features', icon: <SparklesIcon size={18} /> },
  { id: 'architecture', title: '4. Architecture', icon: <Database size={18} /> },
  { id: 'api', title: '5. API Reference', icon: <Terminal size={18} /> },
  { id: 'examples', title: '6. Example Prompts', icon: <Code size={18} /> },
  { id: 'tech-stack', title: '7. Tech Stack', icon: <LayoutTemplate size={18} /> },
  { id: 'faq', title: '8. FAQ', icon: <Search size={18} /> },
  { id: 'start', title: '9. Get Started', icon: <Play size={18} /> },
];

function SparklesIcon({ size }: { size: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
    </svg>
  );
}

const CodeBlock = ({ title, code, method }: { title: string, code: string, method?: string }) => {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <div className="bg-dark-800 rounded-xl overflow-hidden border border-white/10 mb-6">
      <div className="flex items-center justify-between px-4 py-2 border-b border-white/5 bg-white/5">
        <div className="flex items-center gap-3">
          {method && (
            <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${method === 'POST' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>
              {method}
            </span>
          )}
          <span className="text-xs text-gray-400 font-mono">{title}</span>
        </div>
        <button onClick={handleCopy} className="text-gray-400 hover:text-white transition-colors">
          {copied ? <CheckCircle size={16} className="text-green-400" /> : <Copy size={16} />}
        </button>
      </div>
      <div className="p-4 overflow-x-auto">
        <pre className="text-sm font-mono text-accent-cyan whitespace-pre-wrap">{code}</pre>
      </div>
    </div>
  );
};

const AccordionItem = ({ question, answer }: { question: string, answer: string }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="border border-white/10 rounded-xl mb-4 overflow-hidden bg-dark-800/50 backdrop-blur-sm">
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        className="w-full flex items-center justify-between p-4 text-left hover:bg-white/5 transition-colors"
      >
        <span className="font-bold text-gray-200">{question}</span>
        <motion.div animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={20} className="text-gray-400" />
        </motion.div>
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="p-4 pt-0 text-gray-400 border-t border-white/5 mt-2">
              {answer}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export const DocsPage = () => {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState('intro');
  const [showTopBtn, setShowTopBtn] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollTop;
      const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scroll = `${totalScroll / windowHeight}`;
      setScrollProgress(Number(scroll));
      setShowTopBtn(totalScroll > 400);

      const sectionElements = sections.map(s => document.getElementById(s.id));
      let current = 'intro';
      for (const el of sectionElements) {
        if (el && totalScroll >= el.offsetTop - 200) {
          current = el.id;
        }
      }
      setActiveSection(current);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      window.scrollTo({ top: el.offsetTop - 100, behavior: 'smooth' });
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-dark-900 text-white relative">
      <div className="fixed top-0 left-0 w-full h-1 bg-white/10 z-50">
        <motion.div 
          className="h-full bg-gradient-to-r from-accent-cyan to-accent-violet" 
          style={{ width: `${scrollProgress * 100}%` }}
        />
      </div>

      <nav className="fixed top-0 w-full z-40 border-b border-white/10 bg-dark-900/80 backdrop-blur-xl h-16 flex items-center justify-between px-6">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.5)]">
            <BookOpen size={16} className="text-white" />
          </div>
          <span className="text-xl font-bold tracking-wider text-gradient">GENESIS.DOCS</span>
        </Link>
        <div className="flex items-center gap-4">
          <Link to="/dashboard">
            <button className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm font-medium transition-colors">
              Go to App
            </button>
          </Link>
        </div>
      </nav>

      <div className="flex pt-16 h-screen">
        {/* Sidebar */}
        <aside className="w-64 fixed left-0 h-[calc(100vh-4rem)] border-r border-white/10 overflow-y-auto hidden md:block bg-dark-900/50 backdrop-blur-md">
          <div className="p-6 space-y-2">
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">Contents</h4>
            {sections.map(s => (
              <button
                key={s.id}
                onClick={() => scrollTo(s.id)}
                className={`w-full flex items-center gap-3 text-left px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  activeSection === s.id ? 'bg-accent-violet/20 text-accent-cyan border border-accent-violet/30 shadow-[0_0_15px_rgba(139,92,246,0.2)]' : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <span className={activeSection === s.id ? 'text-accent-cyan' : 'text-gray-500'}>{s.icon}</span>
                {s.title}
              </button>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 md:ml-64 p-8 md:p-16 overflow-y-auto relative pb-32">
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.02] pointer-events-none mix-blend-overlay fixed" />
          
          <div className="max-w-4xl mx-auto space-y-32">
            
            {/* 1. Introduction */}
            <section id="intro" className="pt-8">
              <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                <h1 className="text-5xl font-black mb-6 tracking-tight text-gradient">Genesis AI Documentation</h1>
                <p className="text-xl text-gray-400 leading-relaxed">
                  Genesis AI is a revolutionary architectural engine that converts plain English prompts into a full, production-ready application architecture. It instantly synthesizes UI schemas, API routing, relational databases, validation constraints, and authentication rules.
                </p>
              </motion.div>
            </section>

            {/* 2. How It Works */}
            <section id="how-it-works">
              <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><Layers className="text-accent-cyan" /> How It Works</h2>
                <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-white/10 before:to-transparent">
                  {[
                    "Prompt: Describe your app in natural language.",
                    "AI Engine: Intelligent extraction of entities and intent.",
                    "System Design: Module mapping and architecture scaffolding.",
                    "Schema Generation: Detailed DB tables, relations, and APIs.",
                    "Validation: Deep consistency checking and automated repair.",
                    "Live Preview: Dynamic rendering of your app instantly."
                  ].map((step, i) => (
                    <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                       <div className="flex items-center justify-center w-10 h-10 rounded-full border border-white/10 bg-dark-800 text-accent-cyan shadow-[0_0_15px_rgba(6,182,212,0.3)] shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                         {i + 1}
                       </div>
                       <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl glass border border-white/5 hover:border-accent-cyan/30 transition-colors">
                         <p className="font-medium text-gray-200">{step}</p>
                       </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            </section>

            {/* 3. Features */}
            <section id="features">
              <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><SparklesIcon size={28} className="text-accent-cyan" /> Core Features</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {["UI Schema Generation", "API Endpoints & Validation", "Database Schema & Relations", "Auth Roles & Scopes", "Business Logic Inference", "Live Interactive Preview", "Metrics & Analytics Dashboard", "Persistent Prompt History"].map((feat, i) => (
                    <GlowCard key={i}>
                      <div className="flex items-center gap-3">
                         <div className="w-8 h-8 rounded bg-white/5 flex items-center justify-center text-accent-cyan"><CheckCircle size={16} /></div>
                         <h3 className="font-bold text-gray-200">{feat}</h3>
                      </div>
                    </GlowCard>
                  ))}
                </div>
              </motion.div>
            </section>

            {/* 4. Architecture */}
            <section id="architecture">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                 <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><Database className="text-accent-cyan" /> Architecture</h2>
                 <div className="glass p-8 rounded-3xl border border-white/10 text-center">
                    <div className="flex flex-col items-center gap-4">
                       <div className="px-8 py-4 bg-dark-800 rounded-xl border border-white/20 font-bold w-full max-w-sm">Frontend (React + Vite)</div>
                       <div className="h-8 w-px bg-gradient-to-b from-white/20 to-accent-cyan"></div>
                       <div className="px-8 py-4 bg-accent-cyan/10 text-accent-cyan rounded-xl border border-accent-cyan/30 font-bold w-full max-w-sm shadow-[0_0_30px_rgba(6,182,212,0.2)]">REST API (FastAPI)</div>
                       <div className="h-8 w-px bg-gradient-to-b from-accent-cyan to-accent-violet"></div>
                       <div className="flex flex-wrap justify-center gap-4 w-full">
                         <div className="px-8 py-4 bg-dark-800 rounded-xl border border-white/20 font-bold flex-1 max-w-xs">AI Engine (Groq / OpenAI)</div>
                         <div className="px-8 py-4 bg-dark-800 rounded-xl border border-white/20 font-bold flex-1 max-w-xs">Database (SQLite/Postgres)</div>
                       </div>
                    </div>
                 </div>
               </motion.div>
            </section>

            {/* 5. API Reference */}
            <section id="api">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                 <div className="flex items-center justify-between mb-8">
                   <h2 className="text-3xl font-bold flex items-center gap-3"><Terminal className="text-accent-cyan" /> API Reference</h2>
                   <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm font-medium transition-colors border border-white/10 flex items-center gap-2">
                     Open Swagger <ChevronRight size={16} />
                   </a>
                 </div>
                 
                 <CodeBlock 
                   method="POST"
                   title="/api/v1/generate" 
                   code={`{
  "prompt": "Build hospital app with doctors, patients, and appointments"
}`} 
                 />
                 <CodeBlock 
                   method="GET"
                   title="/api/v1/metrics" 
                   code={`// Returns system analytics
{
  "total_requests": 150,
  "success_requests": 148,
  "failed_requests": 2,
  "avg_latency": 1.25
}`} 
                 />
                 <CodeBlock 
                   method="GET"
                   title="/api/v1/history" 
                   code={`// Returns previous generations array
[
  {
    "id": 1,
    "prompt": "...",
    "output_json": "{...}"
  }
]`} 
                 />
               </motion.div>
            </section>

            {/* 6. Example Prompts */}
            <section id="examples">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                 <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><Code className="text-accent-cyan" /> Example Prompts</h2>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                   {[
                     "Build a hospital management app with doctors, patients, and billing.",
                     "Design an ecommerce platform with products, shopping carts, and order history.",
                     "Create a school administration portal for students, teachers, and attendance tracking.",
                     "Build a CRM for real estate agents with properties, clients, and appointments."
                   ].map((prompt, i) => (
                     <div key={i} className="p-6 bg-dark-800 rounded-xl border border-white/5 hover:border-accent-violet/30 transition-colors shadow-lg group">
                        <Terminal size={20} className="text-accent-violet mb-4 group-hover:text-accent-cyan transition-colors" />
                        <p className="text-gray-300 italic">"{prompt}"</p>
                     </div>
                   ))}
                 </div>
               </motion.div>
            </section>

            {/* 7. Tech Stack */}
            <section id="tech-stack">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                 <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><LayoutTemplate className="text-accent-cyan" /> Tech Stack</h2>
                 <div className="flex flex-wrap gap-4">
                   {["React 18", "TypeScript", "Tailwind CSS", "Framer Motion", "Zustand", "FastAPI", "Python 3.11", "SQLAlchemy", "Groq AI"].map((tech, i) => (
                     <span key={i} className="px-6 py-3 rounded-full bg-white/5 border border-white/10 font-medium text-gray-300 hover:bg-white/10 hover:text-white transition-colors">
                       {tech}
                     </span>
                   ))}
                 </div>
               </motion.div>
            </section>

            {/* 8. FAQ */}
            <section id="faq">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                 <h2 className="text-3xl font-bold mb-8 flex items-center gap-3"><Search className="text-accent-cyan" /> FAQ</h2>
                 <div className="max-w-3xl">
                   <AccordionItem question="Does it generate real applications?" answer="It generates the complete system architecture, schemas, API endpoints, database tables, and validation rules. It also renders a live interactive frontend preview of what the app will look like." />
                   <AccordionItem question="Can I export the code?" answer="Yes, you can copy the raw JSON architecture and use it to bootstrap your own backend, or directly plug it into your existing CI/CD pipelines." />
                   <AccordionItem question="Is authentication supported?" answer="Yes, the AI automatically infers user roles (Admin, Staff, Student) and assigns permissions based on your prompt." />
                   <AccordionItem question="Does the Live Preview work with all prompts?" answer="The Live Preview uses a dynamic rendering engine that intelligently maps abstract schemas to pre-built premium UI components like tables, forms, and animated charts." />
                 </div>
               </motion.div>
            </section>

            {/* 9. Get Started */}
            <section id="start" className="pt-16 pb-20 border-t border-white/10">
               <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center">
                 <h2 className="text-5xl font-black mb-6">Ready to Build?</h2>
                 <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">Skip the boilerplate and design your next massive software project in seconds.</p>
                 <div className="flex items-center justify-center gap-4">
                    <Link to="/dashboard">
                      <AnimatedButton className="px-10 py-5 text-xl shadow-[0_0_30px_rgba(6,182,212,0.4)]">
                         Start Generating Now
                      </AnimatedButton>
                    </Link>
                 </div>
               </motion.div>
            </section>

          </div>
        </main>
      </div>

      {/* Back to top button */}
      <AnimatePresence>
        {showTopBtn && (
          <motion.button
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            onClick={scrollToTop}
            className="fixed bottom-8 right-8 p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 transition-all z-50 shadow-[0_0_20px_rgba(0,0,0,0.5)] hover:-translate-y-1"
          >
            <ArrowUp size={24} />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
};
