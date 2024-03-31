import src.polls.choice.models as models
import src.polls.choice.schemas as schema

from src.actions.actions import BaseActions


class ChoiceActions(BaseActions[models.Choice, schema.CreateChoice, schema.UpdateChoice]):
    """Choice actions with basic CRUD operations"""

    pass


choice_action = ChoiceActions(models.Choice)
