#Using dictionary to store data
resposes={}
terminator=True
while terminator:
    name=input("Please input your name:  ")
    respose=input("What did you learn today?  ")
    resposes[name]=respose
    repeat=input("Is there anyone else?Please reply yes or no:  ")
    if repeat=="yes":
        continue
    else:
        terminator=False
#To decorate your answer
print("/n  Poll Result  ")
for name,respose in resposes.items():
    print(f"{name} learn {respose} today.")


#delete the Key-value paris
alien_0 = {'color': 'green', 'points': 5}  
print(alien_0)
del alien_0['points']
print(alien_0)

#Re-enter the value
alien_0 = {'color': 'green'}
print(f"The alien is {alien_0['color']}.")
alien_0['color'] = 'yellow'
print(f"The alien is now {alien_0['color']}.")


#the way:get(key1,key2):
#you mast input the target key in key1,you can input what you want to print if the target name not in dictionary
alien_0 = {'color': 'green', 'speed': 'slow'}
point_value = alien_0.get('points', 'No point value assigned.')
print(point_value)


# Store dictionarys in a dictionary
users = {
      'aeinstein': {
          'first': 'albert',
          'last': 'einstein',
          'location': 'princeton',
          },

      'mcurie': {
          'first': 'marie',
          'last': 'curie',
          'location': 'paris',
          },

      }

for username, user_info in users.items():
    print(f"\nUsername: {username}")
    full_name = f"{user_info['first']} {user_info['last']}"
    location = user_info['location']

    print(f"\tFull name: {full_name.title()}")
    print(f"\tLocation: {location.title()}")