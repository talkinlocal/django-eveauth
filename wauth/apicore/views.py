from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    u = request.user
    return render_to_response('auth/index.html', {'user': u, 'user_profile': u.get_profile()})
