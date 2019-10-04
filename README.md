# ClassicQuestGivers
Dataset on all quests and from what questgiver they are from in claasic (db.db)

### Usage:
Application is ment to be run thru a linux terminal (sorry windows users =3).\
In `settings.json` change the path to your wow installation path (if this is not done the `--file` option is required).\
Most basic usage:\
`python main.py $character_name $character_realm` 

For aditional options:\
`python main.py -h` .

### Goals:
With given level find questgivers with yellow quests (in specified zone or not) from stored dataset from classic.wowhead.com. ✔️

### Aditional Goals: 
Make availeble via web using django.
