import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface ATSAnalysis {
    id: string;
    overall_score: number;
    score_category: string;
    keyword_score: number;
    formatting_score: number;
    experience_score: number;
    education_score: number;
    skills_score: number;
    contact_score: number;
    strengths: string[];
    improvements: string[];
    missing_elements: string[];
    analyzed_at: string;
}

export const uploadCV = async (file: File): Promise<ATSAnalysis> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/upload-cv/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const getAnalysis = async (analysisId: string): Promise<ATSAnalysis> => {
    const response = await axios.get(`${API_BASE_URL}/analysis/${analysisId}/`);
    return response.data;
};
