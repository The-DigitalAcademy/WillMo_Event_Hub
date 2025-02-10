CREATE TABLE "Customers" (
  "contact" varchar,
  "name" varchar,
  "surname" varchar,
  "email" varchar,
  "password" varchar PRIMARY KEY
);

CREATE TABLE "Location" (
  "location_id" serial PRIMARY KEY,
  "province" varchar,
  "city" varchar,
  "venue_title" varchar,
  "google_maps" varchar
);

CREATE TABLE "Type" (
  "type_id" serial PRIMARY KEY,
  "type" varchar
);


CREATE TABLE "Category" (
  "category_id" serial PRIMARY KEY,
  "category" varchar
);


CREATE TABLE "Events" (
  "event_id" serial PRIMARY KEY,
  "capacity" integer,
  "quantity" integer,
  "start_date" date,
  "start_time" time,
  "description" varchar,
  "event_title" varchar,
  "location_id" integer,
  "category_id" integer,
  "price" float,
  "image" varchar,
  "event_url" varchar,
FOREIGN KEY ("location_id") REFERENCES "Location" ("location_id"),
FOREIGN KEY ("category_id") REFERENCES "Category" ("category_id")
);

CREATE TABLE "CustomerType" (
  "type_id" integer,
  "password" varchar,
  FOREIGN KEY ("type_id") REFERENCES "Type" ("type_id"),
  FOREIGN KEY ("password") REFERENCES "Customers" ("password")
);

CREATE TABLE "CustomerMap" (
  "password" varchar,
  "event_id" integer,
  FOREIGN KEY ("password") REFERENCES "Customers" ("password"),
    FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id")
);