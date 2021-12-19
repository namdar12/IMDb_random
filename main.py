from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
import requests
import random
import json
import http.client


Builder.load_file('frontend.kv')
headers = {'User-agent': 'Chrome/95.0'}

class FirstScreen(Screen):

    def get_movie_link(self):
        """
        This method grabs the list of movies form MostPopularMovies
        :return: Dictionary, with one key, 'items' , Value is a list of movies
        """
        conn = http.client.HTTPSConnection("imdb-api.com", 443)
        conn.request("GET","https://imdb-api.com/en/API/MostPopularMovies/k_382ogi2l", headers=headers)
        res = conn.getresponse()
        data = res.read()
        movie_dictionary = json.loads(data.decode("utf-8"))
        return movie_dictionary

    def movie_picker(self):
        """
        Choose a random movie

        """
        movie_dictionary = self.get_movie_link()
        max_movies = len(movie_dictionary['items'])
        number = random.randint(0, max_movies)
        self.movie = movie_dictionary['items'][number]

    def download_image(self):
        """
        Downloads the movie image to 'files/images`, so that it can be displayed later
        """
        self.movie_picker()
        image_path = 'files/image.jpeg'
        req = requests.get(self.movie['image'], headers=headers)
        print(self.movie['image'])
        with open(image_path, 'wb') as file:
            file.write(req.content)
        return image_path

    def set_image(self):
        """
        Set's the Image
        """
        self.manager.current_screen.ids.img.source = self.download_image()
        self.manager.current_screen.ids.img.reload()

    def set_labels(self):
        """
        Set's the label
        """
        label = "Title: {}, Year: {}, Rating: {}".format(str(self.movie['title']),str(self.movie['year']),
                                                                                   str(self.movie['imDbRating']))
        self.manager.current_screen.ids.moveInfo.text = label



class RootWidget(ScreenManager): # screen manager, inhereted from screenmanger not required for much
        pass

class MainApp(App):#inhereting from class App

    def build(self):
        return RootWidget()   #main app


MainApp().run()

