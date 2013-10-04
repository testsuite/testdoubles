def main():
    import sys
    from tests.common import run_nose2

    nose2 = run_nose2(__package__)
    sys.exit(nose2)

if __name__ == '__main__':
    main()