'use client';

import { useState } from 'react';
import Image from 'next/image';
import { PredictionResult } from '@/lib/api';
import apiClient from '@/lib/api';

interface PredictionResultProps {
  result: PredictionResult;
  onReset: () => void;
}

export default function PredictionResult({ result, onReset }: PredictionResultProps) {
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [comment, setComment] = useState('');
  
  const { prediction, image_info, image_url, prediction_id } = result;
  const { class: predictionClass, confidence, probability, processing_time } = prediction;
  
  // Determine color based on prediction and confidence
  const getColorClass = () => {
    if (predictionClass === 'no_tumor') {
      return 'bg-green-100 border-green-500 text-green-700';
    } else if (confidence >= 0.6) {
      return 'bg-red-100 border-red-500 text-red-700';
    } else {
      return 'bg-yellow-100 border-yellow-500 text-yellow-700';
    }
  };
  
  const getConfidenceBarColor = () => {
    if (predictionClass === 'no_tumor') {
      return 'bg-green-500';
    } else if (confidence >= 0.6) {
      return 'bg-red-500';
    } else {
      return 'bg-yellow-500';
    }
  };
  
  const handleFeedbackSubmit = async (isCorrect: boolean) => {
    try {
      setIsSubmitting(true);
      await apiClient.submitFeedback(prediction_id, isCorrect, comment);
      setFeedbackSubmitted(true);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="w-full max-w-3xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-4 sm:p-6">
        <div className="flex flex-col sm:flex-row gap-6">
          {/* Image */}
          <div className="sm:w-1/2">
            <div className="relative w-full h-64 bg-gray-100 rounded-lg overflow-hidden">
              <Image
                src={`${process.env.NEXT_PUBLIC_API_URL}${image_url}`}
                alt="Uploaded MRI scan"
                fill
                className="object-contain"
              />
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Original size: {image_info.original_size[0]} x {image_info.original_size[1]} px
            </div>
          </div>
          
          {/* Results */}
          <div className="sm:w-1/2">
            <div className={`p-4 border rounded-lg ${getColorClass()}`}>
              <h3 className="text-lg font-semibold mb-1">
                {predictionClass === 'tumor' ? 'Tumor Detected' : 'No Tumor Detected'}
              </h3>
              <p className="text-sm mb-4">
                {predictionClass === 'tumor' 
                  ? 'The model has detected patterns consistent with a brain tumor in this scan.'
                  : 'The model did not detect patterns consistent with a brain tumor in this scan.'
                }
              </p>
              
              <div className="mb-4">
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Confidence: {(confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className={`h-2.5 rounded-full ${getConfidenceBarColor()}`}
                    style={{ width: `${confidence * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="text-xs space-y-1">
                <p>Processing time: {processing_time.toFixed(3)} seconds</p>
                <p>Raw probability: {(probability * 100).toFixed(2)}%</p>
              </div>
            </div>
            
            {/* Feedback section */}
            {!feedbackSubmitted ? (
              <div className="mt-4 p-4 border border-gray-200 rounded-lg">
                <h4 className="text-sm font-medium mb-2">Was this prediction accurate?</h4>
                <div className="flex gap-2 mb-3">
                  <button
                    onClick={() => handleFeedbackSubmit(true)}
                    disabled={isSubmitting}
                    className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded hover:bg-green-200 disabled:opacity-50"
                  >
                    Yes
                  </button>
                  <button
                    onClick={() => handleFeedbackSubmit(false)}
                    disabled={isSubmitting}
                    className="px-3 py-1 bg-red-100 text-red-800 text-sm rounded hover:bg-red-200 disabled:opacity-50"
                  >
                    No
                  </button>
                </div>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Additional comments (optional)"
                  className="w-full p-2 text-sm border border-gray-300 rounded"
                  rows={2}
                />
              </div>
            ) : (
              <div className="mt-4 p-4 border border-green-200 bg-green-50 rounded-lg text-green-800">
                Thank you for your feedback!
              </div>
            )}
          </div>
        </div>
        
        <div className="mt-6 flex justify-center">
          <button
            onClick={onReset}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Analyze Another Image
          </button>
        </div>
      </div>
      
      <div className="bg-gray-50 px-4 py-3 text-xs text-gray-500">
        <p>
          Disclaimer: This is an AI-assisted analysis and should not replace professional medical diagnosis.
          Always consult with a healthcare professional for medical advice.
        </p>
      </div>
    </div>
  );
} 