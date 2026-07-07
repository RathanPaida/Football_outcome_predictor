'use client';

import { useState, useEffect } from 'react';

// Sub-component to fetch and display player image from Wikipedia
function PlayerCard({ name, team }: { name: string, team: string }) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    // Clean name from position
    const cleanName = name.split(' (')[0];
    const searchQuery = encodeURIComponent(cleanName);
    
    fetch(`https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&titles=${searchQuery}&pithumbsize=200&format=json&origin=*`)
      .then(res => res.json())
      .then(data => {
        const pages = data.query?.pages;
        if (pages) {
          const pageIds = Object.keys(pages);
          if (pageIds.length > 0 && pageIds[0] !== '-1') {
            const thumbnail = pages[pageIds[0]].thumbnail;
            if (thumbnail) {
              setImageUrl(thumbnail.source);
            }
          }
        }
      })
      .catch(() => {});
  }, [name, team]);

  const posMatch = name.match(/\((.*?)\)/);
  const pos = posMatch ? posMatch[1] : '';
  const cleanName = name.split(' (')[0];
  
  const nameParts = cleanName.split(' ');
  const shortName = nameParts.length > 1 ? nameParts[nameParts.length - 1] : cleanName;

  // Position colors
  const getPosColor = (p: string) => {
    if (p === 'GK') return 'bg-yellow-500 text-black';
    if (p === 'DEF') return 'bg-blue-500 text-white';
    if (p === 'MID') return 'bg-emerald-500 text-white';
    if (p === 'ATT') return 'bg-rose-500 text-white';
    return 'bg-gray-500 text-white';
  };

  return (
    <div className="flex flex-col items-center justify-center p-1 group z-20 hover:scale-125 transition-transform duration-300 ease-out cursor-pointer relative">
      <div className="w-12 h-12 md:w-16 md:h-16 rounded-full overflow-hidden bg-gradient-to-br from-gray-800 to-black border-[3px] border-white/80 shadow-[0_10px_20px_rgba(0,0,0,0.8)] flex items-center justify-center relative">
        {imageUrl ? (
          <img src={imageUrl} alt={cleanName} className="w-full h-full object-cover" />
        ) : (
          <svg className="w-6 h-6 md:w-8 md:h-8 text-white/30" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
        )}
        <div className={`absolute -bottom-0.5 -right-0.5 ${getPosColor(pos)} text-[8px] md:text-[10px] font-black px-1.5 py-0.5 rounded border border-black shadow-xl uppercase tracking-tighter`}>
          {pos}
        </div>
      </div>
      <div className="mt-2 bg-black/80 backdrop-blur-md px-2.5 py-1 rounded-md shadow-2xl border border-white/10 group-hover:border-teal-400 transition-colors">
        <span className="text-[10px] md:text-[11px] font-black text-white text-center tracking-wide uppercase shadow-black drop-shadow-md whitespace-nowrap block">
          {shortName}
        </span>
      </div>
    </div>
  );
}

// Highly Premium Football Pitch Component
function FootballPitch({ teamName, formation, players }: { teamName: string, formation: string, players: string[] }) {
  const lines = [1, ...formation.split('-').map(Number)];
  
  if (players.length !== 11) return <div className="text-white text-center p-10 bg-black/50 rounded-xl border border-red-500/50">Awaiting Gemini AI Squad Generation...</div>;

  let playerIndex = 0;
  
  return (
    <div className="flex flex-col w-full h-[650px] rounded-2xl relative overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.8)] border-[6px] border-[#d2dae2]/10 perspective-1000">
      
      {/* Premium Grass Texture (Alternating Stripes) */}
      <div className="absolute inset-0 bg-[#2b5836] bg-[repeating-linear-gradient(0deg,transparent,transparent_40px,rgba(255,255,255,0.03)_40px,rgba(255,255,255,0.03)_80px)]"></div>
      
      {/* Outer Pitch Boundary */}
      <div className="absolute inset-4 border-[3px] border-white/60"></div>
      
      {/* Halfway Line */}
      <div className="absolute top-0 bottom-0 left-1/2 w-[3px] bg-white/60 -translate-x-1/2"></div>
      
      {/* Center Circle */}
      <div className="absolute top-1/2 left-1/2 w-32 h-32 rounded-full border-[3px] border-white/60 -translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute top-1/2 left-1/2 w-2 h-2 rounded-full bg-white -translate-x-1/2 -translate-y-1/2"></div>
      
      {/* Left Penalty Area */}
      <div className="absolute top-1/2 left-4 w-32 h-64 border-[3px] border-l-0 border-white/60 -translate-y-1/2"></div>
      {/* Left Goal Area */}
      <div className="absolute top-1/2 left-4 w-12 h-24 border-[3px] border-l-0 border-white/60 -translate-y-1/2"></div>
      {/* Left Penalty Spot */}
      <div className="absolute top-1/2 left-24 w-1.5 h-1.5 rounded-full bg-white -translate-y-1/2"></div>
      {/* Left D-Box */}
      <div className="absolute top-1/2 left-[142px] w-16 h-24 border-[3px] border-l-0 border-white/60 rounded-r-full border-t-transparent border-b-transparent -translate-y-1/2 opacity-70"></div>

      {/* Right Penalty Area */}
      <div className="absolute top-1/2 right-4 w-32 h-64 border-[3px] border-r-0 border-white/60 -translate-y-1/2"></div>
      {/* Right Goal Area */}
      <div className="absolute top-1/2 right-4 w-12 h-24 border-[3px] border-r-0 border-white/60 -translate-y-1/2"></div>
      {/* Right Penalty Spot */}
      <div className="absolute top-1/2 right-24 w-1.5 h-1.5 rounded-full bg-white -translate-y-1/2"></div>
      {/* Right D-Box */}
      <div className="absolute top-1/2 right-[142px] w-16 h-24 border-[3px] border-r-0 border-white/60 rounded-l-full border-t-transparent border-b-transparent -translate-y-1/2 opacity-70"></div>

      {/* Team Badge Overlays */}
      <div className="absolute top-6 left-8 bg-black/70 px-4 py-2 rounded-lg text-white font-black text-xl backdrop-blur-md z-20 border border-white/20 shadow-xl tracking-widest uppercase">
        {teamName} <span className="text-teal-400 text-sm ml-2">{formation}</span>
      </div>

      {/* Player Rendering (Flex Rows mapped to formation lines) */}
      <div className="absolute inset-0 flex flex-col justify-between py-10 z-30">
        {lines.map((count, lineIndex) => {
          const linePlayers = players.slice(playerIndex, playerIndex + count);
          playerIndex += count;
          
          return (
            <div key={lineIndex} className="flex flex-row justify-center items-center w-full" style={{ gap: count > 3 ? '1.5rem' : '4rem' }}>
              {linePlayers.map((player, idx) => (
                <PlayerCard key={idx} name={player} team={teamName} />
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function Home() {
  const [teams, setTeams] = useState<string[]>([]);
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [isNeutral, setIsNeutral] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'score' | 'tactics' | 'lineups'>('score');

  useEffect(() => {
    fetch('http://localhost:8000/teams')
      .then(res => res.json())
      .then(data => {
        if (data.teams && data.teams.length > 0) {
          setTeams(data.teams);
        }
      })
      .catch(err => console.error("Could not fetch teams from API:", err));
  }, []);

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (homeTeam === awayTeam) {
      alert("A team cannot play against itself.");
      return;
    }

    setLoading(true);
    setResult(null);
    setActiveTab('score');

    const formData = new FormData();
    formData.append('home_team', homeTeam);
    formData.append('away_team', awayTeam);
    formData.append('is_neutral', isNeutral ? '1' : '0');

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (error: any) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8FAFC] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-50 via-[#F8FAFC] to-orange-50 flex items-center justify-center p-4 md:p-10 text-slate-800 font-sans">
      <div className="w-full max-w-7xl bg-white/80 backdrop-blur-3xl border border-blue-200/50 rounded-[2rem] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)] overflow-hidden flex flex-col relative">
        
        {/* Colorful World Cup 2026 Theme Decorative Elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-yellow-300 to-orange-500 rounded-full blur-[100px] opacity-20 -z-10 -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-full blur-[100px] opacity-20 -z-10 translate-y-1/2 -translate-x-1/2"></div>
        <div className="absolute top-1/2 left-1/2 w-[800px] h-[800px] bg-gradient-to-r from-red-400 to-pink-500 rounded-full blur-[150px] opacity-10 -z-10 -translate-x-1/2 -translate-y-1/2 pointer-events-none"></div>

        {/* Header */}
        <div className="relative p-10 text-center border-b border-gray-100 bg-white/50">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-2 bg-gradient-to-r from-blue-500 via-orange-500 to-red-500 rounded-b-full"></div>
          <h1 className="text-4xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-red-600 tracking-tighter drop-shadow-sm mb-2 uppercase">
            Predictive Intelligence
          </h1>
          <p className="text-blue-900 text-sm md:text-base font-bold tracking-[0.2em] uppercase">Powered by XGBoost & Google Gemini AI</p>
        </div>

        <div className="p-6 md:p-10 z-10">
          {/* Form */}
          <form onSubmit={handlePredict} className="space-y-8 max-w-4xl mx-auto mb-12">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              <div className="space-y-3 group">
                <label htmlFor="homeTeam" className="text-xs font-black text-blue-700 uppercase tracking-widest ml-1 drop-shadow-sm">Home Team</label>
                <div className="relative">
                  <select 
                    id="homeTeam"
                    value={homeTeam} 
                    onChange={(e) => setHomeTeam(e.target.value)}
                    required
                    className="w-full p-4 bg-white/90 border border-blue-200 rounded-2xl appearance-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all text-slate-800 font-bold text-lg shadow-sm hover:bg-white cursor-pointer"
                  >
                    <option value="" disabled className="text-gray-400">Select a country...</option>
                    {teams.map(t => <option key={t} value={t} className="text-slate-800">{t}</option>)}
                  </select>
                  <div className="absolute inset-y-0 right-0 flex items-center px-5 pointer-events-none text-blue-500">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>

              <div className="space-y-3 group">
                <label htmlFor="awayTeam" className="text-xs font-black text-orange-600 uppercase tracking-widest ml-1 drop-shadow-sm">Away Team</label>
                <div className="relative">
                  <select 
                    id="awayTeam"
                    value={awayTeam} 
                    onChange={(e) => setAwayTeam(e.target.value)}
                    required
                    className="w-full p-4 bg-white/90 border border-orange-200 rounded-2xl appearance-none focus:ring-4 focus:ring-orange-500/20 focus:border-orange-500 outline-none transition-all text-slate-800 font-bold text-lg shadow-sm hover:bg-white cursor-pointer"
                  >
                    <option value="" disabled className="text-gray-400">Select a country...</option>
                    {teams.map(t => <option key={t} value={t} className="text-slate-800">{t}</option>)}
                  </select>
                  <div className="absolute inset-y-0 right-0 flex items-center px-5 pointer-events-none text-orange-500">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="relative overflow-hidden w-full bg-gradient-to-r from-blue-600 via-purple-600 to-orange-500 hover:from-blue-500 hover:via-purple-500 hover:to-orange-400 text-white font-black text-lg py-5 rounded-2xl transition-all duration-300 shadow-[0_10px_30px_rgba(37,99,235,0.3)] hover:shadow-[0_15px_40px_rgba(249,115,22,0.4)] hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none group"
            >
              <div className="absolute inset-0 w-full h-full bg-white/10 skew-x-[-20deg] -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
              <span className="relative z-10 flex items-center justify-center gap-3 tracking-wide">
                {loading ? (
                  <>
                    <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Gemini AI is generating tactics...
                  </>
                ) : 'INITIALIZE AI ANALYSIS'}
              </span>
            </button>
          </form>

          {/* Results Display */}
          {result && !loading && (
            <div className="animate-[fadeInUp_0.5s_ease-out_forwards] w-full mx-auto">
              
              <style>{`
                @keyframes fadeInUp {
                  from { opacity: 0; transform: translateY(20px); }
                  to { opacity: 1; transform: translateY(0); }
                }
                @keyframes shimmer {
                  100% { transform: translateX(200%); }
                }
                .home-bar-width { width: ${result.probabilities.home_win}%; }
                .draw-bar-width { width: ${result.probabilities.draw}%; }
                .away-bar-width { width: ${result.probabilities.away_win}%; }
              `}</style>

              <div className="flex space-x-3 mb-10 bg-white p-2 rounded-2xl border border-gray-100 shadow-sm">
                <button onClick={() => setActiveTab('score')} className={`flex-1 py-3.5 rounded-xl text-sm font-black uppercase tracking-wider transition-all duration-300 ${activeTab === 'score' ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-md' : 'text-slate-500 hover:text-slate-800 hover:bg-gray-50'}`}>Score & Odds</button>
                <button onClick={() => setActiveTab('tactics')} className={`flex-1 py-3.5 rounded-xl text-sm font-black uppercase tracking-wider transition-all duration-300 ${activeTab === 'tactics' ? 'bg-gradient-to-r from-purple-500 to-red-500 text-white shadow-md' : 'text-slate-500 hover:text-slate-800 hover:bg-gray-50'}`}>Pundit Analysis</button>
                <button onClick={() => setActiveTab('lineups')} className={`flex-1 py-3.5 rounded-xl text-sm font-black uppercase tracking-wider transition-all duration-300 ${activeTab === 'lineups' ? 'bg-gradient-to-r from-red-500 to-orange-500 text-white shadow-md' : 'text-slate-500 hover:text-slate-800 hover:bg-gray-50'}`}>Visual Pitch</button>
              </div>

              {activeTab === 'score' && (
                <div className="space-y-8 max-w-3xl mx-auto">
                  <div className="flex items-center justify-center gap-8 w-full py-6">
                    <span className="text-blue-700 flex-1 text-right text-4xl font-black truncate uppercase tracking-tight drop-shadow-sm">{result.match.home_team}</span>
                    <div className="flex flex-col items-center justify-center shrink-0">
                      <div className="flex items-center gap-6 text-6xl font-black bg-white px-10 py-5 rounded-3xl border border-gray-200 shadow-[0_10px_30px_rgba(0,0,0,0.05)]">
                        <span className="text-blue-600">{result.probabilities.predicted_home_score}</span>
                        <span className="text-slate-300 font-light">-</span>
                        <span className="text-orange-500">{result.probabilities.predicted_away_score}</span>
                      </div>
                      <span className="text-slate-400 font-black text-xs tracking-[0.3em] uppercase mt-4">Predicted Score</span>
                    </div>
                    <span className="text-orange-600 flex-1 text-left text-4xl font-black truncate uppercase tracking-tight drop-shadow-sm">{result.match.away_team}</span>
                  </div>
                  
                  <div className="space-y-5 p-8 bg-white rounded-[2rem] border border-gray-100 shadow-[0_10px_40px_rgba(0,0,0,0.03)]">
                    <div className="group relative overflow-hidden bg-gray-50 border border-gray-100 rounded-2xl p-6 flex justify-between items-center shadow-sm">
                      <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-blue-100 to-blue-50 z-0 home-bar-width transition-all duration-[2000ms] ease-out"></div>
                      <span className="relative z-10 font-black text-blue-900 text-xl tracking-wide uppercase">{result.match.home_team} Win</span>
                      <span className="relative z-10 font-black text-4xl text-blue-600">{result.probabilities.home_win}%</span>
                    </div>
                    <div className="group relative overflow-hidden bg-gray-50 border border-gray-100 rounded-2xl p-6 flex justify-between items-center shadow-sm">
                      <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-gray-200 to-gray-100 z-0 draw-bar-width transition-all duration-[2000ms] ease-out"></div>
                      <span className="relative z-10 font-black text-gray-700 text-xl tracking-wide uppercase">Draw</span>
                      <span className="relative z-10 font-black text-4xl text-gray-600">{result.probabilities.draw}%</span>
                    </div>
                    <div className="group relative overflow-hidden bg-gray-50 border border-gray-100 rounded-2xl p-6 flex justify-between items-center shadow-sm">
                      <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-orange-100 to-orange-50 z-0 away-bar-width transition-all duration-[2000ms] ease-out"></div>
                      <span className="relative z-10 font-black text-orange-900 text-xl tracking-wide uppercase">{result.match.away_team} Win</span>
                      <span className="relative z-10 font-black text-4xl text-orange-500">{result.probabilities.away_win}%</span>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'tactics' && (
                <div className="space-y-6 max-w-4xl mx-auto">
                  <div className="bg-white border border-purple-100 rounded-3xl p-10 shadow-[0_10px_40px_rgba(0,0,0,0.05)] relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-pink-100 to-orange-100 blur-[80px] rounded-full"></div>
                    <h3 className="text-2xl font-black text-slate-800 mb-6 flex items-center gap-3 tracking-wide uppercase relative z-10">
                      <svg className="w-8 h-8 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                      Gemini Pundit Analysis
                    </h3>
                    <p className="text-slate-600 leading-loose text-lg font-medium relative z-10">
                      {result.explanation.text_explanation}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-blue-50/50 border border-blue-100 rounded-3xl p-8 shadow-sm">
                      <h4 className="font-black text-blue-700 mb-4 text-xl uppercase tracking-wider">{result.match.home_team} Strategy</h4>
                      <p className="text-base text-slate-700 leading-relaxed font-medium">{result.tactics.home.tactical_explanation.tactical_approach}</p>
                    </div>
                    <div className="bg-orange-50/50 border border-orange-100 rounded-3xl p-8 shadow-sm">
                      <h4 className="font-black text-orange-600 mb-4 text-xl uppercase tracking-wider">{result.match.away_team} Strategy</h4>
                      <p className="text-base text-slate-700 leading-relaxed font-medium">{result.tactics.away.tactical_explanation.tactical_approach}</p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'lineups' && (
                <div className="flex flex-col xl:flex-row justify-center gap-10 w-full">
                  <div className="flex-1 w-full max-w-xl mx-auto">
                    <FootballPitch 
                      teamName={result.match.home_team} 
                      formation={result.tactics.home.formation} 
                      players={result.tactics.home.starting_xi} 
                    />
                  </div>
                  <div className="flex-1 w-full max-w-xl mx-auto xl:rotate-0">
                    {/* Rotate the away pitch on large screens so they face each other */}
                    <div className="rotate-180 xl:rotate-0 h-full">
                      <FootballPitch 
                        teamName={result.match.away_team} 
                        formation={result.tactics.away.formation} 
                        players={result.tactics.away.starting_xi} 
                      />
                    </div>
                  </div>
                </div>
              )}

            </div>
          )}
        </div>
      </div>
    </main>
  );
}