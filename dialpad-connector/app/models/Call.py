import datetime

class Call:
    
    def __init__(self, call_id= "", subject = "", activity_date = None, phone = "", duration_in_minutes = 0):
        self.call_id = call_id
        self.subject = subject
        self.activity_date = activity_date
        self.phone = phone
        self.duration_in_minutes = duration_in_minutes
