from flask import Flask,request,render_template
from gemini import generate_readme_material
from gitapi import fetch_repo_metadata, extract_owner_repo

app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generate_readme",methods=['POST'])
def generate_readme():
    repo_url=request.form['repo_url']
    owner,repo=extract_owner_repo(repo_url)
    metadata=fetch_repo_metadata(owner,repo)

    genai_response=generate_readme_material(metadata['repo_name'],
                                            metadata['repo_url'],
                                            metadata['repo_description'],
                                            metadata['language'],
                                            metadata['topics'],
                                            metadata['stars'],
                                            metadata['license_name'],
                                            metadata['files'])

    return render_template("readme.html",readme=genai_response)

if __name__=="__main__":
    app.run(debug=True)