# -*- coding: utf-8 -*-
"""
회원가입 페이지
"""
import streamlit as st
from datetime import date, datetime
from auth import save_user, load_user, find_user_by_email

st.set_page_config(
    page_title="회원가입 - 안축장 성장 차트",
    page_icon="📝",
    layout="centered"
)

st.title("📝 회원가입")

# 회원가입 폼
with st.form("register_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("사용자명 *", placeholder="사용자명을 입력하세요")
        email = st.text_input("이메일 *", placeholder="이메일을 입력하세요")
        password = st.text_input("비밀번호 *", type="password", placeholder="비밀번호를 입력하세요 (최소 6자)")
        confirm_password = st.text_input("비밀번호 확인 *", type="password", placeholder="비밀번호를 다시 입력하세요")
    
    with col2:
        full_name = st.text_input("실명 *", placeholder="실명을 입력하세요")
        birth_date = st.date_input("생년월일 *", value=date(2010, 1, 1), max_value=date.today())
        gender = st.selectbox("성별 *", ["", "남", "여"])
    
    submitted = st.form_submit_button("회원가입", use_container_width=True)

if submitted:
    # 유효성 검사
    errors = []
    
    if not username:
        errors.append("사용자명을 입력해주세요.")
    elif len(username) < 3:
        errors.append("사용자명은 최소 3자 이상이어야 합니다.")
    elif load_user(username):
        errors.append("이미 존재하는 사용자명입니다.")
    
    if not email:
        errors.append("이메일을 입력해주세요.")
    elif "@" not in email:
        errors.append("올바른 이메일 형식을 입력해주세요.")
    elif find_user_by_email(email):
        errors.append("이미 등록된 이메일입니다.")
    
    if not password:
        errors.append("비밀번호를 입력해주세요.")
    elif len(password) < 6:
        errors.append("비밀번호는 최소 6자 이상이어야 합니다.")
    
    if password != confirm_password:
        errors.append("비밀번호가 일치하지 않습니다.")
    
    if not full_name:
        errors.append("실명을 입력해주세요.")
    
    if not gender:
        errors.append("성별을 선택해주세요.")
    
    if birth_date >= date.today():
        errors.append("생년월일은 오늘 이전이어야 합니다.")
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        # 사용자 데이터 생성
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'fullName': full_name,
            'birthDate': birth_date.isoformat(),
            'gender': gender
        }
        
        # 사용자 저장
        if save_user(user_data):
            st.success("회원가입이 완료되었습니다!")
            st.info("로그인 페이지로 이동하여 로그인해주세요.")
            st.markdown("[로그인 페이지로 이동](login)")
        else:
            st.error("회원가입 중 오류가 발생했습니다. 다시 시도해주세요.")

# 개인정보 보호 안내
st.markdown("---")
st.markdown("### 🔒 개인정보 보호 안내")
st.info("""
• 입력하신 모든 개인정보는 안전하게 암호화되어 저장됩니다.
• 본인만의 데이터에 접근할 수 있으며, 다른 사용자의 데이터는 볼 수 없습니다.
• 데이터는 의료 목적으로만 사용되며, 제3자와 공유되지 않습니다.
""")

# 메인 페이지로 돌아가기
st.markdown("[← 메인 페이지로 돌아가기](/)")
