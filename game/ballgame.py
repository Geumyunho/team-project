import random
import sys

class NotfFourNumber(Exception):
    def __init__(self):
        super().__init__('NotFourNumber')

class BlankNumber(Exception):
    def __init__(self):
        super().__init__('BlankNumber')

class NotPositiveInteger(Exception):
    def __init__(self):
        super().__init__('NotPositiveInteger')

class NotInteger(Exception):
    def __init__(self):
        super().__init__('NotInteger')

class BallGame:
    total_score = 0
    total_balls = 0

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.target_number = self.generate_random_number()
        self.attempts = 0
        self.outs = 0
        self.first_attempt = True

    @staticmethod
    def generate_random_number():
        return random.sample(range(10), 4)

    def display_target_number(self):
        print(f"컴퓨터가 제시한 숫자: {''.join(map(str, self.target_number))}")

    def play_game(self, user_guess):
        self.attempts += 1
        result = self.compare_numbers(user_guess)
        self.display_result(result)
        hits = sum(user_digit == target_digit for user_digit, target_digit in zip(user_guess, self.target_number))
        balls = sum(user_digit in self.target_number and user_digit != target_digit for user_digit, target_digit in zip(user_guess, self.target_number))
        outs = 4 - (hits + balls)
        self.outs += outs

        if result == "홈런":
            if self.first_attempt:
                score = 300
            print(f"홈런! {score}점 획득!")
            self.display_target_number()
            self.total_score += score
            self.reset_game()
        else:
            if result.endswith("3루타"):
                score = 30
            elif result.endswith("2루타"):
                score = 20
            elif result.endswith("1루타"):
                score = 10
            else:
                score = 0

            self.total_score += score

            if self.attempts >= 5 or self.outs > 2:
                self.end_game()

    def compare_numbers(self, user_guess):
        if user_guess == self.target_number:
            return "홈런"

        hits = sum(user_digit == target_digit for user_digit, target_digit in zip(user_guess, self.target_number))
        balls = sum(user_digit in self.target_number and user_digit != target_digit for user_digit, target_digit in zip(user_guess, self.target_number))
        outs = 4 - (hits + balls)
        self.total_balls += balls
        return f"{outs}out {balls}ball {hits}루타"

    def display_result(self, result):
        print(f"출력문: {result}")

    def end_game(self):
        self.total_score += (self.total_balls // 4) * 10
        print(f"게임이 종료되었습니다. 최종 총 점수는 {self.total_score}점입니다.")
        game.display_target_number()
        sys.exit()

# 게임 시작
game = BallGame()

while True:
    user_input = input("4자리 숫자를 입력하세요 (종료하려면 '종료' 입력): ")

    if user_input.lower() == '종료':
        game.end_game()

    try:
        if ' ' in user_input:
            raise BlankNumber
        if '.' in user_input:
            raise NotInteger
        if '-' in user_input:
            raise NotPositiveInteger

        user_guess = [int(digit) for digit in user_input if digit.isdigit()]
        if len(user_guess) != 4:
            raise NotfFourNumber
        if len(set(user_guess)) < 4:
            raise ValueError("중복 없는 숫자를 입력하세요.")

    except NotInteger:
        print('정수를 입력하세요')
        continue
    except NotPositiveInteger:
        print('양의 정수를 입력하세요')
        continue
    except NotfFourNumber:
        print("4자리인 숫자를 입력하세요.")
        continue
    except BlankNumber:
        print('공백이 없는 숫자를 입력하세요')
        continue
    except ValueError as e:
        print(e)
        continue

    game.play_game(user_guess)

