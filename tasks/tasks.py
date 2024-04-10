from autonomous import AutoModel, log
from models.character import Character

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


####################################################################################################
# Tasks
####################################################################################################
def _generate_task(model, pk):
    if Model := _import_model(model):
        obj = Model.get(pk)
        obj.generate()
    return {"url": "/api/components/history"}


def _generate_battlemap_task(model, pk):
    if Model := _import_model(model):
        obj = Model.get(pk)
        obj.generate_battlemap()
    return {"url": "/api/components/map"}


def _generate_image_task(model, pk):
    if Model := _import_model(model):
        obj = Model.get(pk)
        obj.generate_image()
    return {"url": "/api/components/imagemanage"}


def _generate_chat_task(pk, message):
    if Model := Character.get(pk):
        obj = Model.get(pk)
        obj.chat(message)
    return {"url": "/api/components/page/chats"}
