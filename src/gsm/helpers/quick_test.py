import os


def switch(choice):

    def action_a():
        print("Action A")

    def action_b():
        print("Action B")

    def action_default():
        print("Action par défaut")

    actions = {
        "a": action_a,
        "b": action_b,
    }

    actions.get(choice, action_default)()


if __name__ == "__main__":
    # print('Flet is' , ('running' if os.environ.get("FLET_RUNNING") else 'not yet started'))

    switch("a")

    if os.environ.get("FLET_RUNNING") != "1":
        import subprocess

        os.environ["FLET_RUNNING"] = "1"
        subprocess.run(["flet", "run", "src/gsm/helpers/quick_test.py"])
