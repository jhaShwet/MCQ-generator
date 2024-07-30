# MCQ-generator

MCQ Generator is a web application that lets users generate multiple-choice questions (MCQs) on a given topic, search for related topics, and submit answers. It uses FastAPI for the backend and Streamlit for the frontend.

# Tech Stack

-Backend:
  - FastAPI: High-performance web framework for APIs.
  - Uvicorn: ASGI server for FastAPI.
  - Pydantic: Data validation and settings management.
  - Requests: HTTP library for API requests.

- Frontend:
  - Streamlit: Framework for interactive web applications.

- APIs:
  - AI21: Generates MCQs.
  - DuckDuckGo: Searches for related topics.

- Database:
  - JSON File: Storage for questions and user answers.

- Hosting:
  - GitHub: Repository management.
  - Streamlit Cloud: Deploys the Streamlit app.
  - **Heroku/AWS/DigitalOcean**: For FastAPI deployment.

# Features

- Generate MCQs on a given topic.
- Search for related topics.
- Submit answers.
- User-friendly interface with Streamlit.


## Prerequisites

- Python 3.8+
- `pip` for package management
- AI21 API key
- Basic Git and GitHub knowledge
