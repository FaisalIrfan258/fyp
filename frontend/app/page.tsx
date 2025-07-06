'use client';

import { useState } from 'react';
import ImageUploader from '@/components/ImageUploader';
import LoadingSpinner from '@/components/LoadingSpinner';
import PredictionResult from '@/components/PredictionResult';
import apiClient, { PredictionResult as PredictionResultType } from '@/lib/api';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResultType | null>(null);
  const [uploadState, setUploadState] = useState<'idle' | 'uploading' | 'processing' | 'completed' | 'error'>('idle');

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setResult(null);
    setUploadState('idle');
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setUploadState('uploading');

      // Short delay to show the uploading state
      await new Promise(resolve => setTimeout(resolve, 500));
      setUploadState('processing');

      const result = await apiClient.predict(selectedFile);
      
      setResult(result);
      setUploadState('completed');
    } catch (err) {
      console.error('Error during prediction:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setUploadState('error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setUploadState('idle');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl mb-4">
          Brain Tumor Detection
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload a brain MRI scan image to detect the presence of tumors using our AI-powered analysis.
        </p>
      </div>

      {!result ? (
        <div className="max-w-xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <ImageUploader onImageSelected={handleImageSelected} isLoading={isLoading} />
            
            {error && (
              <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
                {error}
              </div>
            )}
            
            <div className="mt-6 flex justify-center">
              <button
                onClick={handleSubmit}
                disabled={!selectedFile || isLoading}
                className={`px-4 py-2 rounded-md ${
                  !selectedFile || isLoading
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isLoading ? 'Processing...' : 'Analyze Image'}
              </button>
            </div>
            
            {isLoading && (
              <div className="mt-6 flex justify-center">
                <div className="text-center">
                  <LoadingSpinner size="md" color="blue" />
                  <p className="mt-2 text-sm text-gray-600">
                    {uploadState === 'uploading' ? 'Uploading image...' : 'Analyzing image...'}
                  </p>
                </div>
              </div>
            )}
          </div>
          
          <div className="mt-8 bg-blue-50 border border-blue-200 p-4 rounded-md">
            <h3 className="text-sm font-medium text-blue-800 mb-2">How it works</h3>
            <p className="text-sm text-blue-700">
              Our AI model analyzes brain MRI scans to detect patterns consistent with tumors.
              The model was trained on thousands of labeled images and provides confidence scores
              to help with interpretation.
            </p>
          </div>
        </div>
      ) : (
        <PredictionResult result={result} onReset={handleReset} />
      )}
    </div>
  );
}
