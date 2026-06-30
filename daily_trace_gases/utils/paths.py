import os.path
import git

basedir = ""

def set_basedir(value):
    global basedir
    basedir = value

def codebase_folder():
    global basedir
    return basedir
    # repo = git.Repo('.', search_parent_directories=True)
    # return repo.working_tree_dir
    # return "/app/dps-unit-test/daily-trace-gases"

def models_storage():
    codebase = codebase_folder()
    return os.path.join(codebase,"models","JPL_TRACE_GASES_MODELS")
    # return "/app/dps-unit-test/models/JPL_TRACE_GASES_MODELS"
