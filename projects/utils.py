
class Utility():
    def __init__(self):
        pass

    @staticmethod
    def sort_by_completion(items, reverse=False):
        uncompleted = []
        completed = []
        for item in items:
            if item.completed:
                completed.append(item)
            else:
                uncompleted.append(item)
        if reverse:
            for item in uncompleted:
                completed.append(item)
            return completed
        for item in completed:
            uncompleted.append(item)
        return uncompleted

    