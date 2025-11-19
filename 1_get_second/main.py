"""
Here we already know that we don't have to
track /.venv/ and /.idea/ folders
BECAUSE! -> .venv contains the environment (libs ,packages etc.)
         -> .idea contains our IDE's configs
So, there's no need to push it to the remote repository
"""


def func():
    print(f'There suppose to be something here )))')


def another_function():
    print(f'Another function')


if __name__ == '__main__':
    func()
    another_function()