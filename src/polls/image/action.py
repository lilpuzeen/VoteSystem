from src.actions.actions import BaseActions
import src.polls.image.models as model
import src.polls.image.schemas as schema


class ImageActions(BaseActions[model.Image, schema.CreateImage, schema.UpdateImage]):
    """Image actions with basic CRUD operations"""

    pass


image_action = ImageActions(model.Image)
