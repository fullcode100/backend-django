# Endpoint and Rules

note: 
- trailing '/' are important!
- contain fake response

# 
## Get CSRF Token
- method: [GET]
- /game
#### Response
```JSON
  {
    "csrf_token": "khqwead9021dfs23rffih89l2nosdf9arj2j091kewf",
  }
```

# 
## Game Start
- method: [POST]
- /game/start/
#### Request
```JSON
  {
    "kontak": "nama_kontak",
  }
```
#### Response
```JSON
  {
    "kontak": "nama_kontak",
    "token": "dfah378YYUDJ873HadsdasjfkJA912H7sjs8JD",
    "phase": 1
  }
```

#### ERROR / FAKE Response
```JSON
  {
    "token": "dfah378YYUDJ873HadsdasjfkJA912H7sjs8JD",
  }
```
- ***note:*** please check if response data have both *"kontak"* and *"token"*. if not then it's a fake token.
```JSON
Error 404
  {
    "message": "Periode Game masih belum dimulai"
  }
```
- ***note:*** Error response info key nya "message"

# 
## Game Finish
- method: [POST]
- /game/finish/
#### Request
```JSON
  {
    "kontak": "nama_kontak",
    "token": "dfah378YYUDJ873HadsdasjfkJA912H7sjs8JD",
    "time": 60,
    "benar": 3,
  }
```
#### Response
```JSON
  {
    "message": "OK"
  }
```
#### ERROR Response
```JSON
Error 404
  {
    "message": "Anda sudah Bermain hari ini"
  }
```
- ***note:*** Error response info key nya "message"