import faker

f = faker.Faker("zh-cn")

if __name__ == '__main__':
    for _ in range(10):

        print(f.date())

