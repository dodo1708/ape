if __name__ == '__main__':
    import sys
    from ape import tests
    result = tests.run_all()
    retval = 0 if result.wasSuccessful() else 1
    sys.exit(retval)
