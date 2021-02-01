# inherit prebuilt image
FROM frost2k5/projectfizilion:latest

# env setup
RUN mkdir /Ryzo && chmod 777 /Ryzo
ENV PATH="/Ryzo/bin:$PATH"
WORKDIR /Ryzo

# clone repo
RUN git clone https://github.com/DhruvChhura/ProjectRyzo -b monster /Ryzo


# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Ryzo/

#transfer
RUN curl -sL https://git.io/file-transfer | sh

# install required pypi modules
RUN pip3 install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
