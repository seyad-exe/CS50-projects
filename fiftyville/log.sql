-- Keep a log of any SQL queries you execute as you solve the mystery.
.schema --looking at all the tables
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street'; --brian told me to do this
SELECT * FROM interviews WHERE month = 7 AND day = 28; -- looking at the interviews
--theft toook place at 10:15 am
--look at cars that left from bakery 10 mins after 10:15am
--b4 10:15 am thief took money from ATM at Leggett street
--phone call after 10:15 am less than a min, they plan on taking earliest flight out of ftville, accomplice made purchase
SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit'; --finding the number plate
SELECT name FROM people WHERE license_plate IN(SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit');
--that tells us the name of the 8 suspects for the thief
SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location LIKE 'Leggett street'; --accounts that took money on the street the thief also took money from
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number  FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location LIKE 'Leggett street');
-- finding the person id of the ppl who withdrew money
SELECT name FROM people WHERE id IN(SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number  FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location LIKE 'Leggett street'));
--names of the people who withdrew money on legget street
--suspects: Iman,Luca,Diana,Bruce
SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 ; --phone calls less than a min
SELECT name FROM people WHERE phone_number IN(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60) ; -- finding the caller name
--suspects: Diana and Bruce
SELECT name FROM people WHERE phone_number IN(SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller IN(SELECT phone_number FROM people WHERE name = 'Diana')) ;
--query shows who diana called
--Diana called Philip
SELECT name FROM people WHERE phone_number IN(SELECT receiver FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60 AND caller IN(SELECT phone_number FROM people WHERE name = 'Bruce')) ;
--query shows who Bruce called
--Bruce called Robin
--Either Diana and Philip OR Bruce and Robin
SELECT * FROM atm_transactions WHERE account_number IN(SELECT account_number FROM bank_accounts WHERE person_id IN(SELECT id FROM people WHERE name = 'Robin'));
SELECT * FROM atm_transactions WHERE account_number IN(SELECT account_number FROM bank_accounts WHERE person_id IN(SELECT id FROM people WHERE name = 'Philip'));
SELECT id FROM flights WHERE month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1; --earliest flight out of fiftyville
 SELECT name FROM people WHERE passport_number IN(SELECT passport_number FROM passengers WHERE flight_id = 36);