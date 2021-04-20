ARG src=stage0

FROM superelastix/elastix:5.0.1 AS elastix

FROM python:3.8

RUN pip install numpy pandas pyimzml nibabel scipy h5py

FROM elastix

COPY --from=elastix . .

COPY . /app/