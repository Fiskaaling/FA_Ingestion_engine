from git import Repo
import os


def get_info():
    # Returnar ein tekst í lýsur git status
    repo = Repo(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    text = 'Git_Branch,' + str(repo.active_branch) + '\n' + 'Git_commit_sha,' + str(repo.head.object.hexsha) + '\n' + 'Unsaved_changes,' + str(repo.is_dirty()) + '\n'
    return text, repo.is_dirty()