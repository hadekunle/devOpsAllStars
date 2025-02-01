# Weather Data Collection System

## Project Overview
This project is a Weather Data Collection System that demonstrates core DevOps principles by combining:
- External API Integration (OpenWeather API)
- Cloud Storage (AWS S3)
- Version Control (Git)
- Environment Management

## Features
- Fetches real-time weather data for multiple cities
- Displays temperature (°F), humidity, and weather conditions
- Automatically stores weather data in AWS S3
- Supports multiple cities tracking
- Timestamps all data for historical tracking

## Technical Architecture
- **Language:** Python3
- **Cloud Provider:** AWS (S3)
- **External API:** OpenWeather API

```markdown
## Project Structure
weather-dashboard/
  src/
    weather_dashboard.py
    .env
  .gitignore
  requirements.txt
```

## Setup Instructions
1. Clone this repository:
```git clone command```

2. Install dependencies:
pip3 install -r requirements.txt

3. Configure environment variables (.env):
OPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name

4. Run the application:
python3 src/weather_dashboard.py


### What I Learned
- AWS S3 bucket creation and management
- Environment variable management for secure API keys
- Python best practices for API integration
- Git workflow for project development
- Error handling in distributed systems
- Cloud resource management

### Future Enhancements
- Allow users to input list of cities
- Allow user to select temperature units F or C 
- Implement data visualization
- Create automated testing
- Set up CI/CD pipeline
- Create bucket using terraform
```