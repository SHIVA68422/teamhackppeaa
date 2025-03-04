from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Database Model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    exercise = db.Column(db.String(100), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Home Page - Show Enrolled Members
@app.route('/')
def index():
    members = Member.query.all()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Time Fitness</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                text-align: center;
            }}
            .container {{
                width: 50%;
                margin: 50px auto;
                background: white;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1, h2 {{
                color: #333;
            }}
            form input {{
                padding: 10px;
                margin: 10px;
                width: 40%;
            }}
            button {{
                padding: 10px;
                background: #28a745;
                color: white;
                border: none;
                cursor: pointer;
            }}
            button:hover {{
                background: #218838;
            }}
            table {{
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
            }}
            th {{
                background: #28a745;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>All Time Fitness</h1>
            
            <h2>Enroll a New Member</h2>
            <form action="/enroll" method="POST">
                <input type="text" name="name" placeholder="Enter Name" required>
                <input type="text" name="exercise" placeholder="Enter Exercise" required>
                <button type="submit">Enroll</button>
            </form>

            <h2>Enrolled Members</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Exercise</th>
                </tr>
                {"".join(f"<tr><td>{member.name}</td><td>{member.exercise}</td></tr>" for member in members)}
            </table>
        </div>
    </body>
    </html>
    """

# Add New Member
@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form['name']
    exercise = request.form['exercise']
    new_member = Member(name=name, exercise=exercise)
    db.session.add(new_member)
    db.session.commit()
    return redirect('/')

# Run the App
if _name_ == '_main_':
    app.run(debug=True)