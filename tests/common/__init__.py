import os
import subprocess


def is_executing_under_continuous_integration_server():
    return os.getenv('CI', 'false') == 'true'


def run_nose2(*args):
    return subprocess.call(['nose2'] + list(args) + ['--verbose'])


def run_behave():
    from .. import acceptance

    behave = 0
    acceptance_tests_path = acceptance.__path__[0]

    if any([filename for filename in os.listdir(acceptance_tests_path) if filename.endswith('.feature')]):
        behave = subprocess.call(['behave', acceptance_tests_path])
    else:
        print('No feature files were found. Skipping acceptance tests...')

    return behave


def run_pyflakes():
    return subprocess.call(['pyflakes', 'mockingbird'])


def set_support_environment(path):
    os.environ['SUPPORT_PATH'] = '%s%s' % (path, '/support/')


def get_support_path():
    return os.getenv('SUPPORT_PATH', '%s%s' % (os.path.dirname(__file__), '/support/'))