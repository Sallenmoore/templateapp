from autonomous import AutoModel, log


####################################################################################################
# Tasks
####################################################################################################
def _generate_task(model, pk):
    if Model := AutoModel.load_model(model):
        obj = Model.get(pk)
        obj.generate()
    return {"url": "/api/"}


def _generate_image_task(model, pk):
    if Model := AutoModel.load_model(model):
        obj = Model.get(pk)
        obj.generate_image()
    return {"url": "/api/"}
