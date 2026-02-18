# Symptoms-Based Disease Prediction Using Machine Learning With Chat Bot

This is a web application that predicts diseases based on symptoms provided by the user. It leverages Machine Learning algorithms (Random Forest, Naive Bayes, Decision Tree, Voting Classified) and includes a chatbot interface. The system also supports doctor and patient management features such as registration, appointment booking, and doctor ratings.

## Features

- **Disease Prediction:** Users can select multiple symptoms to receive a predicted disease diagnosis.
- **Chatbot:** An interactive chatbot to assist users (`/chat1`).
- **Machine Learning Evaluations:** Visualizations comparing the performance (Accuracy, Precision, Recall, F1-Score) of different ML models used.
- **Doctor Portal:**
    -   Registration and Login.
    -   Manage appointments (Accept/Reject).
    -   View patient details.
-   **Patient Portal:**
    -   Registration and Login.
    -   Search for doctors by specialization and location.
    -   Book appointments.
    -   View appointment status.
    -   Rate doctors.
-   **Admin Panel:** Manage doctors and patients.

## Tech Stack

-   **Backend:** Python, Flask
-   **Frontend:** HTML, CSS, JavaScript (Bootstrap/Custom)
-   **Database:** MySQL
-   **Machine Learning:** Scikit-learn, Pandas, NumPy
-   **Visualization:** Matplotlib

## Prerequisites

-   Python 3.x
-   MySQL Server

## Structure

-   `index.py`: Main Flask application file.
-   `DBConnection.py`: Handles database connection.
-   `ML_Evaluations.py`: Script for training and evaluating ML models.
-   `disease_detection.py`: Logic for predicting diseases based on symptoms.
-   `symptoms_list.py`: Contains the list of symptoms used in the application.
-   `database.sql`: SQL dump file for setting up the database.
-   `templates/`: HTML templates for the web interface.
-   `static/`: Static files (CSS, JS, Images).

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ganeshareti/Symptoms-Based-Disease-Prediction-Using-Machine-Learning-With-Chat-Bot.git
    cd Symptoms-Based-Disease-Prediction-Using-Machine-Learning-With-Chat-Bot
    ```

2.  **Install Dependencies:**
    Install the required Python packages:
    ```bash
    pip install flask mysql-connector-python pandas numpy scikit-learn matplotlib pillow
    ```

3.  **Database Setup:**
    -   Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin).
    -   Create a new database named `disease_prediction`.
    -   Import the `database.sql` file into the `disease_prediction` database.
    -   Update the database credentials in `DBConnection.py` if necessary:
        ```python
        # DBConnection.py
        database = mysql.connector.connect(host="localhost", user="root", passwd="your_password", db="disease_prediction")
        ```

4.  **Run the Application:**
    ```bash
    python index.py
    ```

5.  **Access the App:**
    Open your web browser and navigate to: `http://127.0.0.1:5000/`

## Usage

-   **Home Page:** General information about disease prediction.
-   **Register/Login:** Navigate to the Patient or Doctor tabs to register or log in.
-   **Prediction:** Go to the prediction page, select symptoms from the list, and submit to get a prediction.
-   **Admin:** Access via `/admin` (Default credentials often `admin`/`admin` based on code review).

