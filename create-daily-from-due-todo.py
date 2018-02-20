import requests, time, json, datetime

baseurl = "https://habitica.com/api/v3/"
user_id = "....your user id here...."
api_token = "....your api token here...."
headers = {"x-api-user": user_id, "x-api-key": api_token, "Content-Type": "application/json"}


def createDailysFromDueTasks(baseurl, headers):
	dailys = getDailysText(baseurl, headers)
	duetoday = getDueTasks(baseurl, headers)

	for item in duetoday:
		if item["text"] in dailys:
			print("WARNING: Daily skipped because it's already existing: " + item["text"])
		else:
			createTask(baseurl, headers, str(item["text"]), "daily")
			print("Daily added: " + item["text"])


def getDueTasks(baseurl, headers):
	today = str(time.strftime("%Y-%m-%d"))
	duetoday = []
	req = requests.get(baseurl + "tasks/user?type=todos", headers=headers)

	for todo in req.json()['data']:
		# To send only today's todos to the top:    todo['date'][:10] == today:
		# To send all overdue todos to the top:     todo['date'][:10] <= today:
		if 'date' in todo and todo['date'] and todo['date'][:10] <= today:
			duetoday.append(todo)

	return duetoday


def getDailysText(baseurl, headers):
	req = requests.get(baseurl + "tasks/user?type=dailys", headers=headers)
	dailys = []

	for item in req.json()['data']:
		dailys.append(item["text"])

	return dailys


def createTask(baseurl, headers, taskText, taskType):
	now = datetime.datetime.now()
	payload = {'text': taskText, 'type': taskType, "startDate": str(now.strftime("%Y/%m/%d")), 'priority': 2}
	response = requests.post(baseurl + "tasks/user", data=json.dumps(payload), headers=headers)

	if json.loads(response.content)["success"]:
		return True
	else:
		return False


createDailysFromDueTasks(baseurl, headers)