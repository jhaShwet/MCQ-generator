# MCQ Generator 

MCQ Generator is a web application that lets users generate multiple-choice questions (MCQs) on a given topic, search for related topics, and submit answers. It uses FastAPI for the backend and Streamlit for the frontend.

# Tech Stack

   # Backend: https://mcq-backend-test.onrender.com

    - FastAPI: High-performance web framework for APIs.
    - Uvicorn: ASGI server for FastAPI.
    - Pydantic: Data validation and settings management.
    - Requests: HTTP library for API requests.
    - API Endpoints: Configure the requests on Postman.

      - Root Endpoint
      - Generate MCQ : curl -X POST "https://https://mcq-backend-test.onrender.com/generate/" -H "Content-Type: application/json" -d '{"topic": "Python"}'
      - Search Content : curl -X POST "https://https://mcq-backend-test.onrender.com/search/" -H "Content-Type: application/json" -d '{"topic": "Python"}'
      - Submit Answer : curl -X POST "https://mcq-backend-test.onrender.com/submit_answer/" -H "Content-Type: application/json" -d ' {"question_id": 1, "answer": "A"}'

 # Frontend: https://frontend-app5.onrender.com

   - Streamlit: Framework for interactive web applications.
   - Functionality:
      - Allows users to generate MCQs.
      - Provides a search feature for related topics.
      - Submits user answers.
        
# Database:

   - JSON File: Storage for questions and user answers.

# Hosting:

- GitHub: # https://github.com/jhaShwet/MCQ-generator/
- Render: Deployment of the application
- Generate MCQs on a given topic.
- Search for related topics.
- Submit answers.
- User-friendly interface with Streamlit.

# Prerequisites
- Python 3.8+
- pip for package management
- AI21 API key
