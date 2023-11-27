from faker import Faker

from app.models import MeetingRoom, Employee


fake = Faker()

for i in range(8):
    name = fake.word() + " Room"
    max_attendees = fake.random_int(min=1, max=20)
    is_tv = fake.boolean(chance_of_getting_true=40)

    MeetingRoom.objects.create(name=name, max_attendees=max_attendees, is_tv=is_tv)


for i in range(8):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    Employee.objects.create(username=username, email=email, password=password)
