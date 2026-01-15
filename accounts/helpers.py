from collections import defaultdict
from interactions.models import Reaction


def get_reaction_map(posts):
    """
    Returns a dictionary:
        { post_id: {reaction_key: count, ...}, ... }
    """
    reaction_map = {}

    # Get all reactions for the posts in one query
    reactions = Reaction.objects.filter(post__in=posts)

    # Initialize all posts with empty dict
    for post in posts:
        reaction_map[post.id] = {}

    for reaction in reactions:
        if reaction.post_id not in reaction_map:
            reaction_map[reaction.post_id] = {}
        reaction_map[reaction.post_id][reaction.reaction] = (
            reaction_map[reaction.post_id].get(reaction.reaction, 0) + 1
        )

    return reaction_map


def get_user_reactions(user, posts):
    """
    Returns a dictionary:
        { post_id: reaction_key, ... }
    """
    user_reactions = {}
    if not user.is_authenticated:
        return user_reactions

    reactions = Reaction.objects.filter(post__in=posts, user=user)
    for reaction in reactions:
        user_reactions[reaction.post_id] = reaction.reaction

    return user_reactions

def get_reaction_counts(post):
    """ Returns a dictionary of reaction counts for a given post:
        { reaction_key: count, ... }
    """
    reaction_counts = defaultdict(int)
    reactions = Reaction.objects.filter(post=post)

    for reaction in reactions:
        reaction_counts[reaction.reaction] += 1

    return dict(reaction_counts)
