FROM python:3.11.5
WORKDIR /usr/src/app
COPY . .
RUN pip install -r ./requirements.txt
EXPOSE 3000
CMD ["./control_scripts/start_server.sh"]