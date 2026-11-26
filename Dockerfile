
FROM python:3.12-slim

RUN useradd -m -u 1000 usuario
USER usuario
ENV PATH=/home/usuario/.local/bin:$PATH
WORKDIR /home/usuario/app

COPY --chown=usuario requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=usuario . .

EXPOSE 8765
CMD ["solara", "run", "app.py", "--host=0.0.0.0", "--production"]