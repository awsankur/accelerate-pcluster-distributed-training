ARG BASE_IMAGE

FROM $BASE_IMAGE

LABEL description="Latest PyTorch DALI container"

ENV PYTHONUNBUFFERED=TRUE

ENV PYTHONDONTWRITEBYTECODE=TRUE
    
# Install other python libraries
RUN pip install tifffile==2021.11.2 

COPY ./docker/ /test-dali/

WORKDIR /test-dali

#ENTRYPOINT ["python3", "/trace-model/trace-model.py"]

