## 반달곰 커피 홈페이지

[참조링크 <>](<https://반달곰 커피>)

[참조링크 urlencoded](<https://%EB%B0%98%EB%8B%AC%EA%B3%B0%20%EC%BB%A4%ED%94%BC>)

[참조링크 기본](https://반달곰 커피)

https://반달곰 커피

오디오 출력 소스코드

```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)
encoded_audio_data = base64.b64encode(fp.getvalue())
```

![david](david.jpg)
