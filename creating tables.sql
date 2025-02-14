CREATE TABLE "Customers" (
  "contact" varchar,
  "name" varchar,
  "surname" varchar,
  "email" varchar PRIMARY KEY,
  "password" varchar
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

CREATE TABLE "Organizer" (
  "organizer_id" serial PRIMARY KEY,
  "email" varchar,
  "bank_name" varchar,
  "bank_account_number" varchar,
  "account_holder_name" varchar,
  "bank_code" varchar,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email")
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
  "organizer_id" integer,
  "cart_id" integer,
  FOREIGN KEY ("location_id") REFERENCES "Location" ("location_id"),
  FOREIGN KEY ("category_id") REFERENCES "Category" ("category_id"),
  FOREIGN KEY ("organizer_id") REFERENCES "Organizer" ("organizer_id"),
  FOREIGN KEY ("cart_id") REFERENCES "Cart" ("cart_id"),
  FOREIGN KEY ("booking_id") REFERENCES "Bookings" ("booking_id")
);

CREATE TABLE "Cart" (
  "cart_id" serial PRIMARY KEY,
  "email" varchar,
  "cart_quantity" integer,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),
);

CREATE TABLE "Bookings" (
  "booking_id" serial PRIMARY KEY,
  "email" varchar,
  "event_id" integer,
  "booking_date" timestamp default current_timestamp,
  "status" varchar default 'pending' CHECK ("status" IN ('pending', 'confirmed')),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email")
);

CREATE TABLE "CustomerType" (
  "type_id" integer,
  "email" varchar,
  PRIMARY KEY ("type_id", "email"),
  FOREIGN KEY ("type_id") REFERENCES "Type" ("type_id"),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email")
);

CREATE TABLE "CustomerMap" (
  "email" varchar,
  "event_id" integer,
  PRIMARY KEY ("email", "event_id"),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id")
);

CREATE TABLE "BookingEventMap" (
  "booking_id" integer,
  "event_id" integer,
  PRIMARY KEY ("booking_id", "event_id"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id"),
  FOREIGN KEY ("booking_id") REFERENCES "Bookings" ("booking_id")
);