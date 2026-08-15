import sys

# Lancer avec : uv run flet run scripts/app_window/main.py

sys.argv.append("essai")  # simulation ""./go essai"
# sys.argv.append('deux') # simulation ""./go essai deux"

if __name__ == "__main__":
    args = sys.argv[1:]
    print("Oki")
    print("Arguments reçus :", args)
    
    if args:
        print("Premier argument :", args[0])
    else:
        print("Aucun argument")
