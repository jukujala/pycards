import os


def absolute_file_paths(directory):
  path = os.path.abspath(directory)
  return [entry.path for entry in os.scandir(path) if entry.is_file()]


