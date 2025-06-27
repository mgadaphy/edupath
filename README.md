# React + TypeScript# EduPath - Your Guide to Academic and Career Success in Cameroon

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/mgadaphy/edupath)](https://github.com/mgadaphy/edupath/issues)
[![GitHub stars](https://img.shields.io/github/stars/mgadaphy/edupath)](https://github.com/mgadaphy/edupath/stargazers)

EduPath is an AI-powered educational guidance system designed to help Cameroonian students make informed decisions about their academic and career paths. The system provides personalized recommendations for university programs and career paths based on students' academic performance, interests, and job market trends.

## Features

- 🎓 Personalized university program recommendations
- 💼 Career path suggestions based on academic performance
- 🏫 Comprehensive database of Cameroonian universities and programs
- 📊 Job market insights and employment trends
- 🎯 Career assessment and skill matching
- 📱 Responsive design for all devices

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite 4.x
- Radix UI Components
- Tailwind CSS
- React Router v6
- Axios for API communication

### Backend
- FastAPI
- PostgreSQL
- Redis
- Neo4j
- Google Agent Development Kit (ADK)

### DevOps
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Google Cloud Platform (GCP)

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm
- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mgadaphy/edupath.git
   cd edupath
   ```

2. Start the development environment:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development

### Frontend Development

To run the frontend in development mode:

```bash
cd edupath-frontend
pnpm install
pnpm run dev
```

### Backend Development

To run the backend services:

```bash
docker-compose up -d postgres redis neo4j
cd edupath-backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Project Structure

```
edupath/
├── edupath-backend/         # FastAPI backend
├── edupath-frontend/        # React frontend
├── docker-compose.yml       # Docker Compose configuration
├── README.md               # This file
└── CHANGELOG.md            # Project changelog
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the [MIT License](https://opensource.org/license/MIT) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google ADK (GitHub)](https://github.com/google/adk-python) and [Google Vertex AI Agent Development Kit](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart) for the agent development framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend library
- [Radix UI](https://www.radix-ui.com/) for accessible UI components

## Contact

For any questions or feedback, please open an issue or contact the maintainers.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```
