import os
from transformers import pipeline
from deepface import DeepFace

MAX_LEN_EMO_ROBERTA = 2048
POSITIVE_EMOTIONS = ['JOY', 'SURPRISE']
NEUTRAL_EMOTIONS = ['NEUTRAL']
NEGATIVE_EMOTIONS = ['SADNESS', 'FEAR', 'ANGER', 'DISGUST']


# set project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def distilroberta_inference(classifier, text):
    emotion_labels = classifier(text)

    # emotion_labels is a list of dictionaries
    # each dictionary has two keys: 'label' and 'score'
    # 'label' is the emotion and 'score' is the confidence score

    # get the label with the highest score by iterating over the dictionaries in the list
    # and comparing the score
    max_score = 0
    for emotion_label in emotion_labels[0]:
        if emotion_label['score'] > max_score:
            max_score = emotion_label['score']
            emotion_string = emotion_label['label']
    return emotion_string.upper()



def map_deep_face_emotions(emotion):
    if emotion == 'happy':
        return 'JOY'
    elif emotion == 'surprise':
        return 'SURPRISE'
    elif emotion == 'neutral':
        return 'NEUTRAL'
    elif emotion == 'sad':
        return 'SADNESS'
    elif emotion == 'fear':
        return 'FEAR'
    elif emotion == 'angry':
        return 'ANGER'
    elif emotion == 'disgust':
        return 'DISGUST'
    elif emotion == 'FACE_NOT_DETECTED':
        return 'FACE_NOT_DETECTED'

def deepface_inference_emotions(image_path):
    # capture Value Error when no face is detected and return 'FACE NOT DETECTED'
    #try:
    #    emotions = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
    #    return map_deep_face_emotions(emotions[0]['dominant_emotion'])
    #except ValueError:
    #    return 'FACE_NOT_DETECTED'

    emotions = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
    return map_deep_face_emotions(emotions[0]['dominant_emotion'])


def deepface_inference_similarity(image_path_1, image_path_2):
    metrics = ['cosine', 'euclidean', 'euclidean_l2']
    #try:
    #    result_cosine = DeepFace.verify(img1_path=image_path_1, img2_path=image_path_2, distance_metric=metrics[0], enforce_detection=False)
        # result_euclidean = DeepFace.verify(img1_path=image_path1, img2_path=image_path2, distance_metric=metrics[1])
        # result_euclidean_l2 = DeepFace.verify(img1_path=image_path1, img2_path=image_path2, distance_metric=metrics[2])

    #    return result_cosine['verified'], result_cosine['distance'] #, result_euclidean['distance'], result_euclidean_l2['distance']
    #except ValueError:
    #    return 'FACE_NOT_DETECTED', 'FACE_NOT_DETECTED' #, 'FACE_NOT_DETECTED', 'FACE_NOT_DETECTED

    result_cosine = DeepFace.verify(img1_path=image_path_1, img2_path=image_path_2, distance_metric=metrics[0],
                                    enforce_detection=False)
    # result_euclidean = DeepFace.verify(img1_path=image_path1, img2_path=image_path2, distance_metric=metrics[1])
    # result_euclidean_l2 = DeepFace.verify(img1_path=image_path1, img2_path=image_path2, distance_metric=metrics[2])

    return result_cosine['verified'], result_cosine['distance'] #, result_euclidean['distance'], result_euclidean_l2['distance']

def map_emotions_to_sentiment(emotion):
    if emotion in POSITIVE_EMOTIONS:
        return 'POSITIVE'
    elif emotion in NEUTRAL_EMOTIONS:
        return 'NEUTRAL'
    elif emotion in NEGATIVE_EMOTIONS:
        return 'NEGATIVE'
    else:
        return 'FACE_NOT_DETECTED'


def predict_prompt_sentiment(df):
    # predict the sentiment for each type of prompt
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    df['basic_prompt_emotion'] = df['basic_prompt'].progress_apply(lambda x: distilroberta_inference(classifier,x[:MAX_LEN_EMO_ROBERTA]))

    df['basic_prompt_sentiment'] = df['basic_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
    df['plain_prompt_emotion'] = df['plain_prompt'].progress_apply(lambda x: distilroberta_inference(classifier,x[:MAX_LEN_EMO_ROBERTA]))
    df['plain_prompt_sentiment'] = df['plain_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
    df['verbalised_prompt_emotion'] = df['verbalised_prompt'].progress_apply(lambda x: distilroberta_inference(classifier,x[:MAX_LEN_EMO_ROBERTA]))
    df['verbalised_prompt_sentiment'] = df['verbalised_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
    df['wiki_abstract_prompt_emotion'] = df['wiki_abstract'].progress_apply(lambda x: distilroberta_inference(classifier,x[:MAX_LEN_EMO_ROBERTA]))
    df['wiki_abstract_prompt_sentiment'] = df['wiki_abstract_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
    return df


def predict_image_emotion(df, mode):
    # create new columns for the emotions of the images
    df['image_basic_prompt_emotion'] = ''
    df['image_plain_prompt_emotion'] = ''
    df['image_verbalised_prompt_emotion'] = ''
    df['image_wiki_abstract_prompt_emotion'] = ''

    # create columns to map emotion to sentiment
    df['image_basic_prompt_sentiment'] = ''
    df['image_plain_prompt_sentiment'] = ''
    df['image_verbalised_prompt_sentiment'] = ''
    df['image_wiki_abstract_prompt_sentiment'] = ''


    if mode == 'debug':

        for i in range(df.shape[0]):
            #df['image_basic_prompt_emotion'][i] = DeepFace.analyze(img_path=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_basic_prompt.png'),actions=['emotion'])
            df['image_basic_prompt_emotion'][i] = deepface_inference_emotions(
                image_path=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_basic_prompt.png'))
            df['image_plain_prompt_emotion'][i] = deepface_inference_emotions(
                image_path=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_plain_prompt.png'))
            df['image_verbalised_prompt_emotion'][i] = deepface_inference_emotions(
                image_path=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_verbalised_prompt.png'))
            df['image_wiki_abstract_prompt_emotion'][i] = deepface_inference_emotions(
                image_path=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_wiki_abstract_prompt.png'))

            df['image_basic_prompt_sentiment'][i] = map_emotions_to_sentiment(df['image_basic_prompt_emotion'][i])
            df['image_plain_prompt_sentiment'][i] = map_emotions_to_sentiment(df['image_plain_prompt_emotion'][i])
            df['image_verbalised_prompt_sentiment'][i] = map_emotions_to_sentiment(df['image_verbalised_prompt_emotion'][i])
            df['image_wiki_abstract_prompt_sentiment'][i] = map_emotions_to_sentiment(df['image_wiki_abstract_prompt_emotion'][i])


    else:
        # predict the emotion of the image for each kind of prompt
        df['image_basic_prompt_emotion'] = df['item_id'].progress_apply(lambda x: deepface_inference_emotions(image_path=os.path.join(project_dir, 'images', x, x + '_basic_prompt.png')))
        df['image_plain_prompt_emotion'] = df['item_id'].progress_apply(lambda x: deepface_inference_emotions(image_path=os.path.join(project_dir, 'images', x, x + '_plain_prompt.png')))
        df['image_verbalised_prompt_emotion'] = df['item_id'].progress_apply(lambda x: deepface_inference_emotions(image_path=os.path.join(project_dir, 'images', x, x + '_verbalised_prompt.png')))
        df['image_wiki_abstract_prompt_emotion'] = df['item_id'].progress_apply(lambda x: deepface_inference_emotions(image_path=os.path.join(project_dir, 'images', x, x + '_wiki_abstract_prompt.png')))

        # map the emotion to sentiment
        df['image_basic_prompt_sentiment'] = df['image_basic_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
        df['image_plain_prompt_sentiment'] = df['image_plain_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
        df['image_verbalised_prompt_sentiment'] = df['image_verbalised_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))
        df['image_wiki_abstract_prompt_sentiment'] = df['image_wiki_abstract_prompt_emotion'].progress_apply(lambda x: map_emotions_to_sentiment(x))


    return df



def compute_image_similarity(df, mode):
    # create new columns for the similarity metrics and verified for each of the metrics
    df['image_basic_prompt_similarity'] = ''
    df['image_plain_prompt_similarity'] = ''
    df['image_verbalised_prompt_similarity'] = ''
    df['image_wiki_abstract_prompt_similarity'] = ''

    df['image_basic_prompt_verified'] = ''
    df['image_plain_prompt_verified'] = ''
    df['image_verbalised_prompt_verified'] = ''
    df['image_wiki_abstract_prompt_verified'] = ''

    if mode == 'debug':
        for i in range(df.shape[0]):
            df['image_basic_prompt_similarity'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_basic_prompt.png'))[1]
            df['image_plain_prompt_similarity'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730', 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_plain_prompt.png'))[1]
            df['image_verbalised_prompt_similarity'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_verbalised_prompt.png'))[1]
            df['image_wiki_abstract_prompt_similarity'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_wiki_abstract_prompt.png'))[1]

            df['image_basic_prompt_verified'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_basic_prompt.png'))[0]
            df['image_plain_prompt_verified'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_plain_prompt.png'))[0]
            df['image_verbalised_prompt_verified'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730',   'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_verbalised_prompt.png'))[0]
            df['image_wiki_abstract_prompt_verified'][i] = deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', 'Q51730', 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', 'Q51730', 'Q51730' + '_wiki_abstract_prompt.png'))[0]

    else:
        df['image_basic_prompt_similarity'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x,  'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_basic_prompt.png'))[1])
        df['image_plain_prompt_similarity'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_plain_prompt.png'))[1])
        df['image_verbalised_prompt_similarity'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_verbalised_prompt.png'))[1])
        df['image_wiki_abstract_prompt_similarity'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_wiki_abstract_prompt.png'))[1])

        df['image_basic_prompt_verified'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_basic_prompt.png'))[0])
        df['image_plain_prompt_verified'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_plain_prompt.png'))[0])
        df['image_verbalised_prompt_verified'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_verbalised_prompt.png'))[0])
        df['image_wiki_abstract_prompt_verified'] = df['item_id'].progress_apply(lambda x: deepface_inference_similarity(image_path_1 = os.path.join(project_dir, 'images', x, 'ground_truth.jpg'), image_path_2=os.path.join(project_dir, 'images', x, x + '_wiki_abstract_prompt.png'))[0])


    return df


