FROM python

MAINTAINER sde-test <minghaolyu@gmail.com>

RUN pip install --upgrade pip && \
    pip install --no-cache-dir numpy

RUN  mkdir /submission



WORKDIR /submission

COPY . /usr/src/

ENTRYPOINT python /usr/src/bond.py $0 $1
