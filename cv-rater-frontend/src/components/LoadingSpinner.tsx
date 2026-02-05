import React from 'react';

const LoadingSpinner: React.FC = () => {
    return (
        <div className="flex flex-col items-center justify-center p-12">
            <div className="relative w-24 h-24">
                {/* Outer ring */}
                <div className="absolute inset-0 border-4 border-primary-500/30 rounded-full"></div>
                {/* Spinning ring */}
                <div className="absolute inset-0 border-4 border-transparent border-t-primary-500 border-r-secondary-500 rounded-full animate-spin"></div>
                {/* Inner dot */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-6 h-6 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full animate-pulse"></div>
                </div>
            </div>
            <p className="mt-6 text-lg font-medium text-white/80 animate-pulse">
                Analyzing your CV...
            </p>
            <p className="mt-2 text-sm text-white/60">
                This may take a few moments
            </p>
        </div>
    );
};

export default LoadingSpinner;
