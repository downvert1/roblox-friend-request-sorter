import requests, httpx, threading, queue, time, operator
import dateutil.parser as dp
import numpy as np


session = requests.Session()
session.cookies['.ROBLOSECURITY'] = ""


nextPageCursor = ""
v = False
total_friends = 0
user_list = []
times_ran = 0

for _ in range(10000):
    times_ran+=1 
    try:
        req = session.get("https://friends.roblox.com/v1/my/friends/requests?sortOrder=Desc&limit=100&cursor=" + nextPageCursor)
    except:
        pass

    if req.status_code == 200:
        nextPageCursor = req.json()['nextPageCursor']
        print(f"Next Cursor: {nextPageCursor}")
        if nextPageCursor == None:
            v = True

        json1 = req.json()['data'][:]
        for i in range(len(json1)):
            userid = req.json()['data'][i]['id']
            username = req.json()['data'][i]['name']
            termed = req.json()['data'][i]['isBanned']
            sent_at = req.json()['data'][i]['friendRequest']['sentAt']
            user_list.append(userid)

        total_friends += int(len(req.json()['data']))
        print(f"Friends Counted: {total_friends} | Page Cursor: {nextPageCursor}")

    
    else:
        print(req.status_code)
        print(req.content)
    if v == True:
        break


print("Finished gathering friend requests...")
print("Starting dictionary parsing...")
time.sleep(3)
value_dictionary = {}
lists = np.array_split(user_list, times_ran)
print(f"Amount of lists to format: {len(lists)}")
time.sleep(3)
print("Sending requests to rblx.trade | PLEASE WAIT FOR PROGRAM TO SAY FINISHED")
for list in lists:
    python_list = list.tolist()
    url_data = ','.join(map(str, python_list))
    url = f"https://rblx.trade/api/v2/users/info?userIds={url_data}"
    r = requests.get(url)
    json2 = r.json()[:]
    for i in range(len(json2)):
        user_name = r.json()[i]['username']
        value = r.json()[i]['accountValue']
        value_dictionary.update({user_name:value})

sorted_dictionary = sorted(value_dictionary.items(), key=lambda x: -x[1])
final_dictionary = {k:v for k,v in sorted_dictionary}

print(f"Length of final sorted dictionary: {len(final_dictionary)}")
time.sleep(3)
with open("friend_data.txt", "w") as f:
    for key, value in final_dictionary.items():
        f.writelines(f"{key} | {value}\n")


print("\nFinished!\n")

input("Enter to exit")
