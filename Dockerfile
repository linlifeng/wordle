FROM python
COPY ./ /

ENTRYPOINT ["python", "wordle.py"]
