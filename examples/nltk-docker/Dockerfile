FROM quay.io/vanessa/qme
LABEL MAINTAINER @vsoch
# docker build -t quay.io/vanessa/nltk-qme .
RUN pip install nltk && \
    mkdir ~/nltk_data && \
    mkdir ~/nltk_data/chunkers && \
    mkdir ~/nltk_data/corpora && \
    mkdir ~/nltk_data/taggers && \
    mkdir ~/nltk_data/tokenizers && \
    python -c "import nltk; nltk.download(['brown', 'gutenberg', 'reuters', 'inaugural', 'punkt'])"
EXPOSE 5000
WORKDIR /code
COPY ./script.py /code/run.py
