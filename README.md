# Algorithm Atlas Comparison App

This app allows you to compare various machine learning algorithms using the lazypredict library. It provides a user-friendly interface to upload a CSV dataset, set parameters, and visualize the performance of different models.

## Features

- Upload a CSV dataset or use the built-in example datasets (Diabetes and California Housing)
- Specify the data split ratio and random seed for reproducibility
- View dataset dimensions and variable details
- Compare the performance of multiple machine learning algorithms
- Visualize model performance metrics (R-squared, RMSE, and calculation time) using bar plots
- Download the training and test set predictions as CSV files
- Download the performance plots as PDF files

## Requirements

To run this app, you need to have the following dependencies installed:

- Python 3.x
- streamlit
- pandas
- base58
- numpy
- pillow
- plotly
- scikit-learn
- lazypredict
- seaborn
- matplotlib
- xgboost
- lightgbm
- pytest
- tqdm
- shap
- lime
- joblib
- scipy

You can install the required packages by running the following command:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

```
git clone https://github.com/AbhiSingh378/stoneCap.git
```

2. Navigate to the project directory:

```
cd stoneCap
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Run the Streamlit app:

```
streamlit run app.py
```

5. Access the app in your web browser at `http://localhost:8501`

6. Upload a CSV dataset or use the example datasets
7. Set the desired parameters (data split ratio and random seed)
8. Explore the dataset and view its details
9. Compare the performance of different machine learning algorithms
10. Visualize the model performance metrics using bar plots
11. Download the training and test set predictions as CSV files
12. Download the performance plots as PDF files

## Example Datasets

The app includes two example datasets:

1. Diabetes Dataset: This dataset is used to predict the progression of diabetes based on various physiological measures.

2. California Housing Dataset: This dataset is used to predict the median house value based on various features such as population, median income, and housing median age.

You can use these datasets to test the functionality of the app and explore different machine learning algorithms.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
```

And here's the `requirements.txt` file:

```
streamlit
pandas
base58
numpy
pillow
plotly
scikit-learn
lazypredict
seaborn
matplotlib
xgboost
lightgbm
pytest
tqdm
shap
lime
joblib
scipy
```