CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.numbers_kafka (
    value Int64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'numbers',
    kafka_group_name = 'numbers_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1;

CREATE TABLE IF NOT EXISTS analytics.numbers (
    value Int64,
    ts DateTime DEFAULT now()
) ENGINE = MergeTree
ORDER BY ts;

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.numbers_mv
TO analytics.numbers AS
SELECT value, now() AS ts
FROM analytics.numbers_kafka;

CREATE TABLE IF NOT EXISTS analytics.numbers_sign_sum (
    sum_positive Int64,
    sum_negative Int64
) ENGINE = SummingMergeTree
ORDER BY tuple();

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.numbers_sign_sum_mv
TO analytics.numbers_sign_sum AS
SELECT
    if(value > 0, value, 0) AS sum_positive,
    if(value < 0, value, 0) AS sum_negative
FROM analytics.numbers;

CREATE TABLE IF NOT EXISTS analytics.numbers_dlq_kafka (
    raw String,
    reason String,
    ts DateTime
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'numbers_dlq',
    kafka_group_name = 'numbers_dlq_consumer',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1;

CREATE TABLE IF NOT EXISTS analytics.numbers_dlq (
    raw String,
    reason String,
    ts DateTime
) ENGINE = MergeTree
ORDER BY ts;

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.numbers_dlq_mv
TO analytics.numbers_dlq AS
SELECT raw, reason, ts
FROM analytics.numbers_dlq_kafka;
