## About:

- ### cbv-tracker is a simple Python package that works alongside Django's Class Based Views by `printing` methods that were called to process `HTTP request` and return `HTTP response`

---

## Installation:

- ### Requirements: python 3.8 or later

        pip install cbv-tracker

---

## How to use:

- ### Example 1 (default)

  `views.py:`

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

  `terminal/output`:

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

- ### Example 2 (settings parameter- every key-value pair is optional)

  `views.py`:

        from cbv_tracker import cbv_tracker

        @cbv_tracker(settings={
            'mro': True,
            'exclude': ['__init__', '__setup__', '__dispatch__']
        })
        class SignupView(CreateView):

        template_name = 'registration/signup.html'
        form_class = CustomUserCreationForm
        success_url = reverse_lazy('login')

        def get(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse('home:home-page'))
            else:
                return super().get(request, *args, **kwargs)

  `terminal/output`:

        ✔ SignupView
        |___ 1, SignupView,
        |___ 2, CreateView,
        |___ 3, SingleObjectTemplateResponseMixin,
        |___ 4, TemplateResponseMixin,
        |___ 5, BaseCreateView,
        |___ 6, ModelFormMixin,
        |___ 7, FormMixin,
        |___ 8, SingleObjectMixin,
        |___ 9, ContextMixin,
        |___ 10, ProcessFormView,
        |___ 11, View
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
        • SignupView → SingleObjectTemplateResponseMixin ↘  get_template_names(self)
        [19/Jul/2022 16:18:14] "GET /signup/ HTTP/1.1" 200

  <span style="color:orange">Note that the Method Resolution Order gets printed only once upon startup of the server</span>

- ### Example 3 (settings parameter- every key-value pair is optional)

  `views.py:`

        from cbv_tracker import cbv_tracker

        @cbv_tracker(settings={
            'exclude': ['__init__', '__setup__', '__dispatch__'],
            'explicit': 'get'
        })
        class SignupView(CreateView):

        template_name = 'registration/signup.html'
        form_class = CustomUserCreationForm
        success_url = reverse_lazy('login')

        def get(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse('home:home-page'))
            else:
                return super().get(request, *args, **kwargs)

  `terminal/output`:

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

  <span style="color:orange">Note that only the body of the first method in its MRO gets printed, in this case `'exclude': ['__init__', '__setup__', '__dispatch__']` setting is ignored</span>
