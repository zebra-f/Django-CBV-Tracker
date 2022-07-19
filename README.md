# About:

- ### cbv-tracker is a simple Python package (used as a `class` decorator) that works alongside Django's Class Based Views by `printing` method names in order that they were called by Django to process `HTTP request` in `views.py`
  ##### Side note: it can be used with any Python's `class` (not exclusive to Django's Class Based Views)

---

# Installation:

- ### Requirements:

  - Python 3

        pip install cbv-tracker

---

# How to use:

- #### import `cbv_tracker`

      from cbv_tracker import cbv_tracker

- #### decorate Django's Class View (or any other class)

      from cbv_tracker import cbv_tracker


      @cbv_tracker()
      class AboutView(TemplateView):
          template_name = "about.html"

- #### you're free to pass a `dictionary` settings parameter ( `@cbv_tracker({})` ) with any of these keys:

  - `'mro'` `<class 'bool'>` (Example 2)

  - `'exclude'` `<class 'list'>` (Example 2)

  - `'explicit'` `<class 'str'>` (Example 3)

- ## Example 1 (default)

  - `views.py`

        from cbv_tracker import cbv_tracker


        @cbv_tracker()
        class SignupView(CreateView):

            template_name = 'registration/signup.html'
            form_class = CustomUserCreationForm
            success_url = reverse_lazy('login')

            def get(self, request, *args, **kwargs):
                if request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('home:home-page'))
                else:
                    return super().get(request, *args, **kwargs)

  - `terminal`

        ✔ SignupView
        System check identified no issues (0 silenced).
        July 19, 2022 - 16:12:13
        Django version 4.0.5, using settings 'mysite.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        • SignupView → View ↘ ----------------------------- __init__(self, **kwargs)
        • SignupView → View ↘ ----------------------------- setup(self, request, *args, **kwargs)
        • SignupView → View ↘ ----------------------------- dispatch(self, request, *args, **kwargs)
        • SignupView ↘ ------------------------------------ get(self, request, *args, **kwargs)
        • SignupView → FormMixin ↘ ------------------------ get_context_data(self, **kwargs)
        • SignupView → FormMixin ↘ ------------------------ get_form(self, form_class=None)
        • SignupView → ModelFormMixin ↘ ------------------- get_form_class(self)
        • SignupView → ModelFormMixin ↘ ------------------- get_form_kwargs(self)
        • SignupView → FormMixin ↘ ------------------------ get_initial(self)
        • SignupView → FormMixin ↘ ------------------------ get_prefix(self)
        • SignupView → TemplateResponseMixin ↘ ------------ render_to_response(self, context, **response_kwargs)
        • SignupView → SingleObjectTemplateResponseMixin ↘  get_template_names(self)
        [19/Jul/2022 16:12:20] "GET /signup/ HTTP/1.1" 200 5778

- ## Example 2 (settings parameter)

  Method Resolution Order `{'mro': True}` gets printed only once upon startup of the server.

  `{'exclude': ['__init__', 'setup', 'dispatch', 'get']}` will ommit listed methods from being `printed`

  - `views.py`

        from cbv_tracker import cbv_tracker


        @cbv_tracker(
            settings={
                'mro': True,
                'exclude': ['__init__', 'setup', 'dispatch', 'get']
            }
        )
        class SignupView(CreateView):

            template_name = 'registration/signup.html'
            form_class = CustomUserCreationForm
            success_url = reverse_lazy('login')

            def get(self, request, *args, **kwargs):
                if request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('home:home-page'))
                else:
                    return super().get(request, *args, **kwargs)

  - `terminal`

        ✔ SignupView
        1, SignupView,
        2, CreateView,
        3, SingleObjectTemplateResponseMixin,
        4, TemplateResponseMixin,
        5, BaseCreateView,
        6, ModelFormMixin,
        7, FormMixin,
        8, SingleObjectMixin,
        9, ContextMixin,
        10, ProcessFormView,
        11, View
        System check identified no issues (0 silenced).
        July 19, 2022 - 16:18:13
        Django version 4.0.5, using settings 'mysite.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        • SignupView → FormMixin ↘ ------------------------ get_context_data(self, **kwargs)
        • SignupView → FormMixin ↘ ------------------------ get_form(self, form_class=None)
        • SignupView → ModelFormMixin ↘ ------------------- get_form_class(self)
        • SignupView → ModelFormMixin ↘ ------------------- get_form_kwargs(self)
        • SignupView → FormMixin ↘ ------------------------ get_initial(self)
        • SignupView → FormMixin ↘ ------------------------ get_prefix(self)
        • SignupView → TemplateResponseMixin ↘ ------------ render_to_response(self, context, **response_kwargs)
        • SignupView → SingleObjectTemplateResponseMixin ↘ get_template_names(self)
        [19/Jul/2022 16:18:14] "GET /signup/ HTTP/1.1" 200

- ## Example 3 (settings parameter)

  Only the body of the first method in its MRO gets printed, in the following case `'exclude'` key is ignored and `get` method is `printed`.

  - `views.py`

        from cbv_tracker import cbv_tracker


        @cbv_tracker(
            settings={
                'exclude': ['__init__', 'setup', 'dispatch' 'get'],
                'explicit': 'get'
            }
        )
        class SignupView(CreateView):

            template_name = 'registration/signup.html'
            form_class = CustomUserCreationForm
            success_url = reverse_lazy('login')

            def get(self, request, *args, **kwargs):
                if request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('home:home-page'))
                else:
                    return super().get(request, *args, **kwargs)

  - `terminal`

        ✔ SignupView
        System check identified no issues (0 silenced).
        July 19, 2022 - 16:22:44
        Django version 4.0.5, using settings 'mysite.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        • SignupView ↘
            def get(self, request, *args, **kwargs):
                if request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('leads:lead-list'))
                else:
                    return super().get(request, *args, **kwargs)

        [19/Jul/2022 16:22:46] "GET /signup/ HTTP/1.1" 200 5778
