import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUpload, FiFile } from 'react-icons/fi';

interface UploadSectionProps {
    onFileSelect: (file: File) => void;
    isLoading: boolean;
}

const UploadSection: React.FC<UploadSectionProps> = ({ onFileSelect, isLoading }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            onFileSelect(acceptedFiles[0]);
        }
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'application/msword': ['.doc']
        },
        maxSize: 5 * 1024 * 1024, // 5MB
        multiple: false,
        disabled: isLoading
    });

    return (
        <div className="glass-card p-8">
            <div className="text-center mb-6">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
                    Upload Your CV
                </h2>
                <p className="text-white/70 mt-2">
                    Get instant ATS compatibility feedback
                </p>
            </div>

            <div
                {...getRootProps()}
                className={`
          border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
          transition-all duration-300 ease-in-out
          ${isDragActive
                        ? 'border-primary-500 bg-primary-500/10 scale-105'
                        : 'border-white/30 hover:border-primary-400 hover:bg-white/5'
                    }
          ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center">
                    <div className={`
            w-20 h-20 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 
            flex items-center justify-center mb-4 transition-transform duration-300
            ${isDragActive ? 'scale-110' : 'scale-100'}
          `}>
                        {acceptedFiles.length > 0 ? (
                            <FiFile className="w-10 h-10 text-white" />
                        ) : (
                            <FiUpload className="w-10 h-10 text-white" />
                        )}
                    </div>

                    {acceptedFiles.length > 0 ? (
                        <div className="space-y-2">
                            <p className="text-white font-semibold">
                                {acceptedFiles[0].name}
                            </p>
                            <p className="text-white/60 text-sm">
                                {(acceptedFiles[0].size / 1024).toFixed(1)} KB
                            </p>
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onFileSelect(acceptedFiles[0]);
                                }}
                                disabled={isLoading}
                                className="gradient-btn mt-4"
                            >
                                {isLoading ? 'Analyzing...' : 'Analyze CV'}
                            </button>
                        </div>
                    ) : (
                        <>
                            {isDragActive ? (
                                <p className="text-xl font-semibold text-primary-400">
                                    Drop your CV here
                                </p>
                            ) : (
                                <>
                                    <p className="text-xl font-semibold text-white mb-2">
                                        Drag & drop your CV here
                                    </p>
                                    <p className="text-white/60 mb-4">
                                        or click to browse
                                    </p>
                                    <p className="text-sm text-white/50">
                                        Supports PDF and DOCX (max 5MB)
                                    </p>
                                </>
                            )}
                        </>
                    )}
                </div>
            </div>

            {acceptedFiles.length === 0 && (
                <div className="mt-6 flex items-center justify-center gap-4 text-sm text-white/50">
                    <span>✓ PDF</span>
                    <span>✓ DOCX</span>
                    <span>✓ Secure & Private</span>
                </div>
            )}
        </div>
    );
};

export default UploadSection;
