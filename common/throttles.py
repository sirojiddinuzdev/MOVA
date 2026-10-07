from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    scope = 'login'

class RegisterRateThrottle(UserRateThrottle):
    scope = 'register'

class ClaimRateThrottle(UserRateThrottle):
    scope = 'claim'

class SearchRateThrottle(UserRateThrottle):
    scope = 'search'
