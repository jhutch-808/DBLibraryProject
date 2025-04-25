CREATE TABLE Author(
	First_Name varchar(50),
	Last_Name varchar(50),
	Publisher varchar(50),
    AuthorID int PRIMARY KEY
);

CREATE TABLE Book(
	ISBN int PRIMARY KEY, 
	Title varchar(50),
	Genre varchar(50),
    AuthorID int,
	Status boolean,
	Publisher varchar(50),
	Pub_date timestamp, 
    FOREIGN KEY (AuthorID) References Author(AuthorID)
);


CREATE TABLE Users(
	Lib_ID int,
	First_Name varchar(50),
	Last_Name varchar(50),
	PRIMARY KEY(Lib_ID)
);

CREATE TABLE Hold(
    ISBN int,
	DayHeld DATE,
	DayHoldExpire DATE, 
	DayOut DATE,
    Lib_ID int,
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
    FOREIGN KEY (Lib_ID) REFERENCES Users(Lib_ID),
	PRIMARY KEY(ISBN,Lib_ID, DayHeld)
);

CREATE TABLE Patron(
    Lib_ID int,
	FavGenre varchar(50),
	Address varchar(50),
	City varchar(50),
	State varchar(50),
    FOREIGN KEY (Lib_ID) REFERENCES Users(Lib_ID),
	PRIMARY KEY(Lib_ID)
);

CREATE TABLE Staff(
    Lib_ID int,
	Role varchar(50),
	CellNum int,
    FOREIGN KEY (Lib_ID) REFERENCES Users(Lib_ID),
	PRIMARY KEY(Lib_ID)
);

CREATE TABLE Checkout(
    ISBN int,
	Lib_ID int, 
	DayOut DATE,
	DayDue DATE,
	DayReturned DATE,
    FOREIGN KEY (ISBN) REFERENCES Book(ISBN),
	PRIMARY KEY(ISBN, DayOut, Lib_ID)
);
	
CREATE TABLE Rating(
    ISBN int,
    Lib_ID int, 
	Rating int check(Rating between 0 and 5),
	Review_text varchar(100),
    FOREIGN KEY (ISBN) References Book(ISBN),
	FOREIGN KEY (Lib_ID) References Users(Lib_ID),
	PRIMARY KEY(ISBN, Lib_ID)
);

CREATE TABLE CreditCard(
    Lib_ID int,
	Credit_card_num Bigint,
	Exp_date DATE, 
	Pin smallint, 
	Zipcode int,
    FOREIGN KEY (Lib_ID) References Users(Lib_ID),
	PRIMARY KEY (Credit_card_num, Lib_ID)
);
