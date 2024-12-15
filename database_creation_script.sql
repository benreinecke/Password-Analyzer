CREATE TABLE [User] (
    userID INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(MAX) NOT NULL,
    password NVARCHAR(MAX) NOT NULL
);

CREATE TABLE Password (
    passwordID INT IDENTITY(1,1) PRIMARY KEY,
    oldPassword VARBINARY(MAX) NOT NULL,
    newPassword VARBINARY(MAX) NOT NULL,
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES [User](userID)
);