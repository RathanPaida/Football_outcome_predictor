'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [teams, setTeams] = useState<string[]>([]);
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [isNeutral, setIsNeutral] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Fetch the list of teams from the dedicated JSON API endpoint
  useEffect(() => {
    // UPDATED URL: Changed to localhost
    fetch('http://localhost:8000/teams')
      .then(res => res.json()) // Parse the response directly as JSON
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

    const formData = new FormData();
    formData.append('home_team', homeTeam);
    formData.append('away_team', awayTeam);
    formData.append('is_neutral', isNeutral ? '1' : '0');

    try {
      // UPDATED URL: Changed to localhost
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
    <main className="min-h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-gray-900 via-purple-950 to-black flex items-center justify-center p-6 text-slate-200">
      <div className="w-full max-w-2xl bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-[0_8px_32px_0_rgba(0,0,0,0.6)] overflow-hidden">
        
        {/* Header */}
        <div className="relative p-10 pb-6 text-center overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent pointer-events-none"></div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 via-purple-400 to-orange-400 tracking-tight drop-shadow-sm">
            Match Predictor AI
          </h1>
          <p className="text-slate-400 mt-3 text-lg font-medium tracking-wide">Powered by XGBoost & Historical Data</p>
        </div>

        <div className="p-8 pt-4">
          <form onSubmit={handlePredict} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              {/* Home Team */}
              <div className="space-y-3 group">
                <label htmlFor="homeTeam" className="text-xs font-bold text-teal-400 uppercase tracking-widest ml-1 group-focus-within:text-teal-300 transition-colors">
                  Home Team
                </label>
                <div className="relative">
                  <select 
                    id="homeTeam"
                    title="Select the home team"
                    aria-label="Select the home team"
                    value={homeTeam} 
                    onChange={(e) => setHomeTeam(e.target.value)}
                    required
                    className="w-full p-4 bg-white/5 border border-white/10 rounded-xl appearance-none focus:ring-2 focus:ring-teal-400 focus:border-transparent outline-none transition-all text-white font-medium shadow-inner hover:bg-white/10 cursor-pointer"
                  >
                    <option value="" disabled className="bg-gray-900 text-gray-400">Select a country...</option>
                    {teams.length > 0 ? (
                      teams.map(t => <option key={t} value={t} className="bg-gray-800 text-white">{t}</option>)
                    ) : (
                      <>
                        <option value="Argentina" className="bg-gray-800 text-white">Argentina</option>
                        <option value="France" className="bg-gray-800 text-white">France</option>
                        <option value="Brazil" className="bg-gray-800 text-white">Brazil</option>
                        <option value="England" className="bg-gray-800 text-white">England</option>
                      </>
                    )}
                  </select>
                  <div className="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none text-white/50">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>

              {/* Away Team */}
              <div className="space-y-3 group">
                <label htmlFor="awayTeam" className="text-xs font-bold text-orange-400 uppercase tracking-widest ml-1 group-focus-within:text-orange-300 transition-colors">
                  Away Team
                </label>
                <div className="relative">
                  <select 
                    id="awayTeam"
                    title="Select the away team"
                    aria-label="Select the away team"
                    value={awayTeam} 
                    onChange={(e) => setAwayTeam(e.target.value)}
                    required
                    className="w-full p-4 bg-white/5 border border-white/10 rounded-xl appearance-none focus:ring-2 focus:ring-orange-400 focus:border-transparent outline-none transition-all text-white font-medium shadow-inner hover:bg-white/10 cursor-pointer"
                  >
                    <option value="" disabled className="bg-gray-900 text-gray-400">Select a country...</option>
                    {teams.length > 0 ? (
                      teams.map(t => <option key={t} value={t} className="bg-gray-800 text-white">{t}</option>)
                    ) : (
                      <>
                        <option value="Argentina" className="bg-gray-800 text-white">Argentina</option>
                        <option value="France" className="bg-gray-800 text-white">France</option>
                        <option value="Brazil" className="bg-gray-800 text-white">Brazil</option>
                        <option value="England" className="bg-gray-800 text-white">England</option>
                      </>
                    )}
                  </select>
                  <div className="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none text-white/50">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Checkbox */}
            <label htmlFor="isNeutral" className="group flex items-center space-x-4 cursor-pointer p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all shadow-sm w-fit mx-auto md:mx-0">
              <div className="relative flex items-center justify-center">
                <input 
                  id="isNeutral"
                  title="Toggle neutral venue"
                  aria-label="Toggle neutral venue"
                  type="checkbox" 
                  checked={isNeutral}
                  onChange={(e) => setIsNeutral(e.target.checked)}
                  className="peer appearance-none w-6 h-6 border-2 border-white/20 rounded bg-white/5 checked:bg-purple-500 checked:border-purple-500 focus:ring-2 focus:ring-purple-400 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all cursor-pointer"
                />
                <svg className="absolute w-4 h-4 text-white opacity-0 peer-checked:opacity-100 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <span className="font-medium text-slate-300 group-hover:text-white transition-colors">Match played at a neutral venue</span>
            </label>

            <button 
              type="submit" 
              disabled={loading}
              className="relative overflow-hidden w-full bg-gradient-to-r from-teal-500 via-purple-500 to-orange-500 hover:from-teal-400 hover:via-purple-400 hover:to-orange-400 text-white font-bold py-4 rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(168,85,247,0.4)] hover:shadow-[0_0_30px_rgba(168,85,247,0.6)] hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              <div className="absolute inset-0 w-full h-full bg-white/20 skew-x-[-20deg] -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
              <span className="relative z-10 flex items-center justify-center gap-2">
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Data...
                  </>
                ) : 'Generate Prediction'}
              </span>
            </button>
          </form>

          {/* Results Display */}
          {result && (
            <div className="mt-10 pt-8 border-t border-white/10 animate-[fadeInUp_0.5s_ease-out_forwards] opacity-0 translate-y-4">
              
              <style>{`
                @keyframes fadeInUp {
                  from { opacity: 0; transform: translateY(20px); }
                  to { opacity: 1; transform: translateY(0); }
                }
                @keyframes shimmer {
                  100% { transform: translateX(200%); }
                }
                .home-bar-width { width: ${result.home_win_prob}%; }
                .draw-bar-width { width: ${result.draw_prob}%; }
                .away-bar-width { width: ${result.away_win_prob}%; }
              `}</style>

              <div className="text-center mb-10">
                <div className="flex items-center justify-center gap-4 md:gap-8 w-full max-w-lg mx-auto">
                  <span className="text-teal-400 drop-shadow-md flex-1 text-right text-xl md:text-2xl font-bold truncate" title={result.home_team}>{result.home_team}</span>
                  
                  <div className="flex flex-col items-center justify-center shrink-0">
                    <div className="flex items-center gap-4 text-4xl md:text-5xl font-black bg-white/10 px-6 py-3 rounded-2xl border border-white/20 shadow-[0_0_20px_rgba(255,255,255,0.1)]">
                      <span className="text-teal-300 drop-shadow-lg">{result.predicted_home_score}</span>
                      <span className="text-slate-600 text-3xl font-light">-</span>
                      <span className="text-orange-300 drop-shadow-lg">{result.predicted_away_score}</span>
                    </div>
                    <span className="text-slate-400 font-semibold text-[10px] tracking-[0.2em] uppercase mt-3">Predicted Score</span>
                  </div>
                  
                  <span className="text-orange-400 drop-shadow-md flex-1 text-left text-xl md:text-2xl font-bold truncate" title={result.away_team}>{result.away_team}</span>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="group relative overflow-hidden bg-white/5 border border-white/10 rounded-2xl p-5 flex justify-between items-center shadow-lg hover:border-teal-400/50 transition-colors">
                  <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-teal-500/20 to-teal-400/40 z-0 home-bar-width transition-all duration-[1500ms] ease-out shadow-[0_0_15px_rgba(45,212,191,0.5)]"></div>
                  <span className="relative z-10 font-bold text-teal-100 tracking-wide text-lg">{result.home_team} Win</span>
                  <span className="relative z-10 font-black text-3xl text-teal-400 drop-shadow-md">{result.home_win_prob}%</span>
                </div>

                <div className="group relative overflow-hidden bg-white/5 border border-white/10 rounded-2xl p-5 flex justify-between items-center shadow-lg hover:border-slate-400/50 transition-colors">
                  <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-slate-600/30 to-slate-500/50 z-0 draw-bar-width transition-all duration-[1500ms] ease-out shadow-[0_0_15px_rgba(148,163,184,0.3)]"></div>
                  <span className="relative z-10 font-bold text-slate-200 tracking-wide text-lg">Draw</span>
                  <span className="relative z-10 font-black text-3xl text-slate-300 drop-shadow-md">{result.draw_prob}%</span>
                </div>

                <div className="group relative overflow-hidden bg-white/5 border border-white/10 rounded-2xl p-5 flex justify-between items-center shadow-lg hover:border-orange-400/50 transition-colors">
                  <div className="absolute left-0 top-0 bottom-0 bg-gradient-to-r from-orange-500/20 to-orange-400/40 z-0 away-bar-width transition-all duration-[1500ms] ease-out shadow-[0_0_15px_rgba(251,146,60,0.5)]"></div>
                  <span className="relative z-10 font-bold text-orange-100 tracking-wide text-lg">{result.away_team} Win</span>
                  <span className="relative z-10 font-black text-3xl text-orange-400 drop-shadow-md">{result.away_win_prob}%</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}