import random
import math

WIDTH = 500
HEIGHT = 500
TOTAL_STEPS = 1000

class Animal:
    def __init__(self, x, y, gender):
        self.x = x
        self.y = y
        self.gender = gender
        self.alive = True

    def move(self, max_step):
        dx = random.randint(-max_step, max_step)
        dy = random.randint(-max_step, max_step)
        # Alan sınırları içinde kal
        new_x = self.x + dx
        new_y = self.y + dy
        self.x = max(0, min(WIDTH - 1, new_x))
        self.y = max(0, min(HEIGHT - 1, new_y))

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

class Sheep(Animal):
    step = 2

class Wolf(Animal):
    step = 3

class Cow(Animal):
    step = 2

class Chicken(Animal):
    step = 1

class Rooster(Animal):
    step = 1

class Lion(Animal):
    step = 4

class Hunter(Animal):
    step = 1

def create_animals(cls, count, male_count=None, female_count=None):
    animals = []
    if male_count is not None and female_count is not None:
        # Belirli sayıda erkek ve dişi oluştur
        for _ in range(male_count):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            animals.append(cls(x, y, "M"))
        for _ in range(female_count):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            animals.append(cls(x, y, "F"))
    else:
        # Rastgele cinsiyet dağılımı
        for _ in range(count):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            gender = random.choice(["M", "F"])
            animals.append(cls(x, y, gender))
    return animals

def check_reproduction(animal_list, cls, max_new_animals=3):
    """Üreme kontrolü - daha gerçekçi kontroller"""
    new_animals = []
    paired = set()
    new_count = 0

    # Sadece yaşayan hayvanları kontrol et
    living_animals = [a for a in animal_list if a.alive]
    
    # Çok fazla hayvan varsa üreme yapma
    if len(living_animals) > 100:
        return 0
    
    for i in range(len(living_animals)):
        if new_count >= max_new_animals:
            break
            
        a1 = living_animals[i]
        if i in paired:
            continue

        for j in range(i + 1, len(living_animals)):
            if new_count >= max_new_animals:
                break
                
            a2 = living_animals[j]
            if j in paired:
                continue

            if a1.gender != a2.gender and a1.distance_to(a2) <= 3:
                # %30 şansla üreme gerçekleşir
                if random.random() < 0.3:
                    x = int((a1.x + a2.x) / 2)
                    y = int((a1.y + a2.y) / 2)
                    gender = random.choice(["M", "F"])
                    new_animal = cls(x, y, gender)
                    new_animals.append(new_animal)

                    paired.add(i)
                    paired.add(j)
                    new_count += 1
                    break

    animal_list.extend(new_animals)
    return len(new_animals)

def simulate():
    # Başlangıç hayvanları - belirtilen sayıda erkek/dişi
    sheeps = create_animals(Sheep, 30, 15, 15)  # 15 erkek, 15 dişi
    cows = create_animals(Cow, 10, 5, 5)        # 5 erkek, 5 dişi
    chickens = create_animals(Chicken, 10, 5, 5) # 5 erkek, 5 dişi tavuk
    roosters = create_animals(Rooster, 10, 5, 5) # 5 erkek, 5 dişi horoz
    wolves = create_animals(Wolf, 10, 5, 5)     # 5 erkek, 5 dişi
    lions = create_animals(Lion, 8, 4, 4)       # 4 erkek, 4 dişi
    hunters = create_animals(Hunter, 1)         # 1 avcı

    print("Hayvanat Bahçesi Projesi")
    print("1000 birim hareket simülasyonu başlıyor...")
    print(f"Başlangıç hayvan sayıları:")
    print(f"Koyun: 30 (15 erkek, 15 dişi)")
    print(f"İnek: 10 (5 erkek, 5 dişi)")
    print(f"Tavuk: 10 (5 erkek, 5 dişi)")
    print(f"Horoz: 10 (5 erkek, 5 dişi)")
    print(f"Kurt: 10 (5 erkek, 5 dişi)")
    print(f"Aslan: 8 (4 erkek, 4 dişi)")
    print(f"Avcı: 1")

    for step in range(TOTAL_STEPS):
        # Hareket ettir
        for animal in sheeps + cows + chickens + roosters + wolves + lions + hunters:
            if animal.alive:
                animal.move(animal.__class__.step)

        # Kurt avlar (4 birim mesafe) - koyun, tavuk, horoz
        for wolf in wolves:
            if not wolf.alive:
                continue
            for prey_list in [sheeps, chickens, roosters]:
                for prey in prey_list:
                    if prey.alive and wolf.distance_to(prey) <= 4:
                        prey.alive = False
                        break  # Bir kurt bir avı avlar

        # Aslan avlar (5 birim mesafe) - inek, koyun
        for lion in lions:
            if not lion.alive:
                continue
            for prey_list in [cows, sheeps]:
                for prey in prey_list:
                    if prey.alive and lion.distance_to(prey) <= 5:
                        prey.alive = False
                        break  # Bir aslan bir avı avlar

        # Avcı avlar (8 birim mesafe) - tüm hayvanlar (avcı hariç)
        for hunter in hunters:
            if not hunter.alive:
                continue
            for prey_list in [sheeps, cows, chickens, roosters, wolves, lions]:
                for prey in prey_list:
                    if prey.alive and hunter.distance_to(prey) <= 8:
                        prey.alive = False
                        break  # Bir avcı bir avı avlar

        # Üreme (her 20 adımda bir)
        if step % 20 == 0:
            check_reproduction(sheeps, Sheep, max_new_animals=2)
            check_reproduction(cows, Cow, max_new_animals=1)
            check_reproduction(chickens, Chicken, max_new_animals=1)
            check_reproduction(roosters, Rooster, max_new_animals=1)
            check_reproduction(wolves, Wolf, max_new_animals=1)
            check_reproduction(lions, Lion, max_new_animals=1)

    # Final sonuçları
    print(f"\n1000 birim hareket sonunda hayvanların sayısı:")
    print(f"Koyun: {sum(1 for a in sheeps if a.alive)}")
    print(f"İnek: {sum(1 for a in cows if a.alive)}")
    print(f"Tavuk: {sum(1 for a in chickens if a.alive)}")
    print(f"Horoz: {sum(1 for a in roosters if a.alive)}")
    print(f"Kurt: {sum(1 for a in wolves if a.alive)}")
    print(f"Aslan: {sum(1 for a in lions if a.alive)}")
    print(f"Avcı: {sum(1 for a in hunters if a.alive)}")
    
    total_animals = (sum(1 for a in sheeps if a.alive) + 
                    sum(1 for a in cows if a.alive) + 
                    sum(1 for a in chickens if a.alive) + 
                    sum(1 for a in roosters if a.alive) + 
                    sum(1 for a in wolves if a.alive) + 
                    sum(1 for a in lions if a.alive) + 
                    sum(1 for a in hunters if a.alive))
    
    print(f"\nToplam hayvan sayısı: {total_animals}")

if __name__ == "__main__":
    simulate()
