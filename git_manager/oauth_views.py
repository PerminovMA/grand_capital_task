__author__ = 'PerminovMA@live.ru'

import uuid
from django.http import Http404, HttpResponse
from tools import get_access_token
from requests import Request
from django.shortcuts import redirect
from gc_task.settings import GITHUB_APP_ID, AUTH_GITHUB_SCOPE, GITHUB_AUTH_URL


def github_auth_connect(request):
    """ Redirect users to request GitHub access.
    more info: developer.github.com/v3/oauth/    (see step 1)

    """

    # Generate random string. It is used to protect against cross-site request forgery attacks.
    state = uuid.uuid4().get_hex()
    request.session['github_auth_state'] = state
    params = {'client_id': GITHUB_APP_ID, 'scope': AUTH_GITHUB_SCOPE, 'state': state}
    req_url = Request('GET', url=GITHUB_AUTH_URL, params=params).prepare().url
    return redirect(req_url)


def github_auth_callback(request):
    """ If the user accepts github_auth_connect request, GitHub redirects back here
    with a code parameter and a state parameter, they can be exchanged for access_token.
    more info: developer.github.com/v3/oauth/    (see step 2)

    """
    original_state = request.session.get('github_auth_state')
    if not original_state:
        raise Http404
    del (request.session['github_auth_state'])

    state = request.GET.get('state')
    code = request.GET.get('code')

    if not state or not code:
        return HttpResponse("Error: Bad Request.", status=400)

    if original_state != state:  # It is used to protect against cross-site request forgery attacks.
        raise Http404

    access_token = get_access_token(code)  # Exchange code on access_token
    request.session['auth_token'] = access_token
    return redirect("/")


def log_out(request):
    if 'auth_token' in request.session:
        request.session.clear()
    return redirect("/")