###########
# BUILDER #
###########

# pull official base image
FROM python AS builder

# set work directory
WORKDIR /usr/src/prayerpulse

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update -y \
    && apt install -y postgresql postgresql-contrib netcat-traditional

# lint
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/prayerpulse/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python

# create directory for the prayerpulse user
RUN mkdir -p /home/prayerpulse

# create the prayerpulse user
RUN addgroup prayerpulse
RUN adduser --group prayerpulse prayerpulseuser

# create the appropriate directories
ENV HOME=/home/prayerpulse
ENV APP_HOME=/home/prayerpulse/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apt update -y && apt install -y netcat-traditional unzip
COPY --from=builder /usr/src/prayerpulse/wheels /wheels
COPY --from=builder /usr/src/prayerpulse/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the prayerpulse user
RUN chown -R prayerpulseuser:prayerpulse $APP_HOME

# change to the prayerpulse user
USER prayerpulseuser

# run entrypoint.sh
ENTRYPOINT ["/home/prayerpulse/web/entrypoint.sh"]