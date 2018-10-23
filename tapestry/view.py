class View:
    filename_re = None

    def __init__(self, dirpath, display, fps=50, sleep=3):
        self.dirpath = dirpath
        self.display = display
        self.fps = fps
        self.sleep = sleep

    @classmethod
    def filter_files(cls, files):
        return sorted([f for f in files if cls.filename_re.match(f)])
