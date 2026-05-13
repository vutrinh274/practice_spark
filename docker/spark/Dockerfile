FROM apache/spark:4.0.0-python3

USER root

RUN pip install pyspark==4.0.0

EXPOSE 15002

CMD ["/opt/spark/sbin/start-connect-server.sh", \
     "--conf", "spark.connect.grpc.binding.port=15002", \
     "--conf", "spark.scheduler.mode=FAIR"]
