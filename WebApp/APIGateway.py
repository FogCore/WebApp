import requests

API_Gateway_URL = 'http://APIGateway:80'


# This class contains the API Gateway methods for working with users
class User:
    API_Gateway_URL = API_Gateway_URL + '/user'

    # Checks the user's existence
    @staticmethod
    def check_user_existence(username):
        params = {'username': username}
        return requests.get(url=API_Gateway_URL + '/check-user-existence', params=params)

    # Creates a new user in the system
    @staticmethod
    def add_user(first_name, last_name, username, password):
        params = {'first_name': first_name,
                  'last_name': last_name,
                  'username': username,
                  'password': password}
        return requests.post(url=User.API_Gateway_URL, params=params)

    # Returns JWT access token based on username and password
    @staticmethod
    def login(username, password):
        params = {'username': username,
                  'password': password}
        return requests.get(url=API_Gateway_URL + '/login', params=params)

    # Returns information about the user
    @staticmethod
    def get_user_info(username, token):
        params = {'username': username}
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url=User.API_Gateway_URL, params=params, headers=headers)

    # Sets the full user name and administrator rights
    @staticmethod
    def update_user_data(username, first_name, last_name, admin, token):
        params = {'first_name': first_name, 'last_name': last_name, 'admin': admin}
        headers = {'Authorization': 'Bearer ' + token}
        return requests.put(url=User.API_Gateway_URL + '/' + username, params=params, headers=headers)

    # Sets new user password
    @staticmethod
    def update_password(username, password, token):
        params = {'password': password}
        headers = {'Authorization': 'Bearer ' + token}
        return requests.patch(url=User.API_Gateway_URL + '/' + username, params=params, headers=headers)


# This class contains the API Gateway methods for working with images of fog applications
class Images:
    API_Gateway_URL = API_Gateway_URL + '/image'

    # Returns the list of fog application images
    @staticmethod
    def list(username, token):
        params = {'username': username}
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url=Images.API_Gateway_URL + 's', params=params, headers=headers)

    # Returns information about a specified image of a fog application
    @staticmethod
    def find(username, image_name, token):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url=Images.API_Gateway_URL + '/' + username + '/' + image_name, headers=headers)

    # Removes an image of fog application
    @staticmethod
    def delete(username, image_name, token):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.delete(url=Images.API_Gateway_URL + '/' + username + '/' + image_name, headers=headers)


# This class contains the API Gateway methods for working with fog nodes
class Cloudlets:
    API_Gateway_URL = API_Gateway_URL + '/cloudlets'

    # Find fog devices that satisfy the specified criteria
    @staticmethod
    def find(cloudlet, token):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(url=Cloudlets.API_Gateway_URL, params=cloudlet, headers=headers)
