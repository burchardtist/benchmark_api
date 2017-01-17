CREATE TABLE benchmark(
    id serial PRIMARY KEY NOT NULL,
    benchmark_date timestamp DEFAULT CURRENT_TIMESTAMP,
    status varchar(50),
    db_system varchar(50),
    db_name varchar(50),
    score decimal(7, 3),
    insert_time decimal(7, 3),
    insert_index_time decimal(7, 3),
    select_time decimal(7, 3),
    select_index_time decimal(7, 3),
    update_time decimal(7, 3),
    update_index_time decimal(7, 3)
);