class ImgNumber():
    '''This class is for saving the current image number and updating it'''

    def __init__(self):

        self.img_number = 0

    def plus(self):
        '''Add one'''

        self.img_number += 1

    def minus(self):
        '''Subtract one'''

        self.img_number -= 1