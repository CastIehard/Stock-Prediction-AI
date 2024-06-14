# Stock Prediction AI

Stock Prediction AI is a proof-of-concept program designed to demonstrate that the stock market is not entirely unpredictable. This program downloads stock data for specified stocks and uses machine learning to predict the stock's performance (in terms of percentage change) for the next day. It employs seven different AI models to provide insights and validate predictions.

## Features

- **Data Acquisition**: Automatically downloads daily stock data for specified stocks that are listed in the tracked_stocks.csv file.
- **Data Preprocessing**: Cleans and prepares the data for machine learning models.
- **Machine Learning Models**: Utilizes seven distinct machine learning models to predict next-day stock percentage changes.
- **Comparison of Models**: Compares the performance of each model to determine the most accurate prediction method.
- **Visual Analytics**: Provides visualizations of the predictions compared to actual performance for easy analysis.

## Automated Workflow
A GitHub Actions workflow is set up to automatically run the program every day at 01:00 a.m. The workflow downloads the latest stock data, trains the models, and generates predictions for the next day. The results are then pushed to the repository for review.

## Installation

To set up and run Stock Prediction AI, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-github-username/Stock-Prediction-AI.git
   cd Stock-Prediction-AI
   ```

2. **Environment Setup**
   - It's recommended to use a virtual environment to manage dependencies:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

3. **Install Dependencies**
   - Install the required Python packages using:
     ```bash
     pip install -r requirements.txt
     ```

## How It Works

The program follows these steps:

1. **Data Collection**: Downloads historical stock data from sources like Yahoo Finance.
2. **Data Preprocessing**: Cleans and prepares the data for machine learning models.
3. **Model Training**: Trains seven different models on historical data to learn patterns.
4. **Prediction**: Each model predicts the percentage change of the stock's price for the next day.
5. **Output**: The predictions are displayed and compared to actual changes using plots.

## Contributing

Contributions to Stock Prediction AI are welcome. Please feel free to fork the repository, make improvements, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Luca Burghard**

For any questions, suggestions, or contributions, please contact me at your-email@example.com.

## Support

For support, please open an issue on the GitHub repository page.