FROM python:3.8-slim

WORKDIR /app
COPY actions /app/actions
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5055
CMD ["rasa", "run", "actions"]