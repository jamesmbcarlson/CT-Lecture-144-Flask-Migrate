from faker import Faker
# from database import db
# from models.customer import Customer

fake = Faker()


from random import randint
def phone_number():
    # (XXX) XXX-XXXX
    numbers = [randint(0,9) for _ in range(10)]
    while numbers[0] in {0,1}:
        numbers[0] = randint(2,9)
    numbers.insert(0, '(')
    numbers.insert(4, ')')
    numbers.insert(5, ' ')
    numbers.insert(9, '-')
    return ''.join([str(num) for num in numbers])

customer_data = []
for _ in range(30):
    password = 'pass123'
    first_name = fake.first_name()
    last_name = fake.last_name()
    name = first_name + ' ' + last_name
    username = first_name[0].lower() + last_name.lower() 
    email = first_name.lower() + last_name[0].lower() + '@' + fake.free_email_domain()
    phone = phone_number()

    # new_customer = Customer(name=name, username=username, password=password, phone=phone, email=email)
    # db.session.add(new_customer)
    customer_data.append((name, username, password, email, phone))

print(customer_data)

# db.session.commit()
# print("Success!")

# print(username, password, name, email, phone)