# RecoveryPro - AI-Powered Injury Recovery Tracker

RecoveryPro is a comprehensive web application that helps users track their injury recovery journey with predictive analytics and personalized insights.

## 🎯 Features

- **Injury Tracking**: Log and monitor multiple injuries
- **Smart Predictions**: AI-powered recovery timeline predictions
- **Progress Analytics**: Visual dashboards showing recovery progress
- **Exercise Logging**: Track exercises and their impact on recovery
- **Personalized Insights**: Get recommendations based on your recovery data
- **User Authentication**: Secure login and registration

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT + Bcrypt
- **ML**: Pandas, NumPy, Scikit-learn
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Charting**: Plotly (optional)
- **Routing**: React Router v6

### Deployment
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git installed

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nurasaduzzaman91-eng/recovery-pro.git
   cd recovery-pro
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost:5432/recovery_pro
uvicorn app:app --reload
```

#### Frontend
```bash
cd frontend
npm install
export REACT_APP_API_URL=http://localhost:8000/api
npm start
```

## 📊 API Endpoints

### Users
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `GET /api/users/me/{user_id}` - Get user profile

### Injuries
- `POST /api/injuries/{user_id}` - Create injury
- `GET /api/injuries/{user_id}` - Get user's injuries
- `GET /api/injuries/detail/{injury_id}` - Get injury details
- `PUT /api/injuries/{injury_id}` - Update injury
- `DELETE /api/injuries/{injury_id}` - Delete injury

### Exercises
- `POST /api/exercises/templates` - Create exercise template
- `GET /api/exercises/templates/{injury_type}` - Get exercises for injury type
- `POST /api/exercises/logs/{injury_id}` - Log exercise completion
- `GET /api/exercises/logs/{injury_id}` - Get exercise logs

### Analytics
- `GET /api/analytics/predict/{injury_id}` - Get recovery prediction
- `GET /api/analytics/injury-analytics/{injury_id}` - Get injury analytics
- `GET /api/analytics/similar-injury-stats/{injury_type}` - Get recovery stats for injury type
- `POST /api/analytics/metrics/{injury_id}` - Log progress metric

## 📈 Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- hashed_password
- full_name
- created_at

### Injuries Table
- id (Primary Key)
- user_id (Foreign Key)
- injury_type
- severity (1-10)
- description
- start_date
- expected_recovery_weeks
- created_at

### ExerciseTemplates Table
- id (Primary Key)
- injury_type
- name
- description
- recommended_frequency
- repetitions
- sets
- duration_minutes
- difficulty_level

### ExerciseLogs Table
- id (Primary Key)
- user_id (Foreign Key)
- injury_id (Foreign Key)
- exercise_id (Foreign Key)
- completed_at
- pain_level (1-10)
- difficulty (1-10)
- notes
- completed

### ProgressMetrics Table
- id (Primary Key)
- injury_id (Foreign Key)
- metric_date
- mobility_score (0-100)
- pain_score (1-10)
- exercises_completed
- range_of_motion
- swelling_level
- notes

## 🤖 ML/Prediction Features

### Recovery Timeline Prediction
- Analyzes pain trends over time
- Tracks mobility improvements
- Calculates exercise adherence
- Predicts estimated recovery date with confidence percentage

### Analytics & Insights
- Pain and mobility trend analysis
- Exercise adherence rate calculation
- Identification of best-performing exercises
- Personalized recovery recommendations

## 📝 Usage Example

1. **Register/Login**: Create an account and sign in
2. **Log Injury**: Add a new injury with details
3. **Track Progress**: Log daily progress metrics
4. **Complete Exercises**: Log exercises and pain levels
5. **View Analytics**: Check recovery predictions and insights
6. **Follow Recommendations**: Get personalized recovery suggestions

## 🔒 Security Features

- Password hashing with bcrypt
- JWT-based authentication
- CORS enabled
- SQL injection protection via SQLAlchemy ORM
- Environment variables for sensitive data

## 📱 Responsive Design

- Mobile-friendly interface
- Responsive grid layouts
- Touch-optimized buttons
- Adaptive forms

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View logs
docker-compose logs db
```

### Frontend Not Loading
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app.py`
- Verify `REACT_APP_API_URL` environment variable

## 🚀 Deployment

### Heroku Deployment

1. Create Heroku app
2. Add PostgreSQL add-on
3. Set environment variables
4. Deploy: `git push heroku main`

### Railway Deployment

1. Connect GitHub repository
2. Add PostgreSQL plugin
3. Deploy automatically

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by RecoveryPro Team**