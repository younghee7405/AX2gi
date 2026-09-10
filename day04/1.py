# -*- coding: utf-8 -*-

def print_all_gugudan():
    """2단부터 9단까지 가로로 정렬하여 구구단을 출력합니다."""
    print("\n" + "=" * 80)
    print("                            [ 구구단 전체 표 ]")
    print("=" * 80)
    
    # 상단 헤더 출력 (2단부터 9단까지)
    header = "  ".join([f"  [{dan}단]   " for dan in range(2, 10)])
    print(header)
    print("-" * 80)
    
    # 곱하는 수 (1~9)
    for i in range(1, 10):
        line = []
        for dan in range(2, 10):
            line.append(f"{dan} x {i} = {dan * i:2d}")
        print("  ".join(line))
    print("=" * 80 + "\n")


def print_single_gugudan(dan):
    """지정한 단의 구구단을 출력합니다."""
    if not (2 <= dan <= 9):
        print("\n[오류] 2단부터 9단 사이의 숫자만 입력 가능합니다.\n")
        return
        
    print("\n" + "=" * 20)
    print(f"      [ {dan} 단 ]")
    print("=" * 20)
    for i in range(1, 10):
        print(f"  {dan} x {i} = {dan * i:2d}")
    print("=" * 20 + "\n")


def main():
    while True:
        print("★ 구구단 프로그램 ★")
        print("1. 구구단 전체 출력")
        print("2. 특정 단 출력 (2~9단)")
        print("3. 프로그램 종료")
        
        choice = input("원하는 메뉴 번호를 입력하세요 (1~3): ").strip()
        
        if choice == '1':
            print_all_gugudan()
        elif choice == '2':
            try:
                dan = int(input("출력할 단을 입력하세요 (2~9): ").strip())
                print_single_gugudan(dan)
            except ValueError:
                print("\n[오류] 올바른 숫자를 입력해주세요.\n")
        elif choice == '3':
            print("\n구구단 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("\n[오류] 잘못된 선택입니다. 1, 2, 3 중 하나를 입력해주세요.\n")


if __name__ == "__main__":
    main()
