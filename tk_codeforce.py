import tkinter as tk
import pandas as pd
import requests
import json

class UsernameError(Exception):
    '''raised if invalid username'''

def main_gui(username):
    print(username)
    if not username:
        username = 'Anu2006'
    userinfo_names = ['current_rating', 'current_rank', 'max_rating', 'max_rank']
    positions = [180, 200, 220, 240]
    resp = get_url(username.replace(' ', '_'))
    cleaned_data = clean_data(resp)

    if cleaned_data != 'no resutlts':
        messages = [f'{name}: {info}'
                    for info, name in zip(get_userinfo(cleaned_data), userinfo_names)]

        print(messages)
        tk.Label(frame, text=f'User: {username}').place(x=120, y=140)
        for message, y in zip(messages, positions):
            info_label = tk.Label(frame, text=message)
            info_label.place(x=20, y=y)

    else:
        info_label = tk.Label(frame, text='no results')
        info_label.place(x=20, y=180)
    
    
# get json
def get_url(username):
    url = f'https://codeforces.com/api/user.rating?handle={username}' 
    # with open('new.txt', 'w') as fp:
    #     fp.write(requests.get(url).text)

    # exit()
    try:
        return requests.get(url).text

    except requests.ConnectionError:
        with open('data.txt') as fp:
            resp = fp.read()

        return resp


# data cleaning
def clean_data(json_data):
    raw_data = json.loads(json_data)
    if raw_data['status'] == 'FAILED':
        raise UsernameError('Invalid username')
        
    else:
        userdata = pd.DataFrame(raw_data)
        if 'results' in userdata:
            return userdata['results']

        else:
            print(raw_data)
            return 'no resutlts'
    
    # with open('new.txt', 'w') as fp:
    #     fp.write(raw_data)



# fetching information from data
def get_userinfo(cleaned_data):
    max_index = len(cleaned_data) - 1
    value_ranges = [max_index, max_index, slice(None, None), slice(None, None)]
    catogaries = ['newRating', 'rank'] * 2

    for value_range, catogary in zip(value_ranges, catogaries):
        try:
            if value_range.__class__ == slice:
                print(catogary)
                yield max(cleaned_data.loc[value_range, catogary])

            else:
                yield  cleaned_data.loc[value_range, catogary]

        except LookupError:
            yield None


root = tk.Tk()
root.geometry('600x600')
root.title('codeforces user ratings')

frame = tk.Frame(root, bg='#7e3ba8')
frame.place(relx = 0.1, rely= 0.1, relwidth = 0.8,
            relheight = 0.8)

welcome = tk.Label(root, text='welcome', relief='solid', width=20, font=('arial', 19, 'bold'))
welcome.place(x=150, y=80)

username_label = tk.Label(frame, text='user name', width=15)
username_label.place(x=10, y=100)

entry = tk.Entry(frame, text='User name')
entry.place(x=120, y=100)

submit = tk.Button(frame, text="Enter", width=15, command=lambda: main_gui(entry.get()))
submit.place(x=300, y=100)

root.mainloop()
