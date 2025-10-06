# -*- coding: utf-8 -*-
"""
사용자 인증 및 데이터 관리 모듈
"""
import json
import hashlib
import secrets
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, Any, List
import streamlit as st

# 사용자 데이터 저장 경로
USERS_DIR = Path("./users")
USERS_DIR.mkdir(exist_ok=True)

def hash_password(password: str) -> str:
    """비밀번호 해시화"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pwd_hash.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    """비밀번호 검증"""
    try:
        salt, pwd_hash = hashed.split(':')
        pwd_hash_bytes = bytes.fromhex(pwd_hash)
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return pwd_hash_bytes == new_hash
    except:
        return False

def save_user(user_data: Dict[str, Any]) -> bool:
    """사용자 정보 저장"""
    try:
        username = user_data['username']
        user_file = USERS_DIR / f"{username}.json"
        
        # 기존 사용자 확인
        if user_file.exists():
            return False
        
        # 비밀번호 해시화
        user_data['password'] = hash_password(user_data['password'])
        user_data['created_at'] = datetime.now().isoformat()
        user_data['user_id'] = secrets.token_hex(8)
        
        # 사용자 데이터 저장
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"사용자 저장 오류: {e}")
        return False

def load_user(username: str) -> Optional[Dict[str, Any]]:
    """사용자 정보 로드"""
    try:
        user_file = USERS_DIR / f"{username}.json"
        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"사용자 로드 오류: {e}")
    return None

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """사용자 인증"""
    user = load_user(username)
    if user and verify_password(password, user['password']):
        # 비밀번호 제거 후 반환
        user.pop('password', None)
        return user
    return None

def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """이메일로 사용자 찾기"""
    for user_file in USERS_DIR.glob("*.json"):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                user = json.load(f)
                if user.get('email') == email:
                    return user
        except:
            continue
    return None

def get_user_data_dir(user_id: str) -> Path:
    """사용자별 데이터 디렉토리 경로"""
    user_data_dir = USERS_DIR / f"{user_id}_data"
    user_data_dir.mkdir(exist_ok=True)
    return user_data_dir

def get_institution_data_dir(institution_name: str) -> Path:
    """기관별 공유 데이터 디렉토리 경로"""
    # 기관명을 안전한 파일명으로 변환
    safe_name = "".join(c for c in institution_name if c.isalnum() or c in ("-", "_", " ")).strip()
    safe_name = safe_name.replace(" ", "_")
    institution_dir = USERS_DIR / f"institution_{safe_name}_data"
    institution_dir.mkdir(exist_ok=True)
    return institution_dir

def get_user_accessible_data_dir(user_data: Dict[str, Any]) -> Path:
    """사용자가 접근 가능한 데이터 디렉토리 경로"""
    if user_data.get('dataSharing', False):
        # 기관 공유 데이터 사용
        return get_institution_data_dir(user_data.get('institutionName', ''))
    else:
        # 개인 데이터만 사용
        return get_user_data_dir(user_data.get('user_id', ''))

def save_user_session(user_data: Dict[str, Any]):
    """사용자 세션 저장"""
    st.session_state.user = user_data
    st.session_state.user_id = user_data['user_id']
    st.session_state.user_data_dir = get_user_accessible_data_dir(user_data)

def clear_user_session():
    """사용자 세션 클리어"""
    if 'user' in st.session_state:
        del st.session_state.user
    if 'user_id' in st.session_state:
        del st.session_state.user_id
    if 'user_data_dir' in st.session_state:
        del st.session_state.user_data_dir

def is_logged_in() -> bool:
    """로그인 상태 확인"""
    return 'user' in st.session_state and 'user_id' in st.session_state

def get_current_user() -> Optional[Dict[str, Any]]:
    """현재 로그인된 사용자 정보 반환"""
    return st.session_state.get('user')

def require_login():
    """로그인 필수 데코레이터"""
    if not is_logged_in():
        st.error("로그인이 필요합니다.")
        st.markdown("### 🔐 로그인")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("로그인 페이지로 이동"):
                st.switch_page("pages/login.py")
        with col2:
            if st.button("회원가입 페이지로 이동"):
                st.switch_page("pages/register.py")
        st.stop()

def get_user_specific_data_path(filename: str) -> Path:
    """사용자별 데이터 파일 경로"""
    if not is_logged_in():
        raise ValueError("로그인이 필요합니다.")
    
    user_data_dir = st.session_state.user_data_dir
    return user_data_dir / filename

def save_user_data(data: Any, filename: str):
    """사용자별 데이터 저장"""
    file_path = get_user_specific_data_path(filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def load_user_data(filename: str) -> Optional[Any]:
    """사용자별 데이터 로드"""
    try:
        file_path = get_user_specific_data_path(filename)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"데이터 로드 오류: {e}")
    return None

def get_institution_users(institution_name: str) -> List[Dict[str, Any]]:
    """동일 기관의 사용자 목록 반환"""
    users = []
    for user_file in USERS_DIR.glob("*.json"):
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                user = json.load(f)
                if (user.get('institutionName') == institution_name and 
                    user.get('dataSharing', False)):
                    # 비밀번호 제거
                    user.pop('password', None)
                    users.append(user)
        except:
            continue
    return users

def get_institution_patient_ids(institution_name: str) -> List[str]:
    """기관별 환자 ID 목록 반환"""
    institution_dir = get_institution_data_dir(institution_name)
    if not institution_dir.exists():
        return []
    return sorted([p.name for p in institution_dir.iterdir() if p.is_dir()])

def create_demo_user():
    """데모 사용자 생성"""
    demo_user = {
        'user_id': 'demo',
        'username': 'demo_user',
        'fullName': '데모 사용자',
        'email': 'demo@example.com',
        'birthDate': '2010-01-01',
        'gender': '남',
        'institutionName': '데모 병원',
        'institutionAddress': '서울시 강남구',
        'licenseNumber': 'DEMO123456',
        'dataSharing': False,
        'created_at': datetime.now().isoformat()
    }
    
    st.session_state.user = demo_user
    st.session_state.user_id = 'demo'
    st.session_state.user_data_dir = Path("./demo_data")
    st.session_state.user_data_dir.mkdir(exist_ok=True)
    
    return demo_user
