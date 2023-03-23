class CustomResponse:
    def __init__(self, *args, **kwargs):
        self.STATUS = kwargs.get('status')
        self.MESSAGE = kwargs.get('message')
        self.DATA = kwargs.get('data')
        print(self.MESSAGE)

    def response(self):
        if self.STATUS == 200:
            context = {"status": self.STATUS, "message": "success", "data": self.DATA}
        elif self.STATUS == 400:
            if self.MESSAGE == "local variable 'response' referenced before assignment":
                context = {"status": self.STATUS, "message": f"{self.MESSAGE}: unable to login.", "data": {}}
            else:
                context = {"status": self.STATUS, "message": self.MESSAGE, "data": {}}
        elif self.STATUS == 404:
            context = {"status": self.STATUS, "message": self.MESSAGE, "data": {}}
        elif self.STATUS == 500:
            context = {"status": self.STATUS, "message": self.MESSAGE, "data": {}}
        else:
            context = {"status": self.STATUS, "message": "success", "data": self.MESSAGE}

        return context