FROM frolvlad/alpine-python3

RUN pip3 install requests gspread timestring oauth2client

WORKDIR .
COPY . .

EXPOSE 8081

CMD python3 server.py
