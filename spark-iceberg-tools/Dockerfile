FROM spark:3.5.1-scala2.12-java17-ubuntu

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip; \
    rm -rf /var/lib/apt/lists/*

RUN pip install argparse pyyaml

ADD --chown=spark:spark /jars/iceberg-spark-runtime-3.5_2.13-1.6.1.jar /opt/spark/jars/
ADD --chown=spark:spark /jars/iceberg-aws-bundle-1.5.0.jar /opt/spark/jars/
ADD --chown=spark:spark /jars/aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars/
ADD --chown=spark:spark /jars/hadoop-aws-3.3.4.jar /opt/spark/jars/
ADD --chown=spark:spark /jars/wildfly-openssl-java-1.0.7.Final.jar /opt/spark/jars/


COPY --chown=spark:spark properties/ /opt/spark/work-dir/default-properties

RUN mkdir -p /opt/spark/conf
COPY --chown=spark:spark sparkhome-properties/ /opt/spark/conf

# COPY --chown=spark:spark scripts/ /opt/spark/work-dir/scripts
RUN mkdir -p /opt/spark/work-dir/spark-event-log
# COPY --chown=spark:spark examples/ /opt/spark/work-dir/examples

COPY --chown=spark:spark sample_script.py /opt/spark/work-dir/scripts/
COPY --chown=spark:spark spark-iceberg-ingest-tranformer/ /opt/spark/work-dir/spark-iceberg-ingest-transformer/

USER spark

