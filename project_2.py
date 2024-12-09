import streamlit as st
import random

# 랜덤 숫자 생성
def generate_random_4_digits(count):
    random_numbers = []
    for _ in range(count):
        random_numbers.append(random.randint(0, 9))
    return random_numbers

# 질문 생성
def question_generator(num_digits):
    q_list = []
    while len(q_list) < num_digits:
        random_number = generate_random_4_digits(1)[0]
        if random_number not in q_list:
            q_list.append(random_number)
    return q_list

# 답변 체크
def check_answer(q_list, p_list):
    strike, ball = 0, 0
    for i in range(len(q_list)):
        if p_list[i] == q_list[i]:
            strike += 1
        elif p_list[i] in q_list:
            ball += 1
    return strike, ball

# Streamlit 앱 시작
def main():
    st.title("숫자 야구 게임")
    st.write("숫자를 맞추는 게임입니다. 중복되지 않는 숫자를 입력하세요!")
    
    # 게임 설정
    game_mode = st.radio("게임 모드를 선택하세요:", ("3자리 숫자", "4자리 숫자"))
    num_digits = 3 if game_mode == "3자리 숫자" else 4
    
    # 게임 초기화
    if "q_list" not in st.session_state:
        st.session_state.q_list = question_generator(num_digits)
        st.session_state.attempts = 0
        st.session_state.history = []

    # 입력 받기
    user_input = st.text_input(f"{num_digits}자리 숫자를 입력하세요 (중복 불가):", max_chars=num_digits)

    if st.button("제출"):
        if len(user_input) != num_digits or not user_input.isdigit():
            st.warning(f"{num_digits}자리 숫자를 정확히 입력하세요.")
        elif len(set(user_input)) != num_digits:
            st.warning("중복된 숫자가 있습니다. 다시 입력하세요.")
        else:
            p_list = list(map(int, user_input))
            st.session_state.attempts += 1
            strike, ball = check_answer(st.session_state.q_list, p_list)
            st.session_state.history.append((p_list, strike, ball))

            if strike == num_digits:
                st.success(f"축하합니다! {st.session_state.attempts}번 만에 정답을 맞추셨습니다.")
                st.session_state.q_list = None
            elif st.session_state.attempts >= 10:
                st.error(f"10번의 시도를 초과했습니다! 정답은 {st.session_state.q_list}였습니다.")
                st.session_state.q_list = None
            else:
                st.info(f"{strike} 스트라이크, {ball} 볼")

    # 이전 기록 표시
    if st.session_state.history:
        st.write("### 시도 기록")
        for attempt, (guess, strike, ball) in enumerate(st.session_state.history, 1):
            st.write(f"시도 {attempt}: {guess} -> {strike} 스트라이크, {ball} 볼")

    # 게임 재시작
    if st.button("게임 재시작"):
        st.session_state.q_list = question_generator(num_digits)
        st.session_state.attempts = 0
        st.session_state.history = []
        st.success("게임이 초기화되었습니다!")

if __name__ == "__main__":
    main()
