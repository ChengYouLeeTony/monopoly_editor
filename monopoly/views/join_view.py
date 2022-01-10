from django.shortcuts import render
from django.views import View
from monopoly.models import Profile, Map
import re

class JoinView(View):
    template_name = 'join_view.html'

    def get(self, request, *args, **kwargs):
        print("request.path:", request.path)
        user = request.user
        host_name = kwargs.get('host_name', user.username)
        map_id = kwargs.get('map_id', None)
        request.session['latest_map_id'] = map_id
        _map = Map.objects.get(id = map_id)
        background_img_url = _map.backgroundsetting.background_img_url
        """for viewer mode"""
        hash_code = user.password.split("$")[-1]
        hash_code_clean = re.sub("[^A-Za-z0-9]", "", hash_code)
        viewer_url = "viewer/" + hash_code_clean + "/" + map_id

        try:
            profile = Profile.objects.get(user=user)
        except Exception:
            profile = None

        context = {
            "user": {
                "name": user.username,
                "avatar": profile.avatar.url if profile else ""
            },
            "host_name": host_name if len(host_name) else user.username,
            "map_id": map_id,
            "background_img_url": background_img_url,
            "viewer_url": viewer_url
        }

        return render(request, self.template_name, context=context)
