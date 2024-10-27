import sqlite3

def print_data(data):
    for i in data:
        print(i)
# If doesnt exist already, it creates it
db = sqlite3.connect('Companies.db')
db.execute("PRAGMA foreign_keys=on")

#Created the cursor
cursor = db.cursor()

#FORMAT TO CREATE A TABLE | INSERT COMMAND
# "CREATE TABLE nameOfTable(field1 type, field2 type)"

#Different Types:
# INT, REAL (float), TEXT, BOOL

#The SQLite database saves even after running the code
#so if i create the table once, if i run the code again and try to create another table, i get an error
# so to solve this, add the "if not exists" keyword so only creates the table if doesnt exist

cursor.execute("CREATE TABLE if not exists company(company_id INT PRIMARY KEY, company_name TEXT, company_budget REAL, num_employees INT)")
cursor.execute("CREATE TABLE if not exists branches(company_id INT, location TEXT, area REAL, FOREIGN KEY(company_id) REFERENCES company(company_id)), PRIMARY KEY(company_id, location)")

# Save the existing changes
db.commit()

#FORMAT TO ADD TO A TABLE | INSERT INTO

# FOR HARD CODED VALUES
# " INSERT INTO table_name values(x, y, z, b)"
# x, y, z, and b have to be of the right table and in the same order as their column order above
cursor.execute("INSERT INTO company values(123, 'Google', 23.7, 3000)")
cursor.execute("INSERT INTO company values(125, 'Amazon', 55.6, 3276)")


var_id = int(input("Enter company ID: "))
var_name = input("Enter company name: ")
var_budget = float(input("Enter company budget: "))
var_emp = int(input("Enter company employees: "))

# For variables ( not hardcode), put ? instead of the value
# " INSERT INTO table_name values(?, ?, ?, ?)", (x,y,b,z)
cursor.execute("INSERT INTO company values(?, ?, ? ,?)", (var_id, var_name, var_budget, var_emp))

db.commit()

# Remember to comment this after the first run since itll save there
cursor.execute("INSERT INTO branches values(123, 'Miami', 500)")
cursor.execute("INSERT INTO branches values(123, 'New York', 450)")
cursor.execute("INSERT INTO branches values(123, 'Detroit', 370)")
cursor.execute("INSERT INTO branches values(124, 'San Francisco', 600)")
cursor.execute("INSERT INTO branches values(124, 'Los Angeles', 289)")

db.commit()

#You can only use cursor.fetchall() once, right after the SELECT query
# if yo uwant to use it again, you have to execute the query again


# "SELECT * FROM company" || selects the entire table
cursor.execute("SELECT * FROM company")
print("All companies:")
print("----------------")
print_data(cursor.fetchall())

# "SELECT att1, att2 from table_name" || selects the first and second attributes from all the rows in that table
# "SELECT * from table_name WHERE att1=x" || selects only the rows where att1=x


# "SELECT * FROM company JOIN branches ON branches.company_id=company.company_id"
# So basically take all the columbs and join them with branches table since they have one common field
# by specifying we wnat to join the 2 tables by cominbing rows wherever company id is equal

# now this one, is the same as the one above, but here we notice that we'd have duplicate companyID field, so instead of selecting all, just take the unique fields
# and join them into one table, (cmopanyid, companyname, branch location, and branch area)
# ADD THE WHERE AT THE END
cursor.execute("SELECT company.company_id, company.company_name, branches.location, branches.area FROM company JOIN branches ON branches.company_id=company.company_id WHERE branches.area >450")
#basically, we're selecting these nique felects FROM the joined table of company and branches , joined at branches.company_id = company.company_id
print("Companies and branches with area greater than 450 square meter:")
print("----------------")
print_data(cursor.fetchall())


# so i want to display here the company id, and the COUNT(*)
#then grow them in order of their company_id

#Theres other functions other than COUNT like MAX() MIN() AVG()
cursor.execute("SELECT company_id, COUNT(*) FROM branches GROUP BY company_id")
print("Companies and their number of branches:")
print("----------------")
print_data(cursor.fetchall())

# You can order by any variable, and choose if desc or asec
cursor.execute("SELECT * FROM branches ORDER BY area desc")
print("Branches sorted by area in descending order:")
print("----------------")
print_data(cursor.fetchall())

# UPDATE KEYWORD
# UPDATE table_name SET att1=x, att2=y
# i can also add WHERE at the end so it only updates rows that meet that condition v
cursor.execute("UPDATE company SET company_budget=40.5, num_employees=3678 WHERE company_id=123")
print("Updated company with ID 123")

# Simple delete keyword
# specify the row or condition the row has to have to be deleted
cursor.execute("DELETE FROM company WHERE company_id=125")
print("Updated company with ID 125")
db.commit()

try:
    cursor.execute("INSERT INTO branches values(126, 'Boston', 320)")
    db.commit()
except:
    print("Tried to create a branch of a company that is non-existent")

db.close()