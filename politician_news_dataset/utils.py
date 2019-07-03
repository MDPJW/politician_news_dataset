import os

sep = os.path.sep
installpath = os.path.dirname(os.path.realpath(__file__))
newspath_form = sep.join(installpath.split(sep)[:-1] + ['data', '{}', 'news'])
commentspath_form = sep.join(installpath.split(sep)[:-1] + ['data', '{}', 'comments'])
