from flask import Flask, render_template, request, redirect, url_for, send_file, session
import pandas as pd
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Ensure the upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Function to process age data
def process_age_data(filepath):
    df = pd.read_csv(filepath)

    # Define age groups
    bins = [0, 18, 35, 60, 100]
    labels = ["0-18", "19-35", "36-60", "60+"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    # Count gender distribution in each age group
    gender_counts = df.groupby(["Age Group", "Gender"]).size().unstack().fillna(0)

    # Calculate insights
    avg_age = df["Age"].mean()
    median_age = df["Age"].median()
    dominant_age_group = df["Age Group"].value_counts().idxmax()

    # Generate bar chart
    plt.figure(figsize=(8, 5))
    gender_counts.plot(kind="bar", stacked=True)
    plt.xlabel("Age Groups")
    plt.ylabel("Count")
    plt.title("Gender Distribution by Age Group")
    plt.legend(title="Gender")
    chart_path = os.path.join("static", "gender_distribution.png")
    plt.savefig(chart_path)
    plt.close()

    return gender_counts.to_html(), avg_age, median_age, dominant_age_group, chart_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            session["uploaded_file"] = file.filename
            return redirect(url_for("visualization"))

    return render_template("upload.html")

@app.route("/visualization")
def visualization():
    uploaded_file = session.get("uploaded_file")
    if not uploaded_file:
        return render_template("visualization.html", message="No data available.")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file)
    df = pd.read_csv(filepath)

    # Define age groups
    bins = [0, 18, 35, 60, 100]
    labels = ["0-18", "19-35", "36-60", "60+"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

    # Count age distribution
    age_group_counts = df["Age Group"].value_counts().sort_index()

    # Create a bar chart
    plt.figure(figsize=(8, 5))
    age_group_counts.plot(kind="bar", color=["blue", "green", "orange", "red"])
    plt.xlabel("Age Groups")
    plt.ylabel("Count")
    plt.title("Age Group Distribution")
    chart_path = os.path.join("static", "age_distribution.png")
    plt.savefig(chart_path)
    plt.close()

    return render_template("visualization.html", chart_path=chart_path)

@app.route("/analysis")
def analysis():
    uploaded_file = session.get("uploaded_file")
    if not uploaded_file:
        return render_template("analysis.html", message="No data available.")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file)
    table_html, avg_age, median_age, dominant_age_group, chart_path = process_age_data(filepath)

    return render_template(
        "analysis.html",
        table_html=table_html,
        avg_age=avg_age,
        median_age=median_age,
        dominant_age_group=dominant_age_group,
        chart_path=chart_path,
    )

@app.route("/download")
def download():
    uploaded_file = session.get("uploaded_file")
    if not uploaded_file:
        return "No file uploaded yet."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.secret_key = "your_secret_key"
    app.run(debug=True)
