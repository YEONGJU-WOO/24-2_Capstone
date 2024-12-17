import streamlit as st
from PIL import Image


def main():
  st.set_page_config(layout='wide')
  st.title('Functional Movement Screen')
  col1,col2 = st.columns([3,2])
  # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.
  title_img = Image.open('pushpress.webp')
  with col1 :
    # column 1 에 담을 내용
    st.subheader(' The Functional Movement Screen (FMS) assesses movement patterns to identify imbalances and reduce injury risk through seven simple tests.')
    st.page_link("pages/fms.py", label="How does the FMS work?", use_container_width=True)
    st.page_link("pages/webcam.py", label="Capture Camera", icon='📷', use_container_width=True)
    st.page_link("pages/video.py", label="Select  Video", icon='▶️', use_container_width=True)

  with col2 :
    # column 2 에 담을 내용
    # st.title('here is column2')
    st.container()
    st.image(title_img)





if __name__ == '__main__':
  main()