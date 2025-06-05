FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional: if you need to prepare assets or DB here (rare)
# RUN python prepare.py

# Don't run ad.py here!
# RUN python ad.py ❌

CMD ["python", "adbot.py"]
