import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime
from pytz import timezone

def main():
    st.set_page_config(layout='wide')
    st.title('Capture Camera')
    col1,col2 = st.columns([2,1])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.


    # column 1 에 담을 내용
    # img_file_buffer = col1.camera_input('Take a picture')
    # st.write(img_file_buffer)
    #
    # if img_file_buffer is not None:
    #     # To read image file buffer as a PIL Image:
    #     img = Image.open(img_file_buffer)
    #
    #     # To convert PIL Image to numpy array:
    #     img_array = np.array(img)
    #
    #     # Check the type of img_array:
    #     # Should output: <class 'numpy.ndarray'>
    #     col1.write(type(img_array))
    #
    #     # Check the shape of img_array:
    #     # Should output shape: (height, width, channels)
    #     col1.write(img_array.shape)

    if 'button' not in st.session_state:
        st.session_state.button = False

    def click_button():
        st.session_state.button = not st.session_state.button

    # column 2 에 담을 내용
    # st.image(title_img)
    col2.subheader("If you're ready to shoot, press the record button, and if you want to end the shoot, press the stop button")





    left, right = col2.columns(2)
    btn_record = left.button("Record", on_click = click_button, use_container_width=True)
    btn_stop = right.button("Stop", on_click = click_button, use_container_width=True)
    # st.write(btn_record, btn_reset)

    def set_record():
        date_today = datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%dT%H%M")
        frame_width = int(camera.get(3))
        frame_height = int(camera.get(4))
        size = (frame_width, frame_height)
        result = cv2.VideoWriter('./saved_video/{}.mp4'.format(date_today), cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

        return result

    btn_save = col2.button("Save", use_container_width=True)
    run = col1.checkbox('Run')
    FRAME_WINDOW = col1.image([])
    camera = cv2.VideoCapture(0)

    if btn_stop is False and btn_record is False:
        print("Ready")
        result = None
    elif btn_stop is False and btn_record is True:
        print("recording")
        result = set_record()



    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        FRAME_WINDOW.image(frame)
        if btn_record:
            frame_1 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            result.write(frame_1)

    else:
        st.write('.')

    if btn_save:
        result.release()



    col2.subheader("If you want to analyze the action, press the Analysis button")
    btn_analysis = col2.button("Analysis", use_container_width=True)

    if btn_analysis:
        st.switch_page("pages/analysis.py")
        pass

if __name__ == '__main__':
    main()