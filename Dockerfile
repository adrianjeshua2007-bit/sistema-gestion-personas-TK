FROM python:3.9-slim

# Instalar dependencias para Tkinter y X11
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    xauth \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# ✅ Crear directorio /app y dar permisos completos
RUN mkdir -p /app && chmod 777 /app
RUN mkdir -p /tmp && chmod 777 /tmp

# Configurar variables de entorno
ENV DISPLAY=host.docker.internal:0
ENV QT_X11_NO_MITSHM=1

WORKDIR /app

# Copiar todos los archivos
COPY . .

# ✅ Dar permisos completos a todos los archivos
RUN chmod -R 777 /app

CMD ["python", "sistema-gestion-personas.py"]