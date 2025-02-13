from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class AnonMovieRateThrottle(AnonRateThrottle):
    rate = '100/day'

class UserMovieRateThrottle(UserRateThrottle):
    rate = '1000/day' 