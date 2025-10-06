# -*- coding: utf-8 -*-
"""
로그인 페이지
"""
import streamlit as st
import requests
from auth import authenticate_user, save_user_session, find_user_by_email

st.set_page_config(
    page_title="로그인 - 안축장 성장 차트",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 로그인")

# 로그인 폼
with st.form("login_form"):
    username = st.text_input("사용자명 또는 이메일", placeholder="사용자명 또는 이메일을 입력하세요")
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
    
    col1, col2 = st.columns(2)
    with col1:
        login_submitted = st.form_submit_button("로그인", use_container_width=True)
    with col2:
        demo_submitted = st.form_submit_button("데모 로그인", use_container_width=True)

if login_submitted:
    if username and password:
        # 이메일로 로그인 시도
        user = authenticate_user(username, password)
        if not user:
            # 이메일로 사용자 찾기
            email_user = find_user_by_email(username)
            if email_user:
                user = authenticate_user(email_user['username'], password)
        
        if user:
            save_user_session(user)
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("사용자명/이메일 또는 비밀번호가 올바르지 않습니다.")
    else:
        st.error("모든 필드를 입력해주세요.")

if demo_submitted:
    from auth import create_demo_user
    create_demo_user()
    st.success("데모 계정으로 로그인했습니다!")
    st.rerun()

# 회원가입 링크
st.markdown("---")
st.markdown("계정이 없으신가요? [회원가입 페이지로 이동](register)")

# 메인 페이지로 돌아가기
st.markdown("[← 메인 페이지로 돌아가기](/)")
