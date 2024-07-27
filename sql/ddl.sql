create database disaster_db
    with owner prayitnaadmin;

create table public.disaster_records
(
    id          bigserial
        constraint disaster_records_pk
            primary key,
    description varchar,
    severity    smallint,
    scale       smallint,
    longitude   numeric(4, 12),
    latitude    numeric(4, 12),
    type        varchar,
    timestamp   timestamp not null
);

alter table public.disaster_records
    owner to prayitnaadmin;

create index disaster_records_timestamp_index
    on public.disaster_records (timestamp desc);

create table public.disaster_reports
(
    id                bigserial
        constraint disaster_reports_pk
            primary key,
    reporter_uniqueid varchar        not null,
    longitude         numeric(4, 12) not null,
    latitude          numeric(4, 12) not null,
    geohash           varchar        not null,
    type              varchar        not null,
    timestamp         timestamp      not null
);

alter table public.disaster_reports
    owner to prayitnaadmin;

create index disaster_reports_timestamp_index
    on public.disaster_reports (timestamp desc);

