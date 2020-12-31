from django.shortcuts import redirect


def logout_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index_page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper
