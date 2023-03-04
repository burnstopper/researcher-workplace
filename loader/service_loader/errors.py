class ServiceError(Exception):
    def __init__(self, status_code):
        self.message = f"unsuccessfull status code: {status_code}"
        super().__init__(self, self.message)

    def __str__(self):
        return "ServiceError: " + self.message
