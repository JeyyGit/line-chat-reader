with open("chat.txt", "r", encoding="utf8") as f:
    chat = f.readlines()

data = {}

for line in chat[4:]:
    try:
        time, person, text = line.strip("\n").split("\t")
        # print(time, person, text)
        data.setdefault(person, {})

        words = text.split()
        for word in words:
            data[person].setdefault(word, 0)
            data[person][word] += 1
    except:
        pass

with open('res.txt', "w", encoding="utf8") as f:
    for person, words in data.items():
        f.write(f"Person: {person}\n")
        
        for word, word_count in sorted(tuple(words.items()), key=lambda i: i[1], reverse=True):
            # print(word, word_count)
            f.write(f"{word}\t{word_count}\n")
