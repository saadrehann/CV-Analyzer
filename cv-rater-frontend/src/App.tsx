import React, { useState } from 'react';
import { uploadCV } from './services/api';
import type { ATSAnalysis } from './services/api';
import UploadSection from './components/UploadSection';
import LoadingSpinner from './components/LoadingSpinner';
import ScoreDisplay from './components/ScoreDisplay';
import DetailedFeedback from './components/DetailedFeedback';
import './index.css';

function App() {
    const [isLoading, setIsLoading] = useState(false);
    const [analysis, setAnalysis] = useState<ATSAnalysis | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = async (file: File) => {
        setIsLoading(true);
        setError(null);

        try {
            const result = await uploadCV(file);
            setAnalysis(result);
        } catch (err: any) {
            console.error('Error uploading CV:', err);
            setError(err.response?.data?.error || 'Failed to analyze CV. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => {
        setAnalysis(null);
        setError(null);
    };

    return (
        <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-5xl md:text-6xl font-extrabold mb-4">
                        <span className="bg-gradient-to-r from-primary-400 via-secondary-400 to-accent-400 bg-clip-text text-transparent">
                            AI-Powered CV Rater
                        </span>
                    </h1>
                    <p className="text-xl text-white/70 max-w-2xl mx-auto">
                        Get instant feedback on your CV's ATS compatibility and improve your chances of landing interviews
                    </p>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="glass-card p-4 mb-8 border-l-4 border-red-500">
                        <div className="flex items-center gap-3">
                            <span className="text-red-500 text-2xl">⚠</span>
                            <div>
                                <p className="text-white font-semibold">Error</p>
                                <p className="text-white/70">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Main Content */}
                {!analysis ? (
                    <div className="max-w-2xl mx-auto">
                        <UploadSection onFileSelect={handleFileSelect} isLoading={isLoading} />
                        {isLoading && (
                            <div className="mt-8">
                                <LoadingSpinner />
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="space-y-8">
                        {/* Reset Button */}
                        <div className="flex justify-center">
                            <button
                                onClick={handleReset}
                                className="glass-card px-6 py-3 text-white font-semibold hover:bg-white/20 transition-all duration-300"
                            >
                                ← Analyze Another CV
                            </button>
                        </div>

                        {/* Results Grid */}
                        <div className="grid lg:grid-cols-2 gap-8">
                            <div>
                                <ScoreDisplay
                                    score={analysis.overall_score}
                                    category={analysis.score_category}
                                />
                            </div>
                            <div>
                                <DetailedFeedback
                                    keywordScore={analysis.keyword_score}
                                    formattingScore={analysis.formatting_score}
                                    experienceScore={analysis.experience_score}
                                    educationScore={analysis.education_score}
                                    skillsScore={analysis.skills_score}
                                    contactScore={analysis.contact_score}
                                    strengths={analysis.strengths}
                                    improvements={analysis.improvements}
                                    missingElements={analysis.missing_elements}
                                />
                            </div>
                        </div>

                        {/* Tips Section */}
                        <div className="glass-card p-8">
                            <h3 className="text-2xl font-bold text-white mb-4">
                                💡 Pro Tips for ATS Optimization
                            </h3>
                            <div className="grid md:grid-cols-2 gap-6 text-white/80">
                                <div>
                                    <h4 className="font-semibold text-white mb-2">Use Keywords</h4>
                                    <p className="text-sm">Include relevant industry keywords and skills from the job description.</p>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-2">Simple Formatting</h4>
                                    <p className="text-sm">Stick to standard fonts and avoid complex layouts or graphics.</p>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-2">Quantify Achievements</h4>
                                    <p className="text-sm">Use numbers and metrics to demonstrate your impact.</p>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-2">Standard Sections</h4>
                                    <p className="text-sm">Include clear sections: Experience, Education, Skills, Contact.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Footer */}
                <div className="mt-16 text-center text-white/50 text-sm">
                    <p>Powered by AI • Secure & Private • No Data Stored</p>
                </div>
            </div>
        </div>
    );
}

export default App;
