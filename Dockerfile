# Dockerfile (modified frontend-builder section)
FROM node:20-slim AS frontend-builder

WORKDIR /app

COPY package*.json ./
RUN npm install

# Copy tailwind config and the static sources
COPY tailwind.config.js ./
COPY static ./static

# Copy Django templates and app template directories so Tailwind can see them
COPY templates ./templates
COPY club ./club
COPY membership ./membership
COPY post ./post
COPY user ./user

RUN npm run build


# =========================
# Stage 2: Python runtime
# =========================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# ✅ Copy ONLY the built CSS from Node stage
COPY --from=frontend-builder /app/static/css/output.css ./static/css/output.css

# Collect static
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "clubmania.wsgi:application", "--bind", "0.0.0.0:8000"]
