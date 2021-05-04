from django.shortcuts import render
from .models import User


def strip_punctuation(word):
    puncts = ['!', '?', '$',',','@','%','^','&','*','(',')','"',"'"]
    for punct in puncts:
        word = word.replace(punct, '')
    return word

def handle_search(query, strings):
    query = query.lower().split(' ')
    scores_words = []
    for string in strings:
        score = 0
        for word in string.lower().split(' '):
            if word in query:
                score += 10
            elif strip_punctuation(word) in query:
                score += 5
            chars = word.split()
            for query_word in query:
                for char in chars:
                    if char in query_word:
                        score += 1
        scores_words.append((score, string))
    return scores_words

# Create your views here.
def view_users(response):
    users = User.objects.all()
    usernames = [user.username for user in users]
    if response.method == "POST":
        print(response.POST)
        search_term = response.POST.get("usersearch")
        score_words = handle_search(search_term, usernames)
        filtered_users = []
        score_words.sort(reverse=True)
        for score, username in score_words:
            print(score, username)
            print(User.objects.get(username=username))
            filtered_users.append(User.objects.get(username=username))
        print(filtered_users)
        users = filtered_users
    users = list(users)
    return render(response, "users/users.html", {'users':users})