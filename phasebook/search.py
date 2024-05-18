from flask import Blueprint, request
import re
from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return {"results": search_users(request.args.to_dict())}, 200


def search_users(args):
    """
    Search users database based on the provided query parameters.
    
    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string
    
    Returns:
        a list of users that match the search parameters, sorted by match priority
    """
    
    id_query = args.get('id')
    name_query = args.get('name', "").lower()
    age_query = args.get('age')
    occupation_query = args.get('occupation', "").lower()

    def matches(user):
        if id_query and user['id'] == id_query:
            return True
        if name_query and name_query in user['name'].lower():
            return True
        if age_query:
            age_range = range(int(age_query) - 1, int(age_query) + 2)
            if user['age'] in age_range:
                return True
        if occupation_query and occupation_query in user['occupation'].lower():
            return True
        return False

    def match_priority(user):
        priority = 0
        if id_query and user['id'] == id_query:
            priority -= 4
        if name_query and name_query in user['name'].lower():
            priority -= 3
        if age_query:
            age_range = range(int(age_query) - 1, int(age_query) + 2)
            if user['age'] in age_range:
                priority -= 2
        if occupation_query and occupation_query in user['occupation'].lower():
            priority -= 1
        return priority

    matched_users = [user for user in USERS if matches(user)]
    matched_users.sort(key=match_priority)

    return matched_users
