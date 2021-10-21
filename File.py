def get_stop_words():
    with open("assets/stop_word.txt",'r') as f:
        return f.readline().split(" ")
