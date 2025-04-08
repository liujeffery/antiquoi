class blackboard:

    def __init__(self, image, description):
        self.item = None
        self.max_price = None
        self.min_price = None
        self.condition = None
        self.image = image
        self.description = description

    def read(self, attribute):
        return getattr(self, attribute)
    
    def write(self, attribute, value):
        setattr(self, attribute, value)

