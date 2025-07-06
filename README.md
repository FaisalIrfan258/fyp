# Brain Tumor Detection Web Application

A full-stack web application for brain tumor detection using a pre-trained PyTorch model. The application allows users to upload brain MRI images and receive AI-powered predictions about tumor presence.

## Technical Stack

- **Frontend**: Next.js 14 with TypeScript
- **Backend**: Python FastAPI
- **AI/ML**: PyTorch (CPU inference)
- **Database**: PostgreSQL
- **File Storage**: Local filesystem
- **Styling**: Tailwind CSS
- **Image Processing**: Pillow (PIL), OpenCV

## Project Structure

```
brain-tumor-detection/
├── frontend/                 # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   ├── public/
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── uploads/
│   ├── model_files/
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Create a database named `brain_tumor_detection`
   - Update the database connection string in `.env` if needed

6. Copy the example environment file:
   ```bash
   copy env.example .env
   ```

7. Start the backend server:
   ```bash
   python main.py
   ```

The backend will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with the following content:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000.

## Features

- **Upload Interface**: Drag-and-drop image upload with preview
- **Prediction Display**: Clear visualization of results with confidence scores
- **History Page**: View past predictions with filtering
- **About Page**: Information about the model and usage
- **Responsive Design**: Mobile-friendly interface

## API Endpoints

- `POST /api/predict` - Upload an image and get tumor prediction
- `GET /api/predictions` - Get prediction history with pagination
- `GET /api/health` - Health check endpoint
- `POST /api/feedback` - Submit feedback on predictions

## Development Guidelines

- Use TypeScript for type safety
- Follow proper error handling practices
- Write comprehensive logs
- Use ESLint and Prettier for code formatting
- Follow the project structure

## License

MIT 