import os

from config import Config
from flask import Flask, get_template_attribute, request

import tasks
from autonomous import AutoModel, log
from autonomous.tasks import AutoTasks

models = {
    "player": "Character",
    "player_faction": "Faction",
    "poi": "POI",
}  # add model names that cannot just be be titlecased from lower case, such as POI or 'player':Character


def _import_model(model):
    model_name = models.get(model, model.title())
    if Model := AutoModel.load_model(model_name):
        return Model
    return None


def create_app():
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(Config)

    # # Configure Extensions
    # if app.config["DEBUG"]:
    #     app.jinja_env.add_extension("jinja2.ext.debug")

    # Configure Routes
    @app.route(
        "/checktask/<taskid>",
        methods=(
            "GET",
            "POST",
        ),
    )
    def checktask(taskid):
        log(taskid)
        if task := AutoTasks().get_task(taskid):
            log(task.status, task.return_value, task.id)
            if task.status == "finished":
                return get_template_attribute("_components.html", "completetask")(
                    url=task.return_value.get("url"),
                )
            elif task.status == "failed":
                return f"Generation Error for task#: {task.id} <br> {task.result.get('error', '')}"
            else:
                return get_template_attribute("_components.html", "checktask")(task.id)
        else:
            return "No task found"

    @app.route("/generate", methods=("POST",))
    def generate():
        task = (
            AutoTasks()
            .task(
                tasks._generate_task,
                model=request.json.get("model"),
                pk=request.json.get("pk"),
            )
            .result
        )
        log(task)
        return get_template_attribute("_components.html", "checktask")(task["id"])

    @app.route("/generate/image", methods=("POST",))
    def image_generate_task():
        task = (
            AutoTasks()
            .task(
                tasks._generate_image_task,
                model=request.json.get("model"),
                pk=request.json.get("pk"),
            )
            .result
        )
        log(task)
        return get_template_attribute("_components.html", "checktask")(task["id"])

    @app.route("/generate/battlemap", methods=("POST",))
    def create_battlemap():
        task = (
            AutoTasks()
            .task(
                tasks._generate_battlemap_task,
                model=request.json.get("model"),
                pk=request.json.get("pk"),
            )
            .result
        )
        log(task)
        return get_template_attribute("_components.html", "checktask")(task["id"])

    @app.route("/generate/chat", methods=("POST",))
    def create_chat():
        task = (
            AutoTasks()
            .task(
                tasks._generate_chat_task,
                pk=request.json.get("pk"),
                message=request.json.get("message"),
            )
            .result
        )
        log(task)
        return get_template_attribute("_components.html", "checktask")(task["id"])

    return app
