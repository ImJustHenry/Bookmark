FROM python:3.11.5
WORKDIR /usr/src/app
RUN git clone https://github.com/ImJustHenry/Bookmark.git
RUN pip install -r ./Bookmark/requirements.txt
CMD ["python", "./Bookmark/src/flask_server.py"]