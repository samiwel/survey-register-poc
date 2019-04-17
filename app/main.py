from flask import Flask, render_template, jsonify, request, redirect, url_for, abort
from app.datastore import InMemoryDatastore
from app.models import Version

app = Flask(__name__)

db = InMemoryDatastore()


@app.route("/questionnaire/create")
def create_questionnaire():
    return render_template("questionnaire-create.html")


@app.route("/questionnaire/create", methods=["POST"])
def post_create_questionnaire():

    questionnaire_name = request.form["name"]
    form_type = request.form["form_type"]
    created_by = request.form["created_by"]

    db.create_questionnaire(questionnaire_name, form_type, created_by)

    return redirect(url_for("get_questionnaire", questionnaire_name=questionnaire_name))


@app.route("/questionnaire/<string:questionnaire_name>/version/create")
def create_version(questionnaire_name):
    return render_template("version-create.html", questionnaire_name=questionnaire_name)


@app.route("/questionnaire/<string:questionnaire_name>/versions", methods=["POST"])
def post_create_version(questionnaire_name):

    id = request.form["id"]
    form_type = request.form["form_type"]
    created_by = request.form["created_by"]
    lang = request.form["lang"]
    variant = request.form["variant"]
    description = request.form["description"]

    db.create_version(
        questionnaire_name,
        Version(id, form_type, {}, created_by, lang, variant, description),
    )

    return redirect(url_for("get_questionnaire", questionnaire_name=questionnaire_name))


@app.route("/questionnaire/<string:questionnaire_name>/version/<string:version_id>")
def get_version(questionnaire_name, version_id):
    return jsonify(db.get_version(questionnaire_name, version_id))


@app.route("/questionnaire/<string:questionnaire_name>")
def get_questionnaire(questionnaire_name):

    if not questionnaire_name:
        return abort(404)

    questionnaire = db.get_questionnaire_by_name(questionnaire_name)

    return render_template("questionnaire.html", questionnaire=questionnaire)


@app.route("/latest")
def latest():
    latest_versions = db.get_latest_versions()

    return jsonify(latest_versions)


@app.route("/")
def home():
    return render_template("index.html")


app.run("0.0.0.0", 9950, debug=True)
