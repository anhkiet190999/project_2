--1 Insert yourself as a New Customer. Do not provide the CustomerID in your query
INSERT INTO CUSTOMER(Name, Phone)
VALUES ('H. Pham', '(682) 772-0172');


--2 Update your phone number to (837) 721-8965
UPDATE CUSTOMER
SET Phone = '(837) 721-8965'
where Name = 'H. Pham';

--3 Increase only daily rates for luxury vehicles by 5%
UPDATE RATE
SET Daily = Daily * 1.05
WHERE Category = 1;

--4a Insert a new luxury van with the following info: Honda Odyssey 2019, vehicle id: 5FNRL6H58KB133711
INSERT INTO VEHICLE
VALUES('5FNRL6H58KB133711', 'Honda Odyssey', '2019', 6, 1);

--4b You also need to insert the following rates:
-----------------------------------------
--  5   |   1   |   900.00  |   150.00  |
--  6   |   1   |   800.00  |   135.00  |
-----------------------------------------
INSERT INTO RATE
VALUES(5, 1, 900.00, 150.00);

INSERT INTO RATE
VALUES(6, 1, 800.00, 135.00);

--5 Return all Compact(1) & Luxury(1) vehivles that were available for rent from June 01, 2019 until Jun 20, 2019.
-- List VechicleID as VIN VIN, Description, year, and how many days have been rented so far. You need to change the weeks into days
SELECT V.VehicleID as VIN, Description, Year, SUM((RentalType * Qty)) as daysRented
FROM VEHICLE V LEFT NATURAL JOIN RENTAL R
WHERE Type = 1 AND Category = 1
    AND V.VehicleID NOT IN (SELECT VehicleID FROM RENTAL 
                            WHERE (StartDate >= '2019-06-1' AND StartDate <= '2019-06-20') 
                            OR (ReturnDate >= '2019-06-1' AND ReturnDate <= '2019-06-20'))
GROUP BY VIN;
--EITHER ABOVE

--OR

-- left join because the car which currently not in rental table will also be available
CREATE VIEW CAR_RENTED_DAYS
AS SELECT VehicleID as VIN, sum((RentalType*Qty)) as daysRented
FROM VEHICLE LEFT NATURAL JOIN RENTAL
WHERE Type = 1 AND Category = 1
GROUP BY VIN;

SELECT DISTINCT V.VehicleID as VIN, Description, Year, daysRented
FROM VEHICLE V, CAR_RENTED_DAYS
WHERE V.VehicleID = VIN 
    AND V.VehicleID NOT IN (SELECT VehicleID FROM RENTAL 
                           WHERE (StartDate >= '2019-06-1' AND StartDate <= '2019-06-20') 
                           OR (ReturnDate >= '2019-06-1' AND ReturnDate <= '2019-06-20'));


--6 Retrun a list with the remaining balance for the customer with the id '221'. 
--List customer name, and the balance
SELECT Name, TotalAmount as remaining_balance
FROM CUSTOMER NATURAL JOIN RENTAL
WHERE CustID = '221' and PaymentDate = 'NULL';


--Type: 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN  
--7 Create a report that will return all vehicles. List the VehicleID as VIN, Description, Year, Type, Category,
-- and Weekly and Daily rates. For the vehicle Type and Category, you need to use the SQL Case statement to substitude the number with text
-- Order your results based on Category (first Luxury and then Basic) and Type based on the Type number, not the text
SELECT V.VehicleID as VIN, Description, Year,
    CASE V.Type 
        WHEN 1 THEN 'Compact'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'Large'
        WHEN 4 THEN 'SUV'
        WHEN 5 THEN 'Truck'
        WHEN 6 THEN 'VAN'
    END Type,
    CASE V.Category
        WHEN 0 THEN 'Basic'
        WHEN 1 THEN 'Luxury'
    END Category,
    Weekly, Daily
FROM VEHICLE V, RATE R
WHERE V.Type = R.Type and V.category = R.category
Order BY V.Category DESC, V.Type;

--8 What is the total of money that customers paid to us until today?
SELECT sum(TotalAmount) AS Total_money
FROM RENTAL
WHERE PaymentDate < DATE('now') AND PaymentDate NOT NULL;

--9a Create a report for the J.Brown customer with all vehicles he rented. List the description, year, type, and category.
--Also, calculate the unit price for every rental, the total duration memtion if it is on weeks or days, the total amount,
-- and if there is any payment. Similarly, as in Question 7, you need to change the numeric values to the coresspoindint text.
--Order the results by StartDate
SELECT V.Description, V.Year,
    CASE V.Type 
        WHEN 1 THEN 'Compact'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'Large'
        WHEN 4 THEN 'SUV'
        WHEN 5 THEN 'Truck'
        WHEN 6 THEN 'VAN'
    END Type,
    CASE V.Category
        WHEN 0 THEN 'Basic'
        WHEN 1 THEN 'Luxury'
    END Category,
    ----check this unit price?????
    CASE R.RentalType
        WHEN 1 THEN RATE.Daily
        WHEN 7 THEN RATE.Weekly
    END UnitPrice,
    CASE R.RentalType
        WHEN 1 THEN R.Qty || ' days'
        WHEN 7 THEN R.Qty || ' weeks'
    END Duration,
    R.TotalAmount , R.PaymentDate 
FROM CUSTOMER C, VEHICLE V, RENTAL R, RATE
WHERE C.CustID = R.CustID AND C.Name = 'J. Brown' AND V.VehicleID = R.VehicleID 
      AND V.type = RATE.Type and V.Category = RATE.Category
ORDER BY StartDate;


--9b For the same customer return the current balance.
SELECT Name, SUM(TotalAmount) as current_balance
FROM CUSTOMER NATURAL JOIN RENTAL
WHERE Name = 'J. Brown' and PaymentDate = 'NULL'
GROUP BY CustID;

--10 Retrieve all weekly rentals for the vehicleID '19VDE1F3XEE414842' that are not paid yet.
--List the Customer Name, the start and return date, and the amount
SELECT Name, StartDate, ReturnDate, TotalAmount
FROM CUSTOMER NATURAL JOIN RENTAL
WHERE VehicleID = '19VDE1F3XEE414842' and PaymentDate = 'NULL';

--11 Return all customers that they never rent a cehicle
SELECT * FROM CUSTOMER 
WHERE CustID NOT IN (SELECT CustID FROM RENTAL);

--12 Return all rentals that the customer paid on the StartDate. List Customer Name, Vehicle Description, 
-- StartDate, ReturnDate, and TotalAmount. Order by Customer Name
 SELECT Name, Description, StartDate, ReturnDate, TotalAmount
 FROM CUSTOMER NATURAL JOIN RENTAL NATURAL JOIN VEHICLE
 WHERE StartDate = PaymentDate
 ORDER BY Name;