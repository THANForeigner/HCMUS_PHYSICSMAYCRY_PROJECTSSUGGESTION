_completed = []

def complete_project(pid):
    global _completed
    if pid not in _completed:
        _completed.append(pid)
