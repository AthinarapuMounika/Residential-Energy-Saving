import bcrypt

password = "mouni123"  # Replace with your desired password
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print("Your bcrypt hash:")
print(hashed.decode())