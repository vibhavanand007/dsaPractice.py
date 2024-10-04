import os
import time
import random
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
file_path = 'questions.csv'

# Initialize or load existing data
if not os.path.isfile(file_path):
    df = pd.DataFrame(columns=['name', 'leetcode_link', 'topics', 'time', 'count'])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)
    df.dropna(how='all', inplace=True)
    df = df.loc[~(df == '').all(axis=1)]
    if 'count' not in df.columns:
        df['count'] = 0
    else:
        df['count'] = df['count'].fillna(0).astype(int)

# Route to Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route to Append a Question
@app.route('/add_question', methods=['POST'])
def add_question():
    global df
    name = request.form.get('name')
    leetcode_link = request.form.get('leetcode_link', 'Na')
    topics = request.form.get('topics', 'Na')
    time_ = time.strftime("%Y-%m-%d %H:%M:%S")

    if not name:
        return "No name provided. Question not added."

    if name in df['name'].tolist():
        return f"The question '{name}' is already in the list. No update made."
    else:
        new_entry = pd.DataFrame([[name, leetcode_link, topics, str(time_), 0]],
                                 columns=['name', 'leetcode_link', 'topics', 'time', 'count'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_path, index=False)
        return redirect(url_for('index'))

# Route to Display All Questions with Pagination
@app.route('/all_questions', methods=['GET'])
def all_questions():
    global df
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of questions per page
    total_questions = df.shape[0]
    total_pages = (total_questions // per_page) + (1 if total_questions % per_page > 0 else 0)

    # Increment time field for every question access
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    questions_to_display = df.iloc[start_index:end_index].copy()
    questions_to_display['time'] = pd.to_datetime(questions_to_display['time']) + pd.DateOffset(minutes=1)

    # Save the updated time back to the CSV
    df.update(questions_to_display)
    df.to_csv(file_path, index=False)

    questions = questions_to_display.to_dict(orient='records')
    return render_template('all_questions.html', questions=questions, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)