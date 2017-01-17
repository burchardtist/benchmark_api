CREATE TABLE benchmark(
    id serial PRIMARY KEY NOT NULL,
    benchmark_date timestamp DEFAULT CURRENT_TIMESTAMP,
    status varchar(50),
    result decimal(7, 3),
    db_system varchar(50),
    db_name varchar(50)
);