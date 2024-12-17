import streamlit as st
from PIL import Image


def main():

    st.set_page_config(layout='wide')
    st.title('How does the FMS work?')
    # 7가지 동작에 대한 설명을 위한 탭  생성
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Deep Squat', 'Hurdle Step', 'In-line Lunge', 'Shoulder Mobility',
                                                      'Active Straight Leg Raise', 'Trunk Stability Push-up', 'Rotary Stability'])

    with tab1:
        st.header('Deep Squat')
        col1, col2 = st.columns([2,1])
        col1.video('https://youtu.be/eQ20KiyBKzU', format='video/mp4')
        col2.subheader('딥 스쿼트 검사 방법 (영상 첨부)')
        col2.markdown('1. 똑바로 서서 발을 어깨 너비로 벌리고 발가락이 정면을 향하도록 합니다.')
        col2.markdown('2. 봉을 양손에 잡고 머리 위로 올려 팔꿈치가 90도가 되도록 합니다.')
        col2.markdown('3. 봉을 머리 위로 밀어 올립니다.')
        col2.markdown('4. 몸통을 똑바로 세우고 뒷꿈치를 바닥에 붙인 상태로 가능한 깊이 앉는 스쿼트 동작을 해봅니다.')
        col2.markdown('5. 최대로 많이 내려간 상태에서 잠시 멈췄다가 시작 자세로 돌아옵니다.')


    with tab2:
        st.header('Hurdle Step')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/fxPDdKWg4GY', format='video/mp4')
        col2.subheader('허들 스텝 검사 방법 (영상 첨부)')
        col2.markdown('1. 지면부터 경골 조면까지의 길이를 측정하여 줄 높이를 설정합니다.')
        col2.markdown('2. 발을 모으고 테스트 키트에 닿게 한 채 똑바로 섭니다.')
        col2.markdown('3. 봉을 양손에 잡고 머리 위에 올려 팔꿈치가 90도가 되게 합니다.')
        col2.markdown('4. 봉을 아래로 내려 목 뒤쪽에서 어깨와 평행이 되게 만듭니다.')
        col2.markdown('5. 몸통을 똑바로 세운 채로 오른쪽 발을 들어 허들을 넘어갑니다.')
        col2.markdown('6. 발꿈치로 바닥을 터치한 후 시작 자세로 돌아옵니다.')

    with tab3:
        st.header('In-line Lunge')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/KCELe_4MhEY', format='video/mp4')
        col2.subheader('인라인 런지 검사 방법 (영상 첨부)')
        col2.markdown('1. 오른발 발가락을 FMS 키트 영점선에 놓고 발을 보드 중앙에 위치시킵니다.')
        col2.markdown('2. 왼발 뒤꿈치는 앞서 측정한 경골 길이 만큼의 눈금에 위치시킵니다.')
        col2.markdown('3. 봉은 척추를 따라 배치하되 머리, 뒤통수, 등 상부 및 꼬리뼈에 모두 닿도록 합니다.')
        col2.markdown('4. 몸통을 똑바로 세워 봉이 수직인 상태를 유지합니다.')
        col2.markdown('5. 런지 자세로 내려가 왼쪽 무릎이 보드 중앙에 닿도록 하고 다시 시작 자세로 돌아옵니다.')

    with tab4:
        st.header('Shoulder Mobility')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/qzHAjr84lPk', format='video/mp4')
        col2.subheader('숄더 모빌리티 검사 방법 (영상 첨부)')
        col2.markdown('1. 발을 모아 똑바로 서서 팔을 좌우로 벌려줍니다.')
        col2.markdown('2. 엄지 손가락이 나머지 손가락 안으로 들어가도록 주먹을 쥡니다.')
        col2.markdown('3. 오른쪽 주먹은 머리 위에서 아래로 내리고, 왼쪽 주먹은 등 뒤에서 위로 올려 최대한 가깝게 합니다. 이때 동작은 한번에 진행해야 합니다.')
        col2.markdown('4. 첫 동작 이후에 손을 움직여 더 가깝게 하려고 해서는 안 됩니다.')


    with tab5:
        st.header('Active Straight Leg Raise')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/9iIXxRoxzRo', format='video/mp4')
        col2.subheader('액티브 스트레이트 레그 레이즈 검사 방법 (영상 첨부)')
        col2.markdown('1. 무릎 뒤쪽이 테스트 키트 위에 닿게 누워 발을 모으고 발가락을 위쪽으로 세웁니다.')
        col2.markdown('2. 손바닥을 위로 향하게 하여 팔을 몸 옆에 둡니다.')
        col2.markdown('3. 왼쪽 다리를 똑바로 펴고 왼쪽 무릎 뒤쪽이 테스트 키트에 닿은 상태를 유지하여 오른쪽 다리를 높이 들어줍니다.')
        col2.markdown('4. 반대쪽도 마찬가지로 실시합니다.')

    with tab6:
        st.header('Trunk Stability Push-up')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/WA4AjT27Bm4', format='video/mp4')
        col2.subheader('트렁크 스태빌리티 푸쉬업 검사 방법 (영상 첨부)')
        col2.markdown('1. 엎드린 상태에서 팔을 머리 위쪽으로 어깨너비만큼 벌려 준비합니다.')
        col2.markdown('2. 양손 엄지손가락이 남자의 경우 이마 옆에, 여자의 경우 턱 옆까지 올 수 있게 내립니다.')
        col2.markdown('3. 양쪽 다리를 붙인 상태에서 발가락을 세웁니다.')
        col2.markdown('4. 몸통을 단단하게 유지한 상태에서 몸 전체가 한 번에 올라올 수 있게 합니다.')

    with tab7:
        st.header('Rotary Stability')
        col1, col2 = st.columns([2, 1])
        col1.video('https://youtu.be/zo09LNnCKrk', format='video/mp4')
        col2.subheader('로터리 스태빌리티 검사 방법 (영상 첨부)')
        col2.markdown('1. FMS 테스트 키트 위에 네발기기 자세를 취하여 엄지, 무릎, 발가락이 테스트 키트에 닿게 합니다.')
        col2.markdown('2. 손은 어깨 밑에, 무릎은 엉덩이 밑에 위치하고 발가락은 뒤쪽을 향하도록 발목을 펴줍니다.')
        col2.markdown('3. 한 번에 부드럽게 통제된 동작으로 같은 쪽 팔과 다리를 들어 올려 바닥을 짚지 않은 상태에서 손목으로 바깥을 터치한 뒤, 무릎과 팔꿈치를 펴서 팔과 다리를 뻗어줍니다.')
        col2.markdown('4. 다시 손으로 발목을 터치하고 시작 자세로 돌아옵니다.')
        col2.markdown('4. 이 동작을 할 때 팔과 다리는 테스트 키트 위 선상에 유지될 수 있도록 합니다.')

if __name__ == '__main__':
  main()