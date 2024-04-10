import os

from autonomous import AutoModel, log
from autonomous.tasks import AutoTasks
from config import Config
from flask import Flask, get_template_attribute, request

import tasks


def create_app():
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(Config)

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
                return f"<p>Generation Error for task#: {task.id} <br> {task.result.get('error', '')}</p>"
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
        return get_template_attribute("_components.html", "checktask")(task["id"])

    return app
