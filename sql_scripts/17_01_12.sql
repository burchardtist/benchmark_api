CREATE DATABASE benchmark_api;

CREATE TABLE benchmark(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    benchmark_date datetime DEFAULT CURRENT_TIMESTAMP,
    status varchar(50)
);