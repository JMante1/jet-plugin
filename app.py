from flask import Flask, request
app = Flask(__name__)

# flask run --host=0.0.0.0

@app.route("/jet")
def hello():
    return render("Blah!")


def render(url):
    return url

def empty():
    pass

@app.route("/status")
def imdoingfine():
    return("I'm doing fine")

@app.route("/run", methods=["GET", "POST"])
def wrapper():
    data = request.json

    print(data['complete_sbol'])
    # Use the `requests` package to GET this URL -> it will return SBOL
    # Load this SBOL into PySBOL to manipulate and interact with
    # Build SPARQL queries and post them to <your-sbh-url>/sparql
    # Get the results back and save things to the static/ directory here

    htmlToReturn = ""
    htmlToReturn += '<img src="http://localhost:5000/static/scary-happy.jpg" />'

    something = False
    if something:
        htmlToReturn = "WOW!"

    print("Hi, I'm not broken yet")
    return htmlToReturn
