import faker

f = faker.Faker("zh-cn")

if __name__ == '__main__':
    for _ in range(10):
        print(f.date())
        print(f.email())
        print(f.phone_number())
        print(f.name())


