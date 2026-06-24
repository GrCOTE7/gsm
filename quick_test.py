# from scripts.essays.salutation import cls, hi

# Script juste pour tester le HotReload en CodeSpace

# uvx watchfiles "python quick_test.py" .

# @n Le message affiché est défini dans MESSAGE_TEST
# @n Change un caractère dans MESSAGE_TEST pour tester le reload !

CHAINE = "Look bien la CLI, et change un caractère dans la variable CHAINE !"

def hi():
    return CHAINE

def cls():
    return "\033c"

while True:
    print(
        cls() +
        "\n".join(
            [" ".join(str(i*j) for j in range(1, i+1)) for i in range(1, 4)]
            + ["", "Ready pour la suite.", "", hi()]
        )
    )



# @! Tatati

# @bug Tatati

# @n Tatati

# @i Tatati

# *** Tatati

# @? Tatati


# @q Tatati

# @2q Tatati

# @Q Tatati

# @2Q Tatati


# @s Tatati


# dl Tatati

# DL Tatati

# @dl Tatati

# @DL Tatati


# see Tatati 🟥

# 2see Tatati ✅

# @2see Tatati 🟥 

# @2SEE Tatati 🟥 

# @see Tatati 🟥 


# 2dbug Tatati

# ❌ Del all BC ↑

# @xxx dfsdfsdf

# 🦄 Tatati

# XXX dfsdfsdf