import React from 'react';
import { FiCheckCircle, FiAlertCircle, FiXCircle } from 'react-icons/fi';

interface DetailedFeedbackProps {
    keywordScore: number;
    formattingScore: number;
    experienceScore: number;
    educationScore: number;
    skillsScore: number;
    contactScore: number;
    strengths: string[];
    improvements: string[];
    missingElements: string[];
}

interface CategoryScoreProps {
    name: string;
    score: number;
    weight: string;
}

const CategoryScore: React.FC<CategoryScoreProps> = ({ name, score, weight }) => {
    const getColor = () => {
        if (score >= 80) return 'bg-green-500';
        if (score >= 65) return 'bg-blue-500';
        if (score >= 50) return 'bg-orange-500';
        return 'bg-red-500';
    };

    return (
        <div className="mb-4">
            <div className="flex justify-between items-center mb-2">
                <span className="text-white font-medium">{name}</span>
                <span className="text-white/60 text-sm">{weight}</span>
            </div>
            <div className="flex items-center gap-3">
                <div className="flex-1 bg-white/10 rounded-full h-3 overflow-hidden">
                    <div
                        className={`${getColor()} h-full rounded-full transition-all duration-1000 ease-out`}
                        style={{ width: `${score}%` }}
                    />
                </div>
                <span className="text-white font-semibold w-12 text-right">{score}%</span>
            </div>
        </div>
    );
};

const DetailedFeedback: React.FC<DetailedFeedbackProps> = ({
    keywordScore,
    formattingScore,
    experienceScore,
    educationScore,
    skillsScore,
    contactScore,
    strengths,
    improvements,
    missingElements,
}) => {
    return (
        <div className="glass-card p-8 space-y-8">
            <div>
                <h2 className="text-2xl font-bold text-white mb-6">
                    Detailed Analysis
                </h2>

                <div className="space-y-4">
                    <CategoryScore name="Keyword Optimization" score={keywordScore} weight="25%" />
                    <CategoryScore name="Formatting & Structure" score={formattingScore} weight="20%" />
                    <CategoryScore name="Experience Relevance" score={experienceScore} weight="20%" />
                    <CategoryScore name="Education & Certifications" score={educationScore} weight="15%" />
                    <CategoryScore name="Skills Match" score={skillsScore} weight="15%" />
                    <CategoryScore name="Contact Information" score={contactScore} weight="5%" />
                </div>
            </div>

            {strengths.length > 0 && (
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <FiCheckCircle className="text-green-500 w-6 h-6" />
                        <h3 className="text-xl font-semibold text-white">Strengths</h3>
                    </div>
                    <ul className="space-y-2">
                        {strengths.map((strength, index) => (
                            <li key={index} className="flex items-start gap-3 text-white/80">
                                <span className="text-green-500 mt-1">✓</span>
                                <span>{strength}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {improvements.length > 0 && (
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <FiAlertCircle className="text-orange-500 w-6 h-6" />
                        <h3 className="text-xl font-semibold text-white">Recommendations</h3>
                    </div>
                    <ul className="space-y-2">
                        {improvements.map((improvement, index) => (
                            <li key={index} className="flex items-start gap-3 text-white/80">
                                <span className="text-orange-500 mt-1">→</span>
                                <span>{improvement}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {missingElements.length > 0 && (
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <FiXCircle className="text-red-500 w-6 h-6" />
                        <h3 className="text-xl font-semibold text-white">Missing Elements</h3>
                    </div>
                    <ul className="space-y-2">
                        {missingElements.map((element, index) => (
                            <li key={index} className="flex items-start gap-3 text-white/80">
                                <span className="text-red-500 mt-1">✗</span>
                                <span>{element}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default DetailedFeedback;
