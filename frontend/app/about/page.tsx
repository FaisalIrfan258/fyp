import React from 'react';

export default function About() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl mb-4">
          About Brain Tumor Detection
        </h1>
        <p className="text-lg text-gray-600">
          Understanding our AI-powered brain tumor detection technology
        </p>
      </div>

      <div className="prose prose-blue mx-auto">
        <section className="mb-12">
          <h2>How It Works</h2>
          <p>
            Our brain tumor detection system uses deep learning technology to analyze MRI (Magnetic Resonance Imaging) scans
            of the brain. The system is designed to identify patterns and abnormalities that may indicate the presence of a tumor.
          </p>
          <p>
            The core of our system is a convolutional neural network (CNN) based on the ResNet18 architecture, which has been
            trained on thousands of labeled MRI scans. This model has learned to recognize the visual patterns associated with
            various types of brain tumors.
          </p>
        </section>

        <section className="mb-12">
          <h2>The Technology</h2>
          <p>
            Our system utilizes the following technologies:
          </p>
          <ul>
            <li><strong>Deep Learning Framework:</strong> PyTorch</li>
            <li><strong>Model Architecture:</strong> Modified ResNet18</li>
            <li><strong>Image Processing:</strong> OpenCV and PIL</li>
            <li><strong>Backend:</strong> FastAPI</li>
            <li><strong>Frontend:</strong> Next.js and React</li>
          </ul>
          <p>
            The model processes images through multiple convolutional layers, extracting increasingly complex features
            that help distinguish between healthy brain tissue and tumor tissue.
          </p>
        </section>

        <section className="mb-12">
          <h2>Understanding Results</h2>
          <p>
            When you upload an MRI scan, our system provides the following information:
          </p>
          <ul>
            <li><strong>Prediction:</strong> Whether a tumor is detected or not</li>
            <li><strong>Confidence Score:</strong> How confident the model is in its prediction (0-100%)</li>
            <li><strong>Processing Time:</strong> How long the analysis took</li>
          </ul>
          <p>
            <strong>Color Coding:</strong>
          </p>
          <ul>
            <li><span className="text-green-600">Green</span> indicates "No Tumor Detected"</li>
            <li><span className="text-red-600">Red</span> indicates "Tumor Detected" with high confidence</li>
            <li><span className="text-yellow-600">Yellow</span> indicates "Tumor Detected" with lower confidence</li>
          </ul>
        </section>

        <section className="mb-12">
          <h2>Important Disclaimer</h2>
          <p className="text-red-600 font-medium">
            This application is for demonstration purposes only and is not intended for clinical use.
          </p>
          <p>
            The predictions made by this system should not be used for diagnosis, treatment decisions, or any medical purpose.
            Always consult with qualified healthcare professionals for medical advice and proper diagnosis.
          </p>
        </section>

        <section className="mb-12">
          <h2>Feedback</h2>
          <p>
            Your feedback helps improve our system. After each prediction, you can indicate whether the result seems accurate
            and provide additional comments. This information will be used to refine and improve the model over time.
          </p>
        </section>

        <section>
          <h2>Technical Details</h2>
          <p>
            For developers and researchers interested in the technical aspects of our system:
          </p>
          <ul>
            <li>The model uses a modified ResNet18 architecture with custom fully connected layers</li>
            <li>Images are preprocessed to 224x224 pixels and normalized</li>
            <li>The system runs on CPU, making it accessible without specialized hardware</li>
            <li>The API is built with FastAPI, providing asynchronous request handling</li>
            <li>All predictions are stored in a database for analysis and improvement</li>
          </ul>
        </section>
      </div>
    </div>
  );
} 