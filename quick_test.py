# from scripts.essays.salutation import cls, hi

# Script juste pour tester le HotReload en CodeSpace

# uvx watchfiles "python quick_test.py" .

CHAINE = "Look bien la CLI, et change un caractère dans la variable CHAINE !"

def hi():
    return CHAINE

def cls():
    return "\033c"

# while True:
print(
    cls() +
    "\n".join(
        [" ".join(str(i*j) for j in range(1, i+1)) for i in range(1, 4)]
        + ["", "Ready pour la suite.", "", hi()]
    )
)
