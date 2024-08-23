import streamlit as st

def get_characteristic():

    age= st.selectbox(
        '사용자의 연령대를 선택해주세요.',
        ('10대','20대', '30대','40대','50대','60대 이상')
    )
    st.session_state['age'] = age

    gender= st.selectbox(
        '사용자의 성별을 선택해주세요.',
        ('남자','여자')
    )
    st.session_state['gender'] = gender

    style = st.selectbox(
        '사용자의 식사 스타일을 선택해주세요.',
        ('비건 (Vegan, 동물성 식품을 전혀 섭취하지 않는 식습관)',
         '베지테리언 (Vegetarian, 고기와 생선을 섭취하지 않는 식습관)', 
         '오므니보어 (Omnivore, 일반적인 식습관)')
    )
    st.session_state['style'] = style

    return st.session_state['age'], st.session_state['gender'], st.session_state['style']

def get_persona():
    persona = f"저는 {st.session_state['age']}인 {st.session_state['gender']}입니다. 저의 식습관은 {st.session_state['style']}입니다. 제 나이, 성별, 식습관에 맞는 레시피 및 재료를 작성해주세요."
    st.session_state['persona'] = persona
    return st.session_state['persona']

def main():
    st.subheader("사용자의 특징을 선택해주세요! 맞춤형 레시피를 제공해드립니다!")
    get_characteristic()
    get_persona()
    # 텍스트 박스 스타일링
    st.markdown(
        """
        <style>
        .text-box {
            background-color: #333333;  /* 어두운 회색 배경 */
            border: 2px dotted #555555;  /* 점선 테두리 */
            padding: 15px;  /* 내부 여백 */
            border-radius: 10px;  /* 모서리 둥글게 */
            color: #ffffff;  /* 흰색 텍스트 */
            font-size: 16px;  /* 텍스트 크기 */
            margin-bottom: 15px;  /* 아래 여백 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("사용자의 특징을 토대로 작성된 가상의 페르소나입니다.")
    
    # 텍스트 박스로 페르소나 출력
    st.markdown(f'<div class="text-box">{st.session_state["persona"]}</div>', unsafe_allow_html=True)