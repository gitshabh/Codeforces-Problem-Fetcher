import requests
import json
import time

users_problems = {'rishabh.srivastava' : '', 'f_in_the_chat' : '', 'singhxayush' : ''} #handles of users for whom you want to fetch unsolved problems
already_solved_problems = {'1824A','1817A','1883G1','1765N','1886C','1883D','1739D','1883F'} #this is not necessary, still I've added this because when we make submissions in gym contests, it's not reflected in our submissions list.
ratingwise_problems = {
    1500 : '_',
    1700 : '_',
    1900 : '_'
}
# specify your required rating of problems here
# tag specification feature still has to be added
# another feature that can be added is to specify the number of problems needed to be fetched of each rating

def fetch_user_submissions() : 
    for user in users_problems.keys() :
        url = f'https://codeforces.com/api/user.status?handle={user}&from=1&count=5000'
        # time.sleep(0.01) # this line can be required because making api calls too quickly can cause 500 errors
        user_response = requests.get(url)
        if user_response.status_code == 200 :
            users_problems[user] = user_response.text
        else :
            print(f'error {user_response.status_code} on user {user}')

def check_if_solved_by_user(problem_code):
    if problem_code in already_solved_problems :
        return True
    
    for problems in users_problems.values() :
        if problems == '' :
            continue
        for result in json.loads(problems)['result']:
            problem = result['problem']
            if str(problem['contestId']) + problem['index'] == problem_code :
                return True

    return False

def fetch_problems() :
    problemset = requests.get('https://codeforces.com/api/problemset.problems')
    if problemset.status_code != 200 :
        print('error' + str(problemset.status_code))
        return
    print(problemset.text)
    problems = json.loads(problemset.text)
    problem_list = problems['result']['problems']
    cnt = 0
    for problem in problem_list :
        if 'rating' in problem.keys():
            rating = problem['rating']
            if rating in ratingwise_problems.keys() and ratingwise_problems[rating] == '_':
                problem_code = str(problem['contestId'])+problem['index']
                status = check_if_solved_by_user(problem_code)
                if status == False:
                    cnt += 1
                    ratingwise_problems[rating] = problem_code
                    if cnt == len(ratingwise_problems):
                        break

fetch_user_submissions()
fetch_problems()
for r,p in ratingwise_problems.items() :
    print(r,p)


