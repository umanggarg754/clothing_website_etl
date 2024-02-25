create table company_profiles (
    id serial primary key ,
    url text unique ,
    country varchar(2),
    name varchar(100),
    phones text[],
    emails text[],
    categories_served text[],
    page_views jsonb,
    geographies_served jsonb,
    social_media jsonb,
    links jsonb,
    "createdAt" timestamp default now(),
    "updatedAt" timestamp
);

create table sku_details (
    id serial primary key ,
    company_id int REFERENCES company_profiles (id),
    url text unique,
    name text,
    images text[],
    colour text,
    price int,
    currency varchar(5),
    silhouette text,
    size text,
    care text,
    composition text,
    "createdAt" timestamp default now(),
    "updatedAt" timestamp
);