# Route and Formatting
- /api/team/
```JSON
[
	{
		"id"
		"name"
		"win"
		"lose"
		"draw"
		"goal_masuk"
        "goal_kebobolan"
        "points"
        "selisih_goal"
        "banyak_match"
	},
	....
]
```
- /api/team/{pk}/
```JSON
{
		"id"
		"name"
		"win"
		"lose"
		"draw"
		"goal_masuk"
        "goal_kebobolan"
        "points"
        "selisih_goal"
        "banyak_match"
		"team_players": [
			{
				"id"
				"name"
				"profile_picture"
			},
			....
		]
        "category"
        "manager"
}
```
- /api/team/{pk}/players/
```JSON
{
	"id"
	"name"
	"team_players": [
		{
			"id"
			"name"
			"profile_picture"
		}
	]
	
}
```
- /api/group/
```JSON
[
	{
		"id"
		"name"
	},
	...
]
```
- /api/group/{pk}/
```JSON
{
	"id"
	"name"
	"category":{
		"id"
		"name"
	}
	"group_teams":[
		{
			"id"
			"name"
			"win"
			"lose"
			"draw"
            "goal_masuk"
            "goal_kebobolan"
            "points"
            "selisih_goal"
            "banyak_match"
		},
		...
	]
}
```
- /api/group/{pk}/teams/
```JSON
{
	"id"
	"name"
	"group_teams":[
		{
			"id"
			"name"
			"win"
			"lose"
			"draw"
            "goal_masuk"
            "goal_kebobolan"
            "points"
            "selisih_goal"
            "banyak_match"
		},
		...
	]
}
```
- /api/category/
```JSON
[
	{
		"id"
		"name"
	}
]
```
- /api/category/{pk}/
```JSON
{
	"id"
	"name"
}
```
- /api/category/{pk}/players/
```JSON
{
	"id"
	"name"
	"category_players":[
		{
			"id"
			"name"
			"profile_picture"
		},
		...
	]
}
```
- /api/category/{pk}/teams/
```JSON
{
	"id"
	"name"
	"category_teams":[
		{
			"id"
			"name"
			"win"
			"lose"
			"draw"
            "goal_masuk"
            "goal_kebobolan"
            "points"
            "selisih_goal"
            "banyak_match"
		},
		...
	]
}
```
- /api/category/{pk}/groups/
```JSON
{
	"id"
	"name"
	"match_groups":[
		{
			"id"
			"name"
		},
		...
	]
}
```

- /api/match_history
```json
[
    {
        "id"
        "team_a": {
            "id"
            "name"
        }
        "team_b": {
            "id"
            "name"
        }
        "is_game"
        "team_a_goal"
        "team_b_goal"
        "stage"
        "is_a_win"
        "is_b_win"
        "group": {
            "id"
            "name"
        }
    }
]
```
- /api/match_history/{category_name}/
```json
[
    {
        "id"
        "team_a": {
            "id"
            "name"
        }
        "team_b": {
            "id"
            "name"
        }
        "is_game"
        "team_a_goal"
        "team_b_goal"
        "stage"
        "is_a_win"
        "is_b_win"
    },
    ......
]
```