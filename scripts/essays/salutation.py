# Script juste pour tester le HotReload en CodeSpace

# 1fo Le message affiché est défini dans MESSAGE_TEST
# 1fo Change un caractère dans MESSAGE_TEST pour tester le reload !

MESSAGE_TEST = "Look bien la CLI, et change un caractère dans la variable chaîne !"

def hi():
    return MESSAGE_TEST

def cls():
    return "\033c"