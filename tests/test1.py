from enum import StrEnum

class Scopes(StrEnum):
    OPENID = "openid"

for i in Scopes:
    print(type( i))
    print(i.value)