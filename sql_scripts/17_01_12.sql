CREATE TABLE benchmark(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    benchmark_date datetime DEFAULT CURRENT_TIMESTAMP,
    status varchar(50),
    result decimal(7, 3),
    db_system varchar(50),
    db_name varchar(50)
);