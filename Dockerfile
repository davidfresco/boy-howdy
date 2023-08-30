FROM python:3

ARG version

WORKDIR /root/

COPY ${version} ./
RUN pip install --no-cache-dir -r ./python_packages.txt

RUN apt update

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

CMD [ "flask", "--app=api.py", "run", "--host=0.0.0.0" ]
