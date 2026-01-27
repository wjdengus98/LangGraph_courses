from dotenv import load_dotenv

load_dotenv()

from graph.graph import app

if __name__ == "__main__":
    print("Hello Advanced Rag")
    print(app.invoke(input = {"question" : "how to make pizza?"}))