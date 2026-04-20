import mysql.connector

def connect():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Ilmfsm06",
        database="BankingApplication"
    )

def setup():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id      INTEGER PRIMARY KEY AUTO_INCREMENT,
            name    TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database ready!")

def create_account():
    name = input("Enter name: ")
    balance = float(input("Enter initial deposit: $"))
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    conn.commit()
    conn.close()
    print(f"Account created for {name}!")

def deposit():
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter deposit amount: $"))
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    conn.commit()
    conn.close()
    print(f"${amount:.2f} deposited!")

def withdraw():
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter withdrawal amount: $"))
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    row = cursor.fetchone()
    if row is None:
        print("Account not found.")
    elif row[0] < amount:
        print(f"Insufficient funds. Balance: ${row[0]:.2f}")
    else:
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
        conn.commit()
        print(f"${amount:.2f} withdrawn!")
    conn.close()

def check_balance():
    account_id = int(input("Enter account ID: "))
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts WHERE id = %s", (account_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        print("Account not found.")
    else:
        print(f"Name: {row[0]} | Balance: ${row[1]:.2f}")

def list_accounts():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, balance FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    if len(rows) == 0:
        print("No accounts found.")
    else:
        print("\n--- All Accounts ---")
        for row in rows:
            print(f"  ID: {row[0]} | Name: {row[1]} | Balance: ${row[2]:.2f}")
        print("--------------------")

def menu():
    setup()
    while True:
        print("\n===== Banking App =====")
        print("1. Create new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check balance")
        print("5. List all accounts")
        print("6. Exit")
        print("=======================")
        choice = input("Choose an option (1-6): ")
        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            list_accounts()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose 1-6.")

if __name__ == "__main__":
    menu()