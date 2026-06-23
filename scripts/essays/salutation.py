# Script juste pour tester le HotReload en CodeSpace
# @n Le message affiché est défini dans MESSAGE_TEST
# @n Change un caractère dans MESSAGE_TEST pour tester le reload !

MESSAGE_TEST = "Look la CLI, et change un caractère dans la variable chaîne !"

def hi():
    return MESSAGE_TEST

def cls():
    return "\033c"