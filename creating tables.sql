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

CREATE TABLE "Customers" (
  "contact" varchar,
  "name" varchar,
  "surname" varchar,
  "email" varchar PRIMARY KEY,
  "password" varchar
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
  FOREIGN KEY ("email") REFERENCES "Customers" ("email") ON DELETE CASCADE
);

CREATE TABLE "Events" (
  "event_id" serial PRIMARY KEY,
  "capacity" integer,
  "quantity" integer,
  "start_date" date,
  "start_time" time,
  "description" varchar,
  "event_title" varchar UNIQUE,
  "location_id" integer,
  "category_id" integer,
  "price" float CHECK ("price" >= 0),
  "image" varchar,
  "event_url" varchar,
  "organizer_id" integer,
  FOREIGN KEY ("location_id") REFERENCES "Location" ("location_id") ON DELETE CASCADE,
  FOREIGN KEY ("category_id") REFERENCES "Category" ("category_id") ON DELETE CASCADE,
  FOREIGN KEY ("organizer_id") REFERENCES "Organizer" ("organizer_id") ON DELETE CASCADE
);

CREATE TABLE "Cart" (
  "cart_id" serial PRIMARY KEY,
  "email" varchar,
  "event_id" integer,
  "cart_quantity" integer CHECK ("cart_quantity" > 0),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email") ON DELETE CASCADE,
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id") ON DELETE CASCADE
);

CREATE TABLE "Bookings" (
  "booking_id" serial PRIMARY KEY,
  "email" varchar,
  "event_id" integer,
  "booking_date" timestamp DEFAULT current_timestamp,
  "status" varchar DEFAULT 'pending' CHECK ("status" IN ('pending', 'confirmed')),
  FOREIGN KEY ("email") REFERENCES "Customers" ("email") ON DELETE CASCADE,
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id") ON DELETE CASCADE
);

CREATE TABLE "CustomerType" (
  "type_id" integer,
  "email" varchar,
  PRIMARY KEY ("type_id", "email"),
  FOREIGN KEY ("type_id") REFERENCES "Type" ("type_id") ON DELETE CASCADE,
  FOREIGN KEY ("email") REFERENCES "Customers" ("email") ON DELETE CASCADE
);

CREATE TABLE "BookingEventMap" (
  "booking_id" integer,
  "event_id" integer,
  PRIMARY KEY ("booking_id", "event_id"),
  FOREIGN KEY ("event_id") REFERENCES "Events" ("event_id") ON DELETE CASCADE,
  FOREIGN KEY ("booking_id") REFERENCES "Bookings" ("booking_id") ON DELETE CASCADE
);
