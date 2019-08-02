from git import Repo
import os

def get_info():
    repo = Repo(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(repo.active_branch)
    print(repo.head.object.hexsha)
    print(repo.is_dirty())
    print(repo.)
