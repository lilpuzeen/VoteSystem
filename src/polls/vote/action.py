import src.polls.vote.models as models
import src.polls.vote.schemas as schema

from src.actions.actions import BaseActions


class VoteActions(BaseActions[models.Vote, schema.CreateVote, schema.UpdateVote]):
    """Vote actions with basic CRUD operations"""

    pass


vote_action = VoteActions(models.Vote)