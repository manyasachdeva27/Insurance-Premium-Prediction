# Insurance Premium Prediction

A machine learning project that predicts insurance premiums based on user input factors such as BMI, age group, lifestyle risk, city tier, income, and occupation. The project includes a FastAPI web application for real-time predictions and a Jupyter notebook for model development.

## Features

- **Machine Learning Model**: Trained model for predicting insurance premiums using regression techniques.
- **FastAPI Web App**: RESTful API for making predictions via HTTP requests.
- **Health Check Endpoint**: Monitor the status and version of the deployed model.
- **Docker Support**: Containerized application for easy deployment.
- **Jupyter Notebook**: Interactive notebook for data exploration, preprocessing, and model training.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/insurance-premium-prediction.git
   cd insurance-premium-prediction
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv myenv
   # On Windows
   myenv\Scripts\activate
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the FastAPI Application

1. Activate the virtual environment (if not already activated).
2. Run the application:
   ```bash
   python app.py
   ```
3. The API will be available at `http://localhost:8000`.

### API Endpoints

- **GET /**: Home page with a simple text response.
- **GET /health**: Health check endpoint returning the model status and version.
- **POST /predict**: Predict insurance premium based on user input.

#### Example Prediction Request

Send a POST request to `/predict` with JSON data:

```json
{
  "bmi": 25.0,
  "age_group": "30-40",
  "lifestyle_risk": "medium",
  "city_tier": "tier1",
  "income_lpa": 10.0,
  "occupation": "salaried"
}
```

Response:
```json
{
  "response": 15000.0
}
```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t insurance-prediction .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 insurance-prediction
   ```

### Model Building

The `Model_building.ipynb` notebook contains the steps for:
- Data loading and exploration
- Data preprocessing
- Feature engineering
- Model training and evaluation
- Saving the trained model

To run the notebook:
1. Install Jupyter:
   ```bash
   pip install jupyter
   ```
2. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
3. Open `Model_building.ipynb` and execute the cells.

## Project Structure

- `app.py`: Main FastAPI application.
- `main.py`: Alternative entry point (if needed).
- `Model_building.ipynb`: Jupyter notebook for model development.
- `insurance.csv`: Dataset used for training.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration.
- `config/`: Configuration files (e.g., city tiers).
- `model/`: Prediction logic and model files.
- `schema/`: Pydantic schemas for input and response.
- `patients.json`: Sample data or test cases.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.