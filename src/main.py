
"""
Music/Language Player Start 
"""
import sys
import os
from src.ui.app_ui import MusicPlayer
import tkinter as tk

def main():
    """애플리케이션 시작 함수"""
    try:
        # 리소스 경로 설정
        if getattr(sys, 'frozen', False):
            # PyInstaller로 패키징된 경우
            application_path = sys._MEIPASS
        else:
            # 일반 Python 스크립트로 실행 중인 경우
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # 애플리케이션 아이콘 경로
        icon_path = os.path.join(os.path.dirname(application_path), 'resources', 'icons', 'music.ico')
        print(icon_path)
        
        # 애플리케이션 시작
        root = tk.Tk()
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        app = MusicPlayer(root)
        root.mainloop()
    
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        input("아무 키나 눌러 종료하세요...")
        sys.exit(1)

if __name__ == "__main__":
    main()