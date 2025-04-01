# Music Player

음악, 언어학습을 위해 도움을 주는 Music Player 입니다. 

## 주요 기능

- 음악, 영어 파일 재생
- Play, Pause, Stop, forward, rewind 기능 제공
- forward, rewind 속도 조절 가능 : Skip Speed
- Loop를 통해서 반복 재생 가능 

## 설치 방법

### 필요 조건

- Python 3.6 이상
- pygame 라이브러리

### pip를 이용한 설치

```bash
pip install pygame
```

### 소스에서 설치

```bash
git clone https://github.com/reinhardt0926/music_player.git
cd music_player
pip install -e .
```

## 사용 방법

### 애플리케이션 실행

```bash
music_player
```

또는 소스 코드에서 직접 실행:

```bash
python -m src.main
```

### 사용 예시

1. "File Select" 버튼을 클릭하여 듣고 싶은 음악(영어 음성 파일)을 선택합니다.
2. "Play" 버튼을 사용하여 음악을 듣습니다. 
3. "Pause", "Stop", "forward", "rewind" 버튼을 사용하여 필요한 음악 재생 기능을 사용합니다. 
4. "Skip Speed" 를 선택하면 "forward", "rewind" 속도를 조절 가능합니다.
5. "Loop Start", "Loop End", "Play Loop"를 통해 반복 재생이 가능합니다. 
    1) 반복 시작하고 싶은 부분에서 "Loop Start" 버튼을 클릭합니다.
    2) 반복 끝내고 싶은 부분에서 "Loop End" 버튼을 클릭합니다.
    3) "Play Loop" 버튼을 클릭하여 반복 구간 재생합니다.
    4) 반복을 끝내고 싶으면 다시 "Play" 버튼 클릭합니다. 

## 배포용 실행 파일 만들기

### PyInstaller를 이용한 실행 파일 생성

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=resources/icons/music.ico --add-data "resources;resources" src/main.py
```

생성된 실행 파일은 `dist` 폴더에서 찾을 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.

