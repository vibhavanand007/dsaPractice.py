import os
import time
import random
import pandas as pd
import math
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
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
    leetcode_link = request.form.get('leetcode_link', 'N/A')
    topics = request.form.get('topics', 'N/A')
    time_ = time.strftime("%Y-%m-%d %H:%M:%S")

    # Validate the input
    if not name:
        flash("No question name provided. Please add a valid question name.", 'error')
        return redirect(url_for('index'))

    # Check if the question is already in the list
    if name in df['name'].tolist():
        flash(f"The question '{name}' is already in the list.", 'warning')
    else:
        # Add the new question to the DataFrame
        new_entry = pd.DataFrame([[name, leetcode_link, topics, str(time_), 0]],
                                 columns=['name', 'leetcode_link', 'topics', 'time', 'count'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_path, index=False)
        flash(f"Question '{name}' added successfully.", 'success')

    return redirect(url_for('index'))

# Route to Display Random Questions
@app.route('/random_questions')
def random_questions():
    global df
    if df.empty:
        flash("No questions available to display.", 'info')
        return redirect(url_for('index'))

    sampled_questions = random.sample(list(df.index), min(5, len(df)))
    questions_list = []

    for index in sampled_questions:
        question_name = df.at[index, 'name']
        question_link = df.at[index, 'leetcode_link']
        question_topics = df.at[index, 'topics']
        df.at[index, 'count'] += 1
        questions_list.append({
            'name': question_name,
            'link': question_link,
            'topics': question_topics,
            'count': df.at[index, 'count']
        })

    df.to_csv(file_path, index=False)
    return render_template('random_questions.html', questions=questions_list)

# Route to Display All Questions with Pagination
@app.route('/all_questions')
def all_questions():
    global df

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Display 10 questions per page
    total_pages = math.ceil(len(df) / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_questions = df.iloc[start:end].to_dict(orient='records')

    return render_template('all_questions.html', questions=paginated_questions, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)