from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates

import uuid
import time

app = FastAPI()

templates = Jinja2Templates("templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/data")
async def read_data(request: Request, chat_file: UploadFile = File(...)):
    byte = await chat_file.read()
    chat = byte.decode().split("\n")

    t = time.perf_counter()
    data = {}
    combined = {}
    for line in chat[4:]:
        try:
            ts, person, text = line.strip("\n").split("\t")
            data.setdefault(person, {})

            words = text.split()
            for word in words:
                combined.setdefault(word, 0)
                combined[word] += 1

                data[person].setdefault(word, 0)
                data[person][word] += 1
        except:
            pass

    data["all"] = combined

    new_data = {}
    for person, words in data.items():
        new_data.setdefault(person, {"id": uuid.uuid4(), "words": []})
        for word, word_count in sorted(tuple(words.items()), key=lambda i: i[1], reverse=True):
            new_data[person]["words"].append((word, word_count))

    print(time.perf_counter() - t)
    return templates.TemplateResponse(request, "index.html", {"data": new_data})