import inspect


__all__ = ["cbv_tracker"]


def method_decorator(original_method, settings, cls_name, qualname):

    def decorator(*args, **kwargs):

        line_length = len(inspect.getsourcelines(original_method)[0][0])
        indentation = '-' * settings['longest']
        
        if 'explicit' in settings and settings['explicit']:
            if cls_name == qualname:
                print(f"• {cls_name} ↘ \n{inspect.getsource(original_method)}")
            else:
                print(f"• {cls_name} → {qualname} \n{inspect.getsource(original_method)}")
        
        else:
            if cls_name == qualname:
                print(f"• {cls_name} ↘ {indentation[len(cls_name):] + '---'} {inspect.getsourcelines(original_method)[0][0][8:line_length-2]}")
            else:
                print(f"• {cls_name} → {qualname} ↘ {indentation[len(cls_name)+len(qualname):]} {inspect.getsourcelines(original_method)[0][0][8:line_length-2]}")

        result = original_method(*args, **kwargs)
        return result

    return decorator


def cbv_tracker(settings=None):
    
    if settings:
        if not isinstance(settings, dict):
            raise TypeError(
                f"""cbv-tracker decorator expects a <class 'dict'> type as a first argument, instead {type(settings)} was given.
                    Example: settings={{'mro': True, 'exclude': ['__init__', 'dispatch']}}
                """
                )
    else:
        settings = dict()
    

    def wrapper(cls):

        print(f"✔ {cls.__name__}")
        
        if "mro" in settings and settings["mro"]:
            mro = ", \n".join(
                [f"  |___ {i + 1}, {c.__name__}" for i, c in enumerate(inspect.getmro(cls)) if c.__name__ != "object"]
                )
            print(mro)


        def explicit():
            if "explicit" in settings and settings["explicit"]:
                if not isinstance(settings['explicit'], str):
                    raise TypeError(
                        f"""settings key 'explicit' expects a <class 'str'> type value, instead {settings['explicit']} was given.
                            Example: settings={{'explicit':'setup'}}
                        """
                        )
                return True
            return False


        def exclude():
            if "exclude" in settings and settings["exclude"]:
                if not isinstance(settings['exclude'], list):
                    raise TypeError(
                        f"""settings key 'exclude' expects a <class 'list'> type value, instead {settings['exclude']} was given.
                            Example: settings={{'exclude': ['__init__', 'dispatch']}}
                        """
                        )
                return True
            return False


        def get_qualname(function_qualname):
            qualname = ""
            for char in function_qualname:
                if char == ".":
                    break
                qualname += char
            return qualname


        settings['longest'] = 1

        for name, function in inspect.getmembers(cls, predicate=inspect.isfunction):
            qualname = get_qualname(function.__qualname__)
            
            if len(qualname) + len(cls.__name__) > settings['longest']:
                settings['longest'] = len(qualname) + len(cls.__name__)


            def setattr_callback():
                setattr(cls, name, method_decorator(function, settings, cls.__name__, qualname))


            if explicit():
                if name == settings['explicit']:
                    setattr_callback()
            elif exclude():
                if name in settings['exclude']:
                    pass
                else:
                    setattr_callback()
            else:
                setattr_callback()

        return cls
    
    return wrapper

