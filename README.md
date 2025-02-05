Clone our repository:
git clone https://github.com/lcloud-zadanie/devops-task.git

Get Into the repo we just cloned
cd devops-task

Setup virtual environment:
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows

Install Requirements:
pip install -r requirements.txt

Run Script :
python3 upload_s3_python.py
