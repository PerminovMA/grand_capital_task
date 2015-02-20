__author__ = 'PerminovMA@live.ru'

from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json


def index(request):
    context = {"logged": 'auth_token' in request.session}
    return render(request, 'index.html', context)


def get_reps(request):
    """ Get a list of repositories of user in the current session.
    :return json string. Example: [{ name: "...", owner: {login: "..."}, ...}, ...]
    more info: https://developer.github.com/v3/

    """
    if 'auth_token' not in request.session:
        return redirect("/")

    headers = {'authorization': 'token %s' % request.session.get("auth_token")}
    r = requests.get('https://api.github.com/user/repos?type=owner', headers=headers)

    if r.status_code / 100 != 2:  # If HTTP status code not 2xx (Success)
        return HttpResponse("Internal Server Error.", status=r.status_code)

    return HttpResponse(r)


def get_rep_statistic(request):
    """
    :param request: contains user_name and repository name as rep_name passed via GET request.
    :return: json string. Example: [{'char': 'a', 'count': 1}, {'char': 'b', 'count': 2}]

    """
    if 'auth_token' not in request.session:
        return index(request)

    user_name = request.GET.get("user_name")
    rep_name = request.GET.get("rep_name")
    # The number of processed commit messages (default = 50)
    depth_processing = 50 if request.GET.get("depth_processing") is None else int(request.GET.get("depth_processing"))

    if not (user_name and rep_name):
        return HttpResponse("Bad Request.", status=400)

    # Request commit messages. More info: https://developer.github.com/v3/
    headers = {'authorization': 'token %s' % request.session.get("auth_token")}
    r = requests.get('https://api.github.com/repos/%s/%s/commits' % (user_name, rep_name), headers=headers)
    if r.status_code / 100 != 2:  # If HTTP status code not 2xx (Success)
        return HttpResponse("Internal Server Error.", status=r.status_code)

    commits = r.json()
    temp_dict = {}

    # count characters
    for commit in commits[:depth_processing]:
        message = commit["commit"]["message"]
        for ch in message:
            if ch in temp_dict:
                temp_dict[ch] += 1
            else:
                temp_dict[ch] = 1

    if " " in temp_dict:  # Replace the " " on "space" for convenience
        temp_dict["space"] = temp_dict[" "]
        del temp_dict[" "]

    # convert from dict {"a": 1, "b": 2} to list [{'char': 'a', 'count': 1}, {'char': 'b', 'count': 2}]
    statistic_list = [{"char": x, "count": y} for x, y in temp_dict.items()]
    statistic_list.sort(key=lambda obj: obj["count"], reverse=True)  # sort by "count"

    return HttpResponse(json.dumps(statistic_list))