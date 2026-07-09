#場景切換
class SceneManager:

    def __init__(self):

        self.scenes = {}

        self.current = None


    def add_scene(self,name,scene):

        self.scenes[name]=scene


    def change_scene(self,name):

        if self.current:

            self.current.exit()

        self.current=self.scenes[name]

        self.current.enter()


    def handle_event(self,event):

        if self.current:

            return self.current.handle_event(event)


    def update(self):

        if self.current:

            self.current.update()


    def draw(self,screen):

        if self.current:

            self.current.draw(screen)
