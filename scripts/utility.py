import requests

class utility:
    def callAPI(self, url):
        """General purpose function for retrieving data from a url
        Args:
            url (string): url???
        Raises:
            RuntimeError: Raises a runtime error when the status code isn't 200
        Returns:
            json: the data retrieved from the website"""
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise RuntimeError(f"Request failed: {response.status_code}")
        
    def downloadFile(self, url):
        success = False
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open("3x" 'wb') as file:
                    file.write(response.content)
                    success = True
                    return success, file
        except:
            return success, ""
        
    def twitchID(self, user):
        url = f"https://api.ivr.fi/v2/twitch/user?login={user}"
        data = self.callAPI(url)
        return data[0]["id"]