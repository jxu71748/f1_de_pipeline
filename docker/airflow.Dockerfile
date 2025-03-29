FROM apache/airflow:2.8.1

USER root

# Install Java（for Spark）
RUN apt-get update && apt-get install -y openjdk-17-jdk wget unzip && \
    apt-get clean

# Setup JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

# Install Spark
ENV SPARK_VERSION=3.5.0
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz


# Add Spark to PATH
ENV PATH=$PATH:/opt/spark/bin

# Get back to airflow user
USER airflow

# Install PySpark
RUN pip install pyspark==3.5.0
