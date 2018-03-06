def assertAs(assertion, message):
    if not assertion:
        print("#" * len(message) + "\n" + message +
              "\n" + "#" * len(message) + "\n")
        assert(assertion)
