import requests
from flask import Blueprint, redirect, render_template, request, session, url_for

from autonomous import AutoModel, log
from autonomous.auth import AutoAuth, auth_required

index_page = Blueprint("index", __name__)

models = {
    "player": "Character",
    "player_faction": "Faction",
    "poi": "POI",
}  # add model names that cannot just be be titlecased from lower case, such as POI or 'player':Character


def _import_model(model):
    if model:
        model_name = models.get(model, model.title())
        if Model := AutoModel.load_model(model_name):
            return Model
    return None


@index_page.route("/", endpoint="index", methods=("GET",))
@auth_required()
def index():
    context = {
        "user": AutoAuth.current_user().pk,
    }
    return render_template("index.html", context=context)


@index_page.route("/<string:model>/<string:pk>", methods=("GET",))
def detail(model, pk):
    if Model := _import_model(model):
        if obj := Model.get(pk):
            user = AutoAuth.current_user()
            log(user)
            context = {
                "user": user.pk,
                "title": obj.name,
                "model": obj.model_name().lower(),
                "pk": obj.pk,
                "world": obj.get_world().pk,
            }
            return render_template("detail.html", user=user, context=context)
    else:
        log(f"Model {model}:{pk} not found")
        return redirect(url_for("index.index"))


@index_page.route(
    "/api/<path:rest_path>",
    endpoint="api",
    methods=(
        "GET",
        "POST",
    ),
)
@auth_required(guest=True)
def api(rest_path):
    url = f"http://api:5000/{rest_path}"

    log(url, request.json)
    response = requests.post(url, json=request.json)
    # log(response.text)
    return response.text


@index_page.route("/task/<path:rest_path>", endpoint="tasks", methods=("POST",))
@auth_required()
def tasks(rest_path):
    # if request.method == "GET":
    #     return redirect(url_for("index.index"))
    # else:
    url = f"http://tasks:5000/{rest_path}"
    # log(url, request.json)
    # with httpx.Client() as client:
    response = requests.post(url, json=request.json)
    # log(response.text)
    return response.text
