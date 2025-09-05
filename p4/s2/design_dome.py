import math

DENSITY = [2.4, 2.7, 7.85]
MATERIAL_ENG = {'glass': 0, 'aluminum': 1, 'carbon_steel': 2}
MATERIAL_KOR = {'유리': 0, '알루미늄': 1, '탄소강': 2}

area = 0
weight = 0


def get_mat_idx(name):
    if MATERIAL_ENG.keys().__contains__(name):
        return MATERIAL_ENG[name]
    if MATERIAL_KOR.keys().__contains__(name):
        return MATERIAL_KOR[name]
    raise ValueError(f'지원하지 않는 재질입니다: {name}')


def half_sphere_area(r):
    return 4 * math.pi * r * r / 2


def circle_area(r):
    return math.pi * r * r


def half_sphere_volume(r):
    return 2 * math.pi * r * r * r / 3


def validate(r, t):
    if r <= 0 or t <= 0:
        raise ValueError('지름과 두께는 0보다 큰 값을 입력하세요')
    if r <= t:
        raise ValueError('두께는 반지름보다 클 수 없습니다.')


def sphere_area(diameter, material, thickness=1):
    global area, weight

    mat_idx = get_mat_idx(material)
    density = DENSITY[mat_idx]
    d = density * 1000
    r = diameter / 2
    t = thickness / 100

    validate(r, t)

    # 2πr² + 2π(r-t)² + πr² - π(r-t)² = 3πr² + π(r-t)²
    # area = (
    #     half_sphere_area(r)
    #     + half_sphere_area(r - t)
    #     + circle_area(r)
    #     - circle_area(r - t)
    # )
    area = half_sphere_area(r)
    volume = half_sphere_volume(r) - half_sphere_volume(r - t)
    earth_weight = volume * d
    weight = earth_weight * 0.38


def main():
    while True:
        try:
            diameter = float(input('지름(m): '))
            material = input(
                '재질 (유리 glass, 알루미늄 aluminum, 탄소강 carbon_steel): '
            )
            thickness = input('두께(cm): ')
            if thickness == '':
                thickness = 1
                sphere_area(diameter, material)
            else:
                thickness = float(thickness)
                sphere_area(diameter, material, thickness)
            print(
                f'재질 ⇒ {material}, 지름 ⇒ {diameter:.3f},',
                f'두께 ⇒ {thickness:.3f}, 면적 ⇒ {area:.3f}, 무게 ⇒ {weight:.3f} kg',
            )
            exit_key = input('계속하려면 아무 키나 입력하세요 (q: 종료): ')
            if exit_key == 'q':
                break
        except KeyboardInterrupt:
            print('프로그램 종료')
            break
        except ValueError:
            print('잘못된 입력값입니다.')
        except Exception as e:
            print('error:', e)


if __name__ == '__main__':
    main()
