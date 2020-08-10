import os
import numpy as np
import utils.local_config as local_config
import utils.audio_utils as audio_utils
import utils.video_utils as video_utils
import tensorflow as tf
from utils.local_config import PREPROCESSED_AUDIO_DIR
from utils.local_config import PREPROCESSED_VIDEO_DIR
from utils.local_config import PREPROCESSED_AUDIO_DIR_TEMP
from utils.local_config import PREPROCESSED_VIDEO_DIR_TEMP
from utils.local_config import DATA_SAVE_DIR
from abc import ABC, abstractmethod

def zero_pad(x, n):
    diff = n - x.shape[0]
    before = diff // 2
    after = diff - before
    x = np.pad(x, (before, after))
    return x


class Preprocess(ABC):
    @abstractmethod
    def process_audio(self):
        pass

    @abstractmethod
    def process_video(self):
        pass

    @abstractmethod
    def load_audio_filenames(self):
        pass

    @abstractmethod
    def load_visual_filenames(self):
        pass
    
    @property
    @abstractmethod
    def emotion_classes():
        pass

    @property
    @abstractmethod
    def audio_duration():
        pass

    @property
    @abstractmethod
    def sample_rate():
        pass
    
    @property
    @abstractmethod
    def offset():
        pass

class RAVDESS(Preprocess):
    EMOTION_CLASSES = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']
    AUDIO_DURATION = 2.5
    OFFSET = 0.8
    SAMPLE_RATE = 441000

    def process_audio(self):
        DATASET_DIR = DATA_SAVE_DIR + '/' + 'Audio_Speech_Actors_01-24'
        OUTPUT_DIR = PREPROCESSED_AUDIO_DIR_TEMP
        for actor_folder in os.listdir(DATASET_DIR):
            print(actor_folder)
            act_no = actor_folder.split('_')[1]
            print(act_no)
            for wavfile in os.listdir(DATASET_DIR + "/" + actor_folder):

                if wavfile.endswith(".wav"):
                    print(wavfile)

                    input_video_path = DATASET_DIR + '/' + actor_folder + '/' + wavfile
                    output_dir_path = OUTPUT_DIR + '/' + actor_folder
                    audio_utils.preprocess_audio(input_video_path, output_dir_path)
    
    def process_video(self):
        DATASET_DIR = DATA_SAVE_DIR + '/' + 'ravdess_speech_videos'
        OUTPUT_DIR = PREPROCESSED_VIDEO_DIR_TEMP
        for actor_folder in os.listdir(DATASET_DIR):
            print(actor_folder)
            act_no = actor_folder.split('_')[1]
            print(act_no)
            for mp4file in os.listdir(DATASET_DIR + "/" + actor_folder):

                if mp4file.endswith(".mp4") and mp4file.startswith('01'):
                    print(mp4file)

                    input_video_path = DATASET_DIR + '/' + actor_folder + '/' + mp4file
                    output_dir_path = OUTPUT_DIR + '/' + actor_folder
                    video_utils.preprocess_video(input_video_path, output_dir_path, 10)
    
    def load_audio_filenames(self):
        print("hello") # Written by Diksha
        X, Y = [], []
        base_path = PREPROCESSED_AUDIO_DIR
        print(base_path)
        for actor_folder in os.listdir(base_path):
            actor_path = base_path + '/' + actor_folder
            files_list = []
            for audio_file in os.listdir(actor_path):
                files_list.append(audio_file)
            files_list.sort()
            for audio_file in files_list:
                audio_path = actor_path + '/' + audio_file
                # S_input = np.load(audio_path)
                # # print(S_input.shape)
                # X.append(S_input) # (216,1)
                X.append(audio_path)

                em_id = int(audio_file.split('-')[2]) - 1
                one_hot_em = tf.one_hot(em_id, len(self.EMOTION_CLASSES))
                # print(one_hot_em.shape)
                Y.append(one_hot_em)
        X = np.array(X)
        Y = np.array(Y)
        return X, Y
    
    def load_visual_filenames(self):
        X, Y = [], []
        base_path = PREPROCESSED_VIDEO_DIR
        print(base_path)
        for actor_folder in os.listdir(base_path):
            actor_path = base_path + '/' + actor_folder + '/' + 'subtracted_frames'
            files_list = []
            for image_file in os.listdir(actor_path):
                files_list.append(image_file)
            files_list.sort()
            for image_file in files_list:
                image_path = actor_path + '/' + image_file
                X.append(image_path)

                em_id = int(image_file.split('-')[2]) - 1
                one_hot_em = tf.one_hot(em_id, len(self.EMOTION_CLASSES))
                # print(one_hot_em)
                Y.append(one_hot_em)
        X = np.array(X)
        Y = np.array(Y)
        return X, Y
    
    @property
    def emotion_classes(self):
        return self.EMOTION_CLASSES

    @property
    def audio_duration(self):
        return self.AUDIO_DURATION

    @property
    def sample_rate(self):
        return self.SAMPLE_RATE

    @property
    def offset(self):
        return self.OFFSET
        
class SAVEE(Preprocess):
    EMOTION_CLASSES = ['a', 'd', 'f', 'h', 'n', 'sa', 'su']
    AUDIO_DURATION = 2
    OFFSET = 0
    SAMPLE_RATE = 441000

    def extract_em_id(self, filename):
        filename = filename.split('.')[0]
        emotion_class = ""
        for ch in filename:
            if(ch.isdigit()):
                break
            emotion_class += ch
        return self.EMOTION_CLASSES.index(emotion_class)

    def process_audio(self):
        DATASET_DIR = DATA_SAVE_DIR + '/' + 'AudioData'
        OUTPUT_DIR = PREPROCESSED_AUDIO_DIR_TEMP
        for actor_folder in os.listdir(DATASET_DIR):
            print(actor_folder)
            act_no = actor_folder
            print(act_no)
            for wavfile in os.listdir(DATASET_DIR + "/" + actor_folder):

                if wavfile.endswith(".wav"):
                    print(wavfile)

                    input_video_path = DATASET_DIR + '/' + actor_folder + '/' + wavfile
                    output_dir_path = OUTPUT_DIR + '/' + actor_folder
                    audio_utils.preprocess_audio(input_video_path, output_dir_path)
    
    def process_video(self):
        DATASET_DIR = DATA_SAVE_DIR + '/' + 'AudioVisualClip'
        OUTPUT_DIR = PREPROCESSED_VIDEO_DIR_TEMP
        for actor_folder in os.listdir(DATASET_DIR):
            print(actor_folder)
            act_no = actor_folder
            print(act_no)
            for avifile in os.listdir(DATASET_DIR + "/" + actor_folder):

                if avifile.endswith(".avi"):
                    print(avifile)

                    input_video_path = DATASET_DIR + '/' + actor_folder + '/' + avifile
                    output_dir_path = OUTPUT_DIR + '/' + actor_folder
                    video_utils.preprocess_video(input_video_path, output_dir_path, 10)
    
    def load_audio_filenames(self):
        print("hello") # Written by Diksha
        X, Y = [], []
        base_path = PREPROCESSED_AUDIO_DIR
        print(base_path)
        for actor_folder in os.listdir(base_path):
            actor_path = base_path + '/' + actor_folder
            files_list = []
            for audio_file in os.listdir(actor_path):
                files_list.append(audio_file)
            files_list.sort()
            for audio_file in files_list:
                audio_path = actor_path + '/' + audio_file
                # S_input = np.load(audio_path)
                # # print(S_input.shape)
                # X.append(S_input) # (216,1)
                X.append(audio_path)

                em_id = self.extract_em_id(audio_file)
                one_hot_em = tf.one_hot(em_id, len(self.EMOTION_CLASSES))
                # print(one_hot_em)
                Y.append(one_hot_em)
        X = np.array(X)
        Y = np.array(Y)
        return X, Y

    def load_visual_filenames(self):
        X, Y = [], []
        base_path = PREPROCESSED_VIDEO_DIR
        print(base_path)
        for actor_folder in os.listdir(base_path):
            actor_path = base_path + '/' + actor_folder + '/' + 'subtracted_frames'
            files_list = []
            for image_file in os.listdir(actor_path):
                files_list.append(image_file)
            files_list.sort()
            for image_file in files_list:
                image_path = actor_path + '/' + image_file
                X.append(image_path)

                em_id = self.extract_em_id(image_file)
                one_hot_em = tf.one_hot(em_id, len(self.EMOTION_CLASSES))
                # print(one_hot_em)
                Y.append(one_hot_em)
        X = np.array(X)
        Y = np.array(Y)
        return X, Y
    
    @property
    def emotion_classes(self):
        return self.EMOTION_CLASSES

    @property
    def audio_duration(self):
        return self.AUDIO_DURATION

    @property
    def sample_rate(self):
        return self.SAMPLE_RATE

    @property
    def offset(self):
        return self.OFFSET
        