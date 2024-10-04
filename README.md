# DSA Questions Web Application

This web application helps users manage and view DSA (Data Structures and Algorithms) questions. It allows users to add questions, display a set of random questions, and view all questions with pagination. Built using Flask, HTML, CSS, and JavaScript, the application includes a contact info toggle button in the top-right corner for quick access to the author's details.

## Features

- **Add New Questions**: Users can input new DSA questions with details such as name, LeetCode link, and topics.
- **Random Questions**: Displays 5 random questions from the list each time the button is clicked.
- **View All Questions**: Users can view all added questions with pagination (10 questions per page).
- **Contact Info**: Hover over a three-dot icon in the top-right corner of any page to display the author's contact information.

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS for responsive design and modern styling.
- **Data Storage**: Questions are stored in a CSV file (`questions.csv`).

## Project Structure

```bash
/DSA_Web_Application
    ├── /static
    │   ├── styles.css    # Custom CSS for the project
    │   ├── script.js     # JavaScript for contact info toggle
    ├── /templates
    │   ├── index.html    # Main home page
    │   ├── random_questions.html  # Random questions page
    │   ├── all_questions.html    # Paginated view of all questions
    ├── app.py            # Main Flask app
    ├── questions.csv     # CSV file to store questions
    └── README.md         # This README file