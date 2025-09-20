# 문제 2. 카이사르 암호
# 수행 과제
# password.txt 파일을 읽어온다.
# 카이사르의 암호를 풀 수 있는 함수를 caesar_cipher_decode() 라는 이름으로 만든다.
# caesar_cipher_decode() 함수는 풀어야 하는 문자열을 파라메터로 추가한다. 이때 파라메터의 이름은 target_text으로 한다.
# caesar_cipher_decode() 에서 자리수에 따라 암호표가 바뀌게 한다. 자리수는 알파벳 수만큼 반복한다.
# 자리수에 따라서 해독된 결과를 출력한다.
# 몇 번째 자리수로 암호가 해독되는지 찾아낸다. 눈으로 식별이 가능하면 해당 번호를 입력하면 그 결과를 result.txt로 저장을 한다.


def move(ch, k, m):
    base0 = ord(ch) - m
    base0 = (base0 + k) % 26
    return base0 + m


def caesar_cipher_decode(target_text):
    for i in range(1, 27):
        print(f'[{i}]: ', end='')
        for j in target_text:
            if j.islower():
                print(chr(move(j, i, 97)), end='')
            elif j.isupper():
                print(chr(move(j, i, 65)), end='')
            else:
                print(j, end='')
        print()


def caesar_cipher_decode_with_key(target_text, key):
    answer = ''
    for j in target_text:
        if j.islower():
            answer += chr(move(j, key, 97))
        elif j.isupper():
            answer += chr(move(j, key, 65))
        else:
            answer += j
    with open('result.txt', 'w') as f:
        f.write(answer)


def main():
    try:
        with open('password.txt', 'r') as f:
            content = f.read()
            caesar_cipher_decode(content)
            num = int(input('맞는 번호 입력: '))
            caesar_cipher_decode_with_key(content, num)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
