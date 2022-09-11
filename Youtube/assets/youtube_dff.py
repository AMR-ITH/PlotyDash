import pandas as pd
from googleapiclient.discovery import build
from dateutil import parser
import isodate
import re
import emoji
import os


def get_data_youtube_channel(get_channel_id):
    api_key = 'AIzaSyDCbp4oZQV0SsLQK0EK-0M6Qrw5GlsrjQY'
    channel_ids = get_channel_id

    youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_stats(youtube, channel_ids):
        all_data = []
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_ids)
        response = request.execute()

        for item in response['items']:
            data = {'channelName': item['snippet']['title'],
                    'subscribers': item['statistics']['subscriberCount'],
                    #                 'views': item['statistics']['viewCount'],
                    'totalVideos': item['statistics']['videoCount'],
                    'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
                    #                 'country': item['snippet']['country']
                    }

            all_data.append(data)

        return (pd.DataFrame(all_data))

    channel_stats = get_channel_stats(youtube, channel_ids)

    ChannelName = channel_stats.loc[0, 'channelName']
    ChannelName = ''.join(str for str in ChannelName if str.isalnum())

    current_dir_path = os.getcwd()

    current_dir_path = current_dir_path + '\\assets'

    list_current_dir_path = os.listdir(current_dir_path)

    for lst_dir in list_current_dir_path:
        if lst_dir.split('_')[0] == 'youtubechannel':
            if ChannelName == lst_dir.split('_')[1].split('.')[0]:
                return ChannelName

    def get_video_ids(youtube, playlist_id):
        video_ids = []

        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        while next_page_token is not None:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

        return video_ids

    def get_video_details(youtube, video_ids):
        all_video_info = []

        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(video_ids[i:i + 50])
            )
            response = request.execute()

            for video in response['items']:
                stats_to_keep = {
                    'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt', 'categoryId'],
                    'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                    'contentDetails': ['duration', 'definition', 'caption']
                }
                video_info = {}
                video_info['video_id'] = video['id']

                for k in stats_to_keep.keys():
                    for v in stats_to_keep[k]:
                        try:
                            video_info[v] = video[k][v]
                        except:
                            video_info[v] = None

                all_video_info.append(video_info)

        return pd.DataFrame(all_video_info)

    def get_comments_in_videos(youtube, video_ids):
        """
        """
        all_comments = {}

        for video_id in video_ids:
            try:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id
                )
                response = request.execute()

                comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in
                                     response['items'][0:10]]

                #             comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

                all_comments[video_id] = comments_in_video

            except:
                continue
                # When error occurs - most likely because comments are disabled on a video

        return all_comments

    video_df = pd.DataFrame()

    playlist_id = channel_stats.loc[0, 'playlistId']

    video_id = get_video_ids(youtube, playlist_id)

    video_info = get_video_details(youtube, video_id)
    comment_dict = get_comments_in_videos(youtube, video_id)
    video_info['commenttext'] = video_info['video_id'].map(comment_dict)

    # append video data together and comment data toghether
    video_df = pd.concat([video_info, video_df])

    '''
    '''

    # Create publish day (in the week) column
    video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x))
    video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))
    # convert duration to seconds
    video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds())
    video_df['tagsCount'] = video_df['tags'].apply(lambda x: 0 if x is None else len(x))
    video_df['titleLength'] = video_df['title'].apply(lambda x: len(x))

    def no_of_words(title):
        # removes all speciall character from the word
        title = re.sub(r"[^a-zA-Z0-9]+", ' ', title)
        count = 0
        for letter in title:
            if letter == ' ':
                count += 1
        return count + 1

    def day_predictor(pushblishDayName):
        day = pushblishDayName
        if day in ['Sunday', 'Saturday']:
            return 'weekend'
        else:
            return 'weekday'

    def min_caterory(secs):
        min = round(secs / 60)
        if min <= 3:
            return "0-3mins"
        elif 3 < min <= 6:
            return "3-6mins"
        elif 6 < min <= 10:
            return "6-10mins"
        elif 10 < min <= 15:
            return "10-15mins"
        elif 15 < min <= 20:
            return "15-20mins"
        elif 20 < min <= 25:
            return "20-25mins"
        elif 25 < min <= 30:
            return "25-30mins"
        elif 30 < min <= 40:
            return "30-40mins"
        elif 40 < min <= 60:
            return "40-60mins"
        elif 60 < min <= 90:
            return "1-1.5h"
        elif 90 < min <= 120:
            return "1.5-2h"
        else:
            return "greater-2h"

    def emoji_counter(comments):
        total_count_emoji = 0
        try:
            for emojis in comments:
                emoji_count = emoji.emoji_count(emojis, unique=True)
                total_count_emoji = total_count_emoji + emoji_count
        except:
            # When error occurs - most likely because of float' object is not iterable
            print('error ouccured')
        return total_count_emoji

    video_df['durationmins'] = video_df['durationSecs'].apply(min_caterory)
    video_df['no_words_title'] = video_df['title'].apply(no_of_words)
    video_df['weekdayVsweekend'] = video_df['pushblishDayName'].apply(day_predictor)
    video_df['emoji_counts'] = video_df['commenttext'].apply(emoji_counter)

    video_df.to_csv(f'assets/youtubechannel_{ChannelName}.csv', index=False)

    return ChannelName
