import faker

f = faker.Faker("zh-cn")




if __name__ == '__main__':
    print(f.sentence(100)[:-1])
    print(f.sentence(10)[:-1])
    print(f.image_url(1000,1110))