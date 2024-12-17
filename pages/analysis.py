import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import time
import glob
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os


def pixel2world_vis_motion(motion, dim=2, is_tensor=False):
#     pose: (17,2,N)
    N = motion.shape[-1]
    if dim==2:
        offset = np.ones([2,N]).astype(np.float32)
    else:
        offset = np.ones([3,N]).astype(np.float32)
        offset[2,:] = 0
    # if is_tensor:
    #     offset = torch.tensor(offset)
    return (motion + offset) * 512 / 2

# 평가 함수
def calculate_vector(data, start_joint, end_joint):
    """두 관절 사이의 벡터를 계산합니다."""
    return data[end_joint] - data[start_joint]

def cosine_similarity_score(actual_vector, ideal_vector, threshold=(0.98, 0.95, 0.85)):
    """코사인 유사도를 기반으로 점수를 계산합니다."""
    similarity = cosine_similarity([actual_vector], [ideal_vector])[0][0]
    if abs(similarity) >= threshold[0]:
        return 3
    elif abs(similarity) >= threshold[1]:
        return 2
    elif abs(similarity) >= threshold[2]:
        return 1
    else:
        return 0

# 평가 항목 함수

joint_mapping = {
        'root': 0, 'RHip': 1, 'RKnee': 2, 'RAnkle': 3, 'LHip': 4, 'LKnee': 5, 'LAnkle': 6,
        'torso': 7, 'neck': 8, 'nose': 9, 'head': 10,
        'LShoulder': 11, 'LElbow': 12, 'LWrist': 13,
        'RShoulder': 14, 'RElbow': 15, 'RWrist': 16
    }

def evaluate_hip_parallel(data):
    """1. 양쪽 고관절이 수평인지 확인"""
    RHip, LHip = data[joint_mapping['RHip']], data[joint_mapping['LHip']]
    return 3 if abs(RHip[1] - LHip[1]) < 0.05 else 2 if abs(RHip[1] - LHip[1]) < 0.10 else 2 if abs(RHip[1] - LHip[1]) < 0.15 else 0

def evaluate_tibia_torso_parallel(data):
    """2. 경골과 상체가 평행한지 확인"""
    tibia_vector = calculate_vector(data, joint_mapping['RKnee'], joint_mapping['RAnkle'])
    torso_vector = calculate_vector(data, joint_mapping['torso'], joint_mapping['neck'])
    return cosine_similarity_score(tibia_vector, torso_vector)

def evaluate_knees_over_feet(data):
    """3. 무릎이 발 위에 위치하는지 확인"""
    RKnee, RAnkle = data[joint_mapping['RKnee']], data[joint_mapping['RAnkle']]
    LKnee, LAnkle = data[joint_mapping['LKnee']], data[joint_mapping['LAnkle']]
    if abs(RKnee[0] - RAnkle[0]) < 0.05 and abs(LKnee[0] - LAnkle[0]) < 0.05:
        score = 3
    elif abs(RKnee[0] - RAnkle[0]) < 0.05 and abs(LKnee[0] - LAnkle[0]) >= 0.05:
        score = 2
    elif abs(RKnee[0] - RAnkle[0]) >= 0.05 and abs(LKnee[0] - LAnkle[0]) < 0.05:
        score = 2
    elif abs(RKnee[0] - RAnkle[0]) >= 0.05 and abs(LKnee[0] - LAnkle[0]) >= 0.05:
        score = 1
    else:
        score = 0
    return score

def evaluate_cog_symmetry(data):
    """4. 체중 중심이 대칭인지 확인"""
    RHip, LHip = data[joint_mapping['RHip']], data[joint_mapping['LHip']]
    COG = (RHip + LHip) / 2  # 중심 좌표
    return 3 if abs(COG[0]) < 0.05 else 2 if abs(COG[0]) < 0.10 else 0

def evaluate_bar_behind_toes(data):
    """5. 봉이 발가락 뒤에 위치하는지 확인 (손과 발가락 비교)"""
    hands = data[joint_mapping['RWrist']]
    toes = data[joint_mapping['RAnkle']]
    return 3 if hands[0] < toes[0] else 0

def evaluate_lumbar_flexion(data):
    """6. 요추의 굴곡 확인"""
    torso_vector = calculate_vector(data, joint_mapping['torso'], joint_mapping['neck'])
    ideal_vertical = np.array([0, 1, 0])
    return cosine_similarity_score(torso_vector, ideal_vertical)


def evaluate_heels_on_ground(data):
    """7. 뒤꿈치가 바닥에 닿아 있는지 확인"""
    RAnkle, LAnkle = data[joint_mapping['RAnkle']], data[joint_mapping['LAnkle']]
    return 3 if RAnkle[2] < 0.05 and LAnkle[2] < 0.05 else 0


def fms(data_npy):
    data = np.load(data_npy)
    frame = np.argmax(np.transpose(data,(1,0,2))[0][:,1])

    scores = {
        "1. Hip Parallel": evaluate_hip_parallel(data[frame]),
        "2. Tibia & Torso Parallel": evaluate_tibia_torso_parallel(data[frame]),
        "3. Knees Over Feet": evaluate_knees_over_feet(data[frame]),
        "4. COG Symmetry": evaluate_cog_symmetry(data[frame]),
        "5. Bar Behind Toes": evaluate_bar_behind_toes(data[frame]),
        "6. Heels on Ground": evaluate_heels_on_ground(data[frame]),
        "7. Lumbar Flexion": evaluate_lumbar_flexion(data[frame]),
    }


    score = list(scores.values())
    return score
    # pass

def main():

    st.set_page_config(layout='wide')
    st.title('Analysis')
    # 7가지 동작에 대한 설명을 위한 탭  생성

    saved_video_list = []
    for filename in glob.glob('*\\squat_data\\*\\*\\Alpha*.mp4'):
        saved_video_list.append(filename)

    saved_3d_list = []
    for filename in glob.glob('*\\squat_data\\*\\*\\X3D.mp4'):
        saved_3d_list.append(filename)

    saved_npy_list = []
    for filename in glob.glob('*\\squat_data\\*\\*\\X3D.npy'):
        saved_npy_list.append(filename)

    saved_video = [['.','.']]
    # saved_3d = []
    for path in saved_video_list:
        dd = path.rsplit('\\', 1)[0]
        saved_video.append([path.split('\\', 4)[-1], glob.glob(f'{dd}\\X3D.mp4')[0]])

    saved_npy = [['.', '.']]
    for path in saved_video_list:
        dd = path.rsplit('\\', 1)[0]
        saved_npy.append([path.split('\\', 4)[-1], glob.glob(f'{dd}\\X3D.npy')[0]])

    my_choice = st.selectbox('분석을 원하는 영상을 선택하세요.', np.array(saved_video)[:,0])   # video.py나 webcam에서 저장된 영상의 리스트를 제공
    matching = [s for s in np.array(saved_video_list) if my_choice in s]
    matching_2 = [s for s in np.array(saved_video) if my_choice in s]
    matching_3 = [s for s in np.array(saved_npy) if my_choice in s]


    tab1, tab2, tab3 = st.tabs(['2D Pose Estimation', '2. 3D Pose Reconstruction', '3. Screen'])

    with tab1:
        col1, col2 = st.columns([1,2.5])
        col1.header('1. 2D Pose Estimation')
        pe_2d = col1.button('2차원 포즈 추정', use_container_width=True)


        if pe_2d:
            #포즈 추정 코드가 실행되어 영상 결과를 출력
            with col1:
                with st.spinner('Wait for it...'):
                    cmd = 'python ../AlphaPose/scripts/demo_inference.py --cfg configs/halpe_26/resnet/256x192_res50_lr1e-3_2x.yaml --checkpoint pretrained_models/halpe26_fast_res50_256x192.pth --video squat_data/deepsquat/IMG_6705.MP4 --outdir squat_data/deepsqaut/deep_2 --save_video'
                    os.system(cmd)

                # if my_choice in ['AlphaPose_IMG_6702.MP4', 'AlphaPose_IMG_6703.MP4', 'AlphaPose_IMG_6705.MP4', 'AlphaPose_IMG_6707.MP4']:
                #     col1.subheader("This Movement is Deep-Squat!")
                # else:
                #     col1.subheader('This Movement is not Deep-Squat! Select right movement')
            with col2:
                # st.video('out_video_1.mp4', 'rb')
                video_file = open(matching[0], 'rb')  # my_choice의 영상을 불러와 재생
                video_bytes = video_file.read()
                #
                st.video(video_bytes)

            pass

    with tab2:
        col1, col2 = st.columns([1, 2])
        col1.header('2. 3D Pose Reconstruction')
        pr_3d = col1.button('3차원 포즈 재구성')
        if pr_3d:
            with col1:
                with st.spinner('Wait for it...'):
                    cmd = 'python ../MotionBERT/infer_wild.py --vid_path example/output_1/out_video.mp4 --json_path example/output_1/alphapose-results.json --out_path example/out_3d'
                    os.system(cmd)
                    # time.sleep(5)
            # 포즈 추정 코드가 실행되어 영상 결과를 출력
            with col2:
                st.video(matching_2[0][1], 'rb')  # my_choice의 영상을 불러와 재생
            pass

    with tab3:
        st.header('Screen')
        col1, col2 = st.columns([1,2])
        btn_fms = col1.button('FMS 실행')

        if btn_fms:
            with st.spinner('Wait for it...'):
                time.sleep(5)

            # 초기 데이터 정의
            data = {
                "Task": ["Deep Squat"] * 7,
                "Criteria": [
                    "1. 양측 고관절이 평행한가?",
                    "2. 경골/상체가 평행한가?",
                    "3. 무릎이 두발에 있는가?",
                    "4. 대칭적이고 체중부하가 이루어지는가?",
                    "5. 봉이 발가락 뒤에 위치하는가?",
                    "6. 요추의 골곡이 보이지 않는가?",
                    "7. 뒤꿈치가 바닥에 닿아 있는가?",
                ],
                "채점방식 (Standard)": ["3, 2, 1, 0"] * 7,
            }

            # 데이터프레임 생성
            df = pd.DataFrame(data)

            col2.title("Deep Squat Evaluation")

            scores = fms(matching_3[0][1])
            df["Score"] = scores

            # 최종 점수 계산
            final_score = sum(scores)

            # 결과 출력
            col2.subheader("채점 결과")
            col2.dataframe(df)

            col1.subheader("최종 점수")
            col1.write(f"최종 점수: {final_score}")




if __name__ == '__main__':
    main()