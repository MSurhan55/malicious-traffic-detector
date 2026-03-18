from google import genai

client = genai.Client(api_key="AIzaSyDhwdiXlvYdSqwhfUNADGQF0sjoQO4ZT5Q")

for model in client.models.list():
    print(model.name)
