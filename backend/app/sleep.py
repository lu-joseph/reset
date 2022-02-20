from app import db
from app.userData import UserData
from datetime import datetime, timedelta


class Sleep(db.Model):
    __tablename__ = 'sleep'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    hours = db.Column(db.REAL)
    quality = db.Column(db.String)
    feel = db.Column(db.String)
    userid = db.Column(db.Integer)

    # date must be in dd-mm-yyyy format
    def add_entry(userid, hours, quality, feel, date=datetime.today().strftime('%Y-%m-%d')):
        if (hours is None or userid is None or quality is None or feel is None):
            raise Exception('field cannot be null')
        elif (quality != "POOR" and quality != "SOSO" and quality != "GOOD"):
            raise Exception('invalid sleep quality')
        elif (feel != "AWAKE" and feel != "TIRED" and feel != "SLEEPY"):
            raise Exception('invalid sleep feeling')
        elif (float(hours) < 0):
            raise Exception('hours cannot be negative')

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be yyyy-mm-dd")

        entry = Sleep(userid=userid, date=date,
                      quality=quality, feel=feel, hours=hours)
        db.session.add(entry)
        db.session.commit()
        return 'success'

    def dailySleepFeedback(id, date):
        user = UserData.getUser(id)
        if (user is None):
            return Exception("user not found")
        recommendedSleep = Sleep.getRecommendedHours(id)
        entryToday = Sleep.query.filter(Sleep.userid == id,
                                        Sleep.date == date).first()
        noEntry = entryToday is None
        # result = 0
        sleepToday = 0
        # if (noEntry):
        #     message = "You have not inputted sleep hours today."
        # else:
        if not noEntry:
            sleepToday = entryToday.hours
            # result = sleepToday - recommendedSleep
            # if result < 0:
            #     message = "Today you slept " + str(abs(result)) + \
            #         " less hours than the recommended amount. Try to do better tomorrow!"
            # elif result == 0:
            #     message = "Good job! You slept the exact recommended number of hours today!"
            # else:
            #     message = "Good job! You slept " + \
            #         str(result) + " more hours than the recommended amount."
        return {
            # 'result': result,
            'noEntry': noEntry,
            # 'message': message,
            # 'quality': entryToday.quality,
            # 'feel': entryToday.feel,
            'hours': sleepToday,
            'recommended_hours': recommendedSleep,
            # 'recommendation': "According to The Center for Disease Control and Prevention, your age group should try to sleep " +
            # str(recommendedSleep) + " hours a night."
        }

    def getRecommendedHours(id):
        user = UserData.getUser(id)
        if (user is None):
            return Exception("user not found")
        age = user["age"]
        if 0 < age <= 2:
            recommendedSleep = 11
        elif 2 < age <= 5:
            recommendedSleep = 10
        elif 5 < age <= 12:
            recommendedSleep = 9
        elif 12 < age <= 18:
            recommendedSleep = 8
        else:
            recommendedSleep = 7
        return recommendedSleep

    def getWeeklyView(id):
        user = UserData.getUser(id)
        if (user is None):
            return Exception("user not found")
        dayOfWeek = datetime.today().weekday()
        week = {'monday': {}, 'tuesday': {},
                'wednesday': {}, 'thursday': {}, 'friday': {}, 'saturday': {}, 'sunday': {}, }
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            week[day] = {'hours': 0, 'entered': False}
        for day in range(dayOfWeek + 1):
            print("date:", (datetime.today() -
                  timedelta(days=dayOfWeek - day)).strftime('%Y-%m-%d'))
            sleepData = Sleep.dailySleepFeedback(
                id, (datetime.today() - timedelta(days=dayOfWeek - day)).strftime('%Y-%m-%d'))
            if not sleepData["noEntry"]:
                week[day]["hours"] = sleepData["hours"]
                week[day]["entered"] = True
        return week

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'hours': self.hours,
            'quality': self.quality,
            'feel': self.feel,
            'userid': self.userid
        }
