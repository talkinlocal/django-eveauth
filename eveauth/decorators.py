from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(raise_exception=False, *group_names):
    """Requuires user membership at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        if raise_exception:
            raise PermissionDenied
        return False

    return user_passes_test(in_groups)

def multigroup_required(raise_exception=False, *group_names):
    """Requires user membership in ALL of the groups passed in."""

    def in_all_groups(u):
        gmap = dict((gname, False) for gname in group_names)
        if u.is_authenticated():
            if u.is_superuser:
                return True

            for gname in gmap.keys():
                gmap[gname] = bool(u.groups.filter(name__iexact=gname))

            for gname in gmap.keys():
                if not gmap[gname]:
                    if raise_exception:
                        raise PermissionDenied
                    return False

            return True

    return user_passes_test(in_all_groups)
