# Assumptions

## Assumption 1: 
We do not allow negative time values for the timer.

## Assumption 2: 
We do not need to scale this right now, if we do we could store the timers in a 
database to show the time left instead of getting that from Celery which can take quite some time.

## Assumption 3:
By application being down we mean the Django or Celery server going down, not the Redis server.
If the Redis server also needs to be restarted, we would need to store the timers in a database.
