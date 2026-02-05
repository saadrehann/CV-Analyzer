import React, { useEffect, useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface ScoreDisplayProps {
    score: number;
    category: string;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score, category }) => {
    const [displayScore, setDisplayScore] = useState(0);

    useEffect(() => {
        // Animate score counting up
        const duration = 2000; // 2 seconds
        const steps = 60;
        const stepValue = score / steps;
        const stepDuration = duration / steps;

        let currentStep = 0;
        const interval = setInterval(() => {
            currentStep++;
            setDisplayScore(Math.min(Math.round(currentStep * stepValue), score));

            if (currentStep >= steps) {
                clearInterval(interval);
            }
        }, stepDuration);

        return () => clearInterval(interval);
    }, [score]);

    const getScoreColor = () => {
        if (score >= 80) return { path: '#10b981', trail: '#10b98120', text: '#10b981' }; // Green
        if (score >= 65) return { path: '#3b82f6', trail: '#3b82f620', text: '#3b82f6' }; // Blue
        if (score >= 50) return { path: '#f59e0b', trail: '#f59e0b20', text: '#f59e0b' }; // Orange
        return { path: '#ef4444', trail: '#ef444420', text: '#ef4444' }; // Red
    };

    const getCategoryBadge = () => {
        if (category === 'Excellent') return 'bg-green-500';
        if (category === 'Good') return 'bg-blue-500';
        if (category === 'Fair') return 'bg-orange-500';
        return 'bg-red-500';
    };

    const colors = getScoreColor();

    return (
        <div className="glass-card p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-6">
                ATS Compatibility Score
            </h2>

            <div className="max-w-xs mx-auto mb-6">
                <CircularProgressbar
                    value={displayScore}
                    text={`${displayScore}%`}
                    styles={buildStyles({
                        pathColor: colors.path,
                        textColor: '#ffffff',
                        trailColor: colors.trail,
                        pathTransitionDuration: 0.5,
                        textSize: '20px',
                    })}
                    className="score-circle"
                />
            </div>

            <div className="flex items-center justify-center gap-2 mb-4">
                <span className={`${getCategoryBadge()} px-4 py-2 rounded-full text-white font-semibold text-lg`}>
                    {category}
                </span>
            </div>

            <p className="text-white/70 text-sm">
                {score >= 80 && "Outstanding! Your CV is highly optimized for ATS systems."}
                {score >= 65 && score < 80 && "Great job! Your CV should pass most ATS systems."}
                {score >= 50 && score < 65 && "Good start. Consider the improvements below to boost your score."}
                {score < 50 && "Your CV needs work. Follow the recommendations to improve ATS compatibility."}
            </p>
        </div>
    );
};

export default ScoreDisplay;
