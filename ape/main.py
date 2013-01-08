def get_task_parser(task):
    '''
    construct an ArgumentParser for task
    this function returns a tuple (parser, proxy_args)
    if task accepts varargs only, proxy_args is True.
    if task accepts only positional and explicit keyword args, 
    proxy args is False.
    '''
    import argparse
    import inspect
    args, varargs, keywords, defaults = inspect.getargspec(task)
    defaults = defaults or []
    parser = argparse.ArgumentParser(
        prog='ape ' + task.__name__,
        add_help=False,
        description = task.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    if varargs is None and keywords is None:
        for idx, arg in enumerate(args):
            if idx < len(args) - len(defaults):
                parser.add_argument(arg)
            else:
                default = defaults[idx - len(defaults)]
                parser.add_argument('--' + arg, default=default)
        return parser, False
    elif not args and varargs and not keywords and not defaults:
        return parser, True
    else:
        raise

def invoke_task(task, args):
    '''
    invoke task with args
    '''
    parser, proxy_args = get_task_parser(task)
    if proxy_args:
        task(*args)
    else:
        pargs = parser.parse_args(args)
        task(**vars(pargs))

def main(args, features=None):
    '''
    composes task modules of the selected features and calls the
    task given by args
    '''
    import importlib
    from ape import tasks, TaskNotFound, FeatureNotFound

    features = features or []
    for feature in features:
        try:
            feature_module = importlib.import_module(feature)
        except ImportError:
            raise FeatureNotFound(feature)
        try:
            tasks_module = importlib.import_module(feature + '.tasks')
            tasks.superimpose(tasks_module)
        except ImportError:
            print 'No tasks module in feature %s. Skipping.' % feature

    if len(args) < 2 or (len(args) == 2 and args[1] == 'help'):
        tasks.help()
    else:
        taskname = args[1]
        try:
            task = tasks.get_task(taskname)
            remaining_args = args[2:] if len(args) > 2 else []
            invoke_task(task, remaining_args)
        except TaskNotFound:
            print 'Task "%s" not found! Use "ape help" to get usage information.' % taskname

if __name__ == '__main__':
    '''
    entry point when used via command line
    
    features are given using the environment variable PRODUCT_EQUATION.
    '''
    import sys
    import os
    features = os.environ.get('PRODUCT_EQUATION', '').split()
    main(sys.argv, features=features)
