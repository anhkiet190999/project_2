--query 1
ALTER TABLE RENTAL ADD Returned INT;

UPDATE RENTAL
SET Returned = CASE PaymentDate
WHEN 'NULL' THEN 0
ELSE 1
END;

--query 2
CREATE VIEW RentalInfo AS
SELECT OrderDate, StartDate, ReturnDate, RentalType * Qty as TotalDays, VehicleID as VIN,
    Description as Vehicle,
    CASE Type
        WHEN 1 THEN 'Compact'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'Large'
        WHEN 4 THEN 'SUV'
        WHEN 5 THEN 'Truck'
        WHEN 6 THEN 'VAN'
    END Type,
    CASE Category
        WHEN 0 THEN 'Basic'
        WHEN 1 THEN 'Luxury'
    END Category,
    CustID as CustomerID, Name as CustomerName, TotalAmount as OrderAmount,
    CASE PaymentDate
        WHEN 'NULL' THEN 0
        ELSE TotalAmount
    END RentalBalance
FROM CUSTOMER NATURAL JOIN RENTAL NATURAL JOIN VEHICLE NATURAL JOIN RATE
ORDER BY StartDate;
