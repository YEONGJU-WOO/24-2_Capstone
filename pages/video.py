import streamlit as st
import cv2
from PIL import Image
import numpy as np
import tempfile


def main():
    st.set_page_config(layout='wide')
    st.title('Select Video')
    col1,col2 = st.columns(2)
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.

    with col1 :
        # column 1 에 담을 내용
        f = st.file_uploader("Upload file")

        try:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(f.read())

            vf = cv2.VideoCapture(tfile.name)

            stframe = st.empty()

            while vf.isOpened():
                ret, frame = vf.read()
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                stframe.image(gray)
            vf.release()
        except:
            pass

    with col2 :
        # column 2 에 담을 내용
        # st.image(title_img)
        col2.subheader("If you want to analyze the action, press the Analysis button")

        btn_analysis = st.button("Analysis", use_container_width=True)
        if btn_analysis:
            st.switch_page('pages/analysis.py')




if __name__ == '__main__':
  main()