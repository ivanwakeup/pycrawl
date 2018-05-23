class BatchWriter(object):

    batch = set()

    def __init__(self):
        pass

    def add_to_write_batch(self, to_add):
        if len(self.batch) > 100:
            self.batch.add(to_add)

    def write_batch(self):
        pass