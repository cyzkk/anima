# -*- coding: utf-8 -*-
# Copyright (c) 2012-2015, Anima Istanbul
#
# This module is part of anima-tools and is released under the BSD 2
# License: http://www.opensource.org/licenses/BSD-2-Clause

import os
import platform
import re
import itertools
import calendar
import datetime
import shutil
import tempfile
import uuid
import copy
import subprocess

from anima import logger


def all_equal(elements):
    """return True if all the elements are equal, otherwise False.
    """
    first_element = elements[0]

    for other_element in elements[1:]:
        if other_element != first_element:
            return False

    return True


def common_prefix(*sequences):
    """return a list of common elements at the start of all sequences, then a
    list of lists that are the unique tails of each sequence.
    """
    # if there are no sequences at all, we're done
    if not sequences:
        return [], []
    # loop in parallel on the sequences
    common = []
    for elements in itertools.izip(*sequences):
        # unless all elements are equal, bail out of the loop
        if not all_equal(elements):
            break

        # got one more common element, append it and keep looping
        common.append(elements[0])

    # return the common prefix and unique tails
    return common, [sequence[len(common):] for sequence in sequences]


def relpath(p1, p2, sep=os.path.sep, pardir=os.path.pardir):
    """return a relative path from p1 equivalent to path p2.

    In particular:

        the empty string, if p1 == p2;
        p2, if p1 and p2 have no common prefix.

    """
    # replace any trailing slashes at the end
    p1 = re.sub(r"[/]+$", "", p1)
    p1 = re.sub(r"[\\]+$", "", p1)

    common, (u1, u2) = common_prefix(p1.split(sep), p2.split(sep))
    if not common:
        return p2  # leave path absolute if nothing at all in common

    return sep.join([pardir] * len(u1) + u2)


def open_browser_in_location(path):
    """Opens the os native browser at the given path

    :param path: The path that the browser should be opened at.
    """
    command = []

    platform_info = platform.platform()

    path = os.path.normpath(os.path.expandvars(path))

    if not os.path.exists(path):
        path = os.path.dirname(path)

    if platform_info.startswith('Linux'):
        command = 'nautilus ' + path
    elif platform_info.startswith('Windows'):
        if os.path.isdir(path):
            command = 'explorer ' + path.replace('/', '\\')
        elif os.path.isfile(path):
            command = 'explorer /select,' + path.replace('/', '\\')
    elif platform_info.startswith('Darwin'):
        # TODO: finder can not open files for now, fix it later
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        command = 'open -a /System/Library/CoreServices/Finder.app ' + path

    if os.path.exists(path):
        subprocess.call(command, shell=True)
    else:
        raise IOError("%s doesn't exists!" % path)


def md5_checksum(path):
    """generates md5 of a file with the given path

    :param path: absolute path to  the file
    """
    import hashlib

    m = hashlib.md5()
    with open(path) as f:
        chunk = f.read(8192)
        while chunk:
            m.update(chunk)
            chunk = f.read(8192)
    return m.digest()


class StalkerThumbnailCache(object):
    """A simple file cache system
    """

    @classmethod
    def get(cls, thumbnail_full_path, login=None, password=None):
        """returns the file either from cache or from stalker server
        """
        import anima

        # look up in the cache first
        filename = os.path.basename(thumbnail_full_path)
        logger.debug('filename : %s' % filename)

        cache_path = os.path.expanduser(anima.local_cache_folder)
        cached_file_full_path = os.path.join(cache_path, filename)

        url = '%s/%s' % (
            anima.stalker_server_internal_address,
            thumbnail_full_path
        )
        login_url = '%s/login' % anima.stalker_server_internal_address

        logger.debug('cache_path            : %s' % cache_path)
        logger.debug('cached_file_full_path : %s' % cached_file_full_path)
        logger.debug('url                   : %s' % url)

        if not os.path.exists(cached_file_full_path) and login and password:
            # download the file and put it on to the cache
            import urllib
            import urllib2
            import cookielib

            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            login_data = urllib.urlencode({
                'login': login,
                'password': password,
                'submit': True
            })
            opener.open(login_url, login_data)

            resp = opener.open(url)
            data = resp.read()

            # put it in to a file
            # TODO: from header decide ascii or binary mode
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)

            with open(cached_file_full_path, 'wb') as f:
                f.write(data)

        return cached_file_full_path


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, text)


def unique(s):
    """ Return a list of elements in s in arbitrary order, but without
    duplicates.
    """

    # Try using a set first, because it's the fastest and will usually work
    try:
        return list(set(s))
    except TypeError:
        pass  # Move on to the next method

    # Since you can't hash all elements, try sorting, to bring equal items
    # together and then weed them out in a single pass
    t = list(s)
    try:
        t.sort()
    except TypeError:
        del t  # Move on to the next method
    else:
        # the sort worked, so we are fine
        # do weeding
        return [x for i, x in enumerate(t) if not i or x != t[i - 1]]
    # Brute force is all that's left
    u = []
    for x in s:
        if x not in u:
            u.append(x)

    return u


def embedded_numbers(s):
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(str(s))
    pieces[1::2] = map(int, pieces[1::2])
    return pieces


def sort_strings_with_embedded_numbers(data):
    """Sorts a string with embedded numbers

    :param list data: A list of strings
    """
    return sorted(data, key=embedded_numbers)


def do_db_setup():
    """the common routing for setting up the database
    """
    from sqlalchemy.exc import UnboundExecutionError

    from stalker import db
    from stalker.db import DBSession

    DBSession.remove()
    DBSession.close()

    try:
        DBSession.connection()
        logger.debug('already connected, not creating any new connections')
    except UnboundExecutionError:
        # no connection do setup
        logger.debug('doing a new connection with NullPool')
        from stalker import defaults
        from sqlalchemy.pool import NullPool
        settings = defaults.database_engine_settings
        settings['sqlalchemy.poolclass'] = NullPool
        db.setup(settings)


def utc_to_local(utc_dt):
    """converts utc time to local time

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def local_to_utc(local_dt):
    """converts local datetime to utc datetime

    based on the answer of J.F. Sebastian on
    http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
    """
    # get the utc_dt as if the local_dt is utc and calculate the timezone
    # difference and add it to the local dt object
    return local_dt - (utc_to_local(local_dt) - local_dt)


class MediaManager(object):
    """Manages media files.

    MediaManager is the media hub of Stalker Pyramid. It is responsible of the
    uploads/downloads of media files and all kind of conversions.

    It can convert image, video and audio files. The default format for image
    files is PNG and the default format for video os WebM (VP8), and mp3
    (stereo, 96 kBit/s) is the default format for audio files.

    It can filter files from request parameters and upload them to the server,
    also for image files it will generate thumbnails and versions to be viewed
    from web.

    It can handle image sequences, and will create only one Link object per
    image sequence. The thumbnail of an image sequence will be a gif image.

    It will generate a zip file to serve all the images in an image sequence.
    """

    def __init__(self):
        self.reference_path = 'References/Stalker_Pyramid/'
        self.version_output_path = 'Outputs/Stalker_Pyramid/'

        # accepted image formats
        self.image_formats = [
            '.gif', '.ico', '.iff',
            '.jpg', '.jpeg', '.png', '.tga', '.tif',
            '.tiff', '.bmp', '.exr',
        ]

        # accepted video formats
        self.video_formats = [
            '.3gp', '.a64', '.asf', '.avi', '.dnxhd', '.f4v', '.filmstrip',
            '.flv', '.h261', '.h263', '.h264', '.ipod', '.m4v', '.matroska',
            '.mjpeg', '.mkv', '.mov', '.mp4', '.mpeg', '.mpg', '.mpeg1video',
            '.mpeg2video', '.mv', '.mxf', '.ogg', '.rm', '.swf', '.vc1',
            '.vcd', '.vob', '.webm'
        ]

        # thumbnail format
        self.thumbnail_format = '.jpg'
        self.thumbnail_width = 512
        self.thumbnail_height = 512
        self.thumbnail_options = {  # default options for thumbnails
            'quality': 80
        }

        # images and videos for web
        self.web_image_format = '.jpg'
        self.web_image_width = 1920
        self.web_image_height = 1080

        self.web_video_format = '.webm'
        self.web_video_width = 960
        self.web_video_height = 540
        self.web_video_bitrate = 4096  # in kBits/sec

        # commands
        import anima
        self.ffmpeg_command_path = anima.ffmpeg_command_path
        self.ffprobe_command_path = anima.ffprobe_command_path

    @classmethod
    def reorient_image(cls, img):
        """re-orients rotated images by looking at EXIF data
        """
        # get the image rotation from EXIF information
        import exifread

        file_full_path = img.filename

        with open(file_full_path) as f:
            tags = exifread.process_file(f)

        orientation_string = tags.get('Image Orientation')

        if orientation_string:
            orientation = orientation_string.values[0]
            if orientation == 1:
                # do nothing
                pass
            elif orientation == 2:  # flipped in X
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:  # rotated 180 degree
                img = img.transpose(Image.ROTATE_180)
            elif orientation == 4:  # flipped in Y
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:  #
                img = img.transpose(Image.ROTATE_270)
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 7:
                img = img.transpose(Image.ROTATE_90)
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.transpose(Image.ROTATE_90)

        return img

    def generate_image_thumbnail(self, file_full_path):
        """Generates a thumbnail for the given image file

        :param file_full_path: Generates a thumbnail for the given file in the
          given path
        :return str: returns the thumbnail path
        """
        # generate thumbnail for the image and save it to a tmp folder
        suffix = self.thumbnail_format

        img = Image.open(file_full_path)
        # do a double scale
        img.thumbnail((2 * self.thumbnail_width, 2 * self.thumbnail_height))
        img.thumbnail((self.thumbnail_width, self.thumbnail_height),
                      Image.ANTIALIAS)

        # re-orient images
        img = self.reorient_image(img)

        if img.format == 'GIF':
            suffix = '.gif'  # force save in gif format
        else:
            # check if the image is in RGB mode
            if img.mode != "RGB":
                img = img.convert("RGB")

        thumbnail_path = tempfile.mktemp(suffix=suffix)

        img.save(thumbnail_path, **self.thumbnail_options)
        return thumbnail_path

    def generate_image_for_web(self, file_full_path):
        """Generates a version suitable to be viewed from a web browser.

        :param file_full_path: Generates a thumbnail for the given file in the
          given path.
        :return str: returns the thumbnail path
        """
        # generate thumbnail for the image and save it to a tmp folder
        suffix = self.thumbnail_format

        img = Image.open(file_full_path)
        if img.size[0] > self.web_image_width \
           or img.size[1] > self.web_image_height:
            # do a double scale
            img.thumbnail(
                (2 * self.web_image_width, 2 * self.web_image_height)
            )
            img.thumbnail(
                (self.web_image_width, self.web_image_height),
                Image.ANTIALIAS
            )

        # re-orient images
        img = self.reorient_image(img)

        if img.format == 'GIF':
            suffix = '.gif'  # force save in gif format
        else:
            # check if the image is in RGB mode
            if img.mode != "RGB":
                img = img.convert("RGB")

        thumbnail_path = tempfile.mktemp(suffix=suffix)

        img.save(thumbnail_path)
        return thumbnail_path

    def generate_video_thumbnail(self, file_full_path):
        """Generates a thumbnail for the given video link

        :param str file_full_path: A string showing the full path of the video
          file.
        """
        # TODO: split this in to two different methods, one generating
        #       thumbnails from the video and another one accepting three
        #       images
        media_info = self.get_video_info(file_full_path)
        video_info = media_info['video_info']

        # get the correct stream
        video_stream = None
        for stream in media_info['stream_info']:
            if stream['codec_type'] == 'video':
                video_stream = stream

        nb_frames = video_stream.get('nb_frames')
        if nb_frames is None or nb_frames == 'N/A':
            # no nb_frames
            # first try to use "r_frame_rate" and "duration"
            frame_rate = video_stream.get('r_frame_rate')

            if frame_rate is None:  # still no frame rate
                # try to use the video_info and duration
                # and try to get frame rate
                frame_rate = float(video_info.get('TAG:framerate', 23.976))
            else:
                # check if it is in Number/Number format
                if '/' in frame_rate:
                    nominator, denominator = frame_rate.split('/')
                    frame_rate = float(nominator)/float(denominator)

            # get duration
            duration = video_stream.get('duration')
            if duration == 'N/A':  # no duration
                duration = float(video_info.get('duration', 1))
            else:
                duration = float(duration)

            # at this stage we should have enough info, may not be correct but
            # we should have something
            # calculate nb_frames
            logger.debug('duration  : %s' % duration)
            logger.debug('frame_rate: %s' % frame_rate)
            nb_frames = int(duration * frame_rate)
        nb_frames = int(nb_frames)

        start_thumb_path = tempfile.mktemp(suffix=self.thumbnail_format)
        mid_thumb_path = tempfile.mktemp(suffix=self.thumbnail_format)
        end_thumb_path = tempfile.mktemp(suffix=self.thumbnail_format)

        thumbnail_path = tempfile.mktemp(suffix=self.thumbnail_format)

        # generate three thumbnails from the start, middle and end of the file
        start_frame = int(nb_frames * 0.10)
        mid_frame = int(nb_frames * 0.5)
        end_frame = int(nb_frames * 0.90) - 1

        # start_frame
        self.ffmpeg(**{
            'i': file_full_path,
            'vf': "select='eq(n,0)'",
            'vframes': start_frame,
            'o': start_thumb_path
        })
        # mid_frame
        self.ffmpeg(**{
            'i': file_full_path,
            'vf': "select='eq(n,%s)'" % mid_frame,
            'vframes': 1,
            'o': mid_thumb_path
        })
        # end_frame
        self.ffmpeg(**{
            'i': file_full_path,
            'vf': "select='eq(n,%s)'" % end_frame,
            'vframes': 1,
            'o': end_thumb_path
        })

        # check if all of the thumbnails are present
        if not os.path.exists(start_thumb_path):
            if os.path.exists(mid_thumb_path):
                start_thumb_path = mid_thumb_path
            elif os.path.exists(end_thumb_path):
                start_thumb_path = end_thumb_path
                mid_thumb_path = end_thumb_path

        if not os.path.exists(mid_thumb_path):
            if os.path.exists(start_thumb_path):
                mid_thumb_path = start_thumb_path
            else:
                start_thumb_path = end_thumb_path
                mid_thumb_path = end_thumb_path

        if not os.path.exists(end_thumb_path):
            # use the mid frame if available or the start frame
            if os.path.exists(mid_thumb_path):
                end_thumb_path = mid_thumb_path
            else:
                mid_thumb_path = start_thumb_path
                end_thumb_path = start_thumb_path

        # now merge them
        self.ffmpeg(**{
            'i': [start_thumb_path, mid_thumb_path, end_thumb_path],
            'filter_complex':
                '[0:0]scale=3*%(tw)s/4:-1,pad=%(tw)s:%(th)s[s];'
                '[1:0]scale=3*%(tw)s/4:-1,fade=out:300:30:alpha=1[m];'
                '[2:0]scale=3*%(tw)s/4:-1,fade=out:300:30:alpha=1[e];'
                '[s][e]overlay=%(tw)s/4:%(th)s-h[x];'
                '[x][m]overlay=%(tw)s/8:%(th)s/2-h/2' %
                {
                    'tw': self.thumbnail_width,
                    'th': self.thumbnail_height
                },
            'o': thumbnail_path
        })

        # remove the intermediate data
        try:
            os.remove(start_thumb_path)
        except OSError:
            pass

        try:
            os.remove(mid_thumb_path)
        except OSError:
            pass

        try:
            os.remove(end_thumb_path)
        except OSError:
            pass

        return thumbnail_path

    def generate_video_for_web(self, file_full_path):
        """Generates a web friendly version for the given video.

        :param str file_full_path: A string showing the full path of the video
          file.
        """
        web_version_full_path = tempfile.mktemp(suffix=self.web_video_format)
        self.convert_to_webm(file_full_path, web_version_full_path)
        return web_version_full_path

    def generate_thumbnail(self, file_full_path):
        """Generates a thumbnail for the given link

        :param file_full_path: Generates a thumbnail for the given file in the
          given path
        :return str: returns the thumbnail path
        """
        extension = os.path.splitext(file_full_path)[-1].lower()
        # check if it is an image or video or non of them
        if extension in self.image_formats:
            # generate a thumbnail from image
            return self.generate_image_thumbnail(file_full_path)
        elif extension in self.video_formats:
            return self.generate_video_thumbnail(file_full_path)

        # not an image nor a video so no thumbnail, raise RuntimeError
        raise RuntimeError('%s is not an image nor a video file, can not '
                           'generate a thumbnail for it!' %
                           file_full_path)

    def generate_media_for_web(self, file_full_path):
        """Generates a media suitable for web browsers.

        It will generate PNG for images, and a WebM for video files.

        :param file_full_path: Generates a web suitable version for the given
          file in the given path.
        :return str: returns the media file path.
        """
        extension = os.path.splitext(file_full_path)[-1].lower()
        # check if it is an image or video or non of them
        if extension in self.image_formats:
            # generate a thumbnail from image
            return self.generate_image_for_web(file_full_path)
        elif extension in self.video_formats:
            return self.generate_video_for_web(file_full_path)

        # not an image nor a video so no thumbnail, raise RuntimeError
        raise RuntimeError('%s is not an image nor a video file!' %
                           file_full_path)

    @classmethod
    def generate_local_file_path(cls, extension=''):
        """Generates file paths in server side storage.

        :param extension: Desired file extension
        :return:
        """
        # upload it to the stalker server side storage path
        new_filename = uuid.uuid4().hex + extension
        first_folder = new_filename[:2]
        second_folder = new_filename[2:4]

        from stalker import defaults
        file_path = os.path.join(
            defaults.server_side_storage_path,
            first_folder,
            second_folder
        )

        file_full_path = os.path.join(
            file_path,
            new_filename
        )

        return file_full_path

    def get_video_info(self, full_path):
        """Returns the video info like the duration  in seconds and fps.

        Uses ffmpeg to extract information about the video file.

        :param str full_path: The full path of the video file
        :return: int
        """
        output_buffer = self.ffprobe(**{
            'show_streams': full_path,
        })

        media_info = {
            'video_info': None,
            'stream_info': []
        }
        video_info = {}
        stream_info = {}

        # get STREAM info
        line = output_buffer.pop(0).strip()
        while line is not None:
            if line == '[STREAM]':
                # pop until you find [/STREAM]
                while line != '[/STREAM]':
                    if '=' in line:
                        flag, value = line.split('=')
                        stream_info[flag] = value
                    line = output_buffer.pop(0).strip()

                copy_stream = copy.deepcopy(stream_info)
                media_info['stream_info'].append(copy_stream)
                stream_info = {}
            try:
                line = output_buffer.pop(0).strip()
            except IndexError:
                line = None

        # also get FORMAT info
        output_buffer = self.ffprobe(**{
            'show_format': full_path,
        })

        line = output_buffer.pop(0).strip()
        while line is not None:
            if line == '[FORMAT]':
                # pop until you find [/FORMAT]
                while line != '[/FORMAT]':
                    if '=' in line:
                        flag, value = line.split('=')
                        video_info[flag] = value
                    line = output_buffer.pop(0).strip()

                media_info['video_info'] = video_info
            try:
                line = output_buffer.pop(0).strip()
            except IndexError:
                line = None

        return media_info

    def ffmpeg(self, **kwargs):
        """A simple python wrapper for ``ffmpeg`` command.
        """
        # there is only one special keyword called 'o'

        # this will raise KeyError if there is no 'o' key which is good to
        # prevent the rest to execute
        output = kwargs.get('o')
        try:
            kwargs.pop('o')
        except KeyError:  # no output
            pass

        # generate args
        args = [self.ffmpeg_command_path]
        for key in kwargs:
            flag = '-' + key
            value = kwargs[key]
            if not isinstance(value, list):
                # append the flag
                args.append(flag)
                # append the value
                args.append(str(value))
            else:
                # it is a multi flag
                # so append the flag every time you append the key
                for v in value:
                    args.append(flag)
                    args.append(str(v))

            # overwrite output

        # if output format is not a jpg or png
        if output.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'tga']:
            # use all cpus
            import multiprocessing
            num_of_threads = multiprocessing.cpu_count()
            args.append('-threads')
            args.append('%s' % num_of_threads)

        # overwrite any file
        args.append('-y')

        # append the output
        if output != '' and output is not None:  # for info only
            args.append(output)

        logger.debug('calling ffmpeg with args: %s' % args)

        process = subprocess.Popen(args, stderr=subprocess.PIPE)

        # loop until process finishes and capture stderr output
        stderr_buffer = []
        while True:
            stderr = process.stderr.readline()

            if stderr == '' and process.poll() is not None:
                break

            if stderr != '':
                stderr_buffer.append(stderr)

        # if process.returncode:
        #     # there is an error
        #     raise RuntimeError(stderr_buffer)

        logger.debug(stderr_buffer)
        logger.debug('process completed!')
        return stderr_buffer

    def ffprobe(self, **kwargs):
        """A simple python wrapper for ``ffprobe`` command.
        """
        # generate args
        args = [self.ffprobe_command_path]
        for key in kwargs:
            flag = '-' + key
            value = kwargs[key]
            if not isinstance(value, list):
                # append the flag
                args.append(flag)
                # append the value
                args.append(str(value))
            else:
                # it is a multi flag
                # so append the flag every time you append the key
                for v in value:
                    args.append(flag)
                    args.append(str(v))

        logger.debug('calling ffprobe with args: %s' % args)

        process = subprocess.Popen(args, stdout=subprocess.PIPE)

        # loop until process finishes and capture stderr output
        stdout_buffer = []
        while True:
            stdout = process.stdout.readline()

            if stdout == '' and process.poll() is not None:
                break

            if stdout != '':
                stdout_buffer.append(stdout)

        # if process.returncode:
        #     # there is an error
        #     raise RuntimeError(stderr_buffer)

        logger.debug(stdout_buffer)
        logger.debug('process completed!')
        return stdout_buffer

    @classmethod
    def convert_to_h264(cls, input_path, output_path, options=None):
        """converts the given input to h264
        """
        if options is None:
            options = {}

        # change the extension to mp4
        output_path = '%s%s' % (os.path.splitext(output_path)[0], '.mp4')

        conversion_options = {
            'i': input_path,
            'vcodec': 'libx264',
            'profile:v': 'main',
            'g': 1,  # key frame every 1 frame
            'b:v': '4096k',
            'o': output_path
        }
        conversion_options.update(options)

        cls.ffmpeg(**conversion_options)

        return output_path

    def convert_to_webm(self, input_path, output_path, options=None):
        """Converts the given input to webm format

        :param input_path: A string of path, can have wild card characters
        :param output_path: The output path
        :param options: Extra options to pass to the ffmpeg command
        :return:
        """
        if options is None:
            options = {}

        # change the extension to webm
        output_path = '%s%s' % (os.path.splitext(output_path)[0], '.webm')

        conversion_options = {
            'i': input_path,
            'vcodec': 'libvpx',
            'b:v': '%sk' % self.web_video_bitrate,
            'o': output_path
        }
        conversion_options.update(options)

        self.ffmpeg(**conversion_options)

        return output_path

    def convert_to_prores(self, input_path, output_path, options=None):
        """Converts the given input to Apple Prores 422 format.

        :param input_path: A string of path, can have wild card characters
        :param output_path: The output path
        :param options: Extra options to pass to the ffmpeg command
        :return:
        """
        if options is None:
            options = {}

        # change the extension to webm
        output_path = '%s%s' % (os.path.splitext(output_path)[0], '.mov')

        conversion_options = {
            'i': input_path,
            'probesize': 5000000,
            'f': 'image2',
            'profile:v': 3,
            'qscale:v': 13,  # use between 9 - 13
            'vcodec': 'prores_ks',
            'vendor': 'ap10',
            'pix_fmt': 'yuv422p10le',
            'o': output_path
        }
        conversion_options.update(options)

        self.ffmpeg(**conversion_options)

        return output_path

    def convert_to_mjpeg(self, input_path, output_path, options=None):
        """Converts the given input to Apple Motion Jpeg format.

        :param input_path: A string of path, can have wild card characters
        :param output_path: The output path
        :param options: Extra options to pass to the ffmpeg command
        :return:
        """
        if options is None:
            options = {}

        # change the extension to webm
        output_path = '%s%s' % (os.path.splitext(output_path)[0], '.mov')

        # ffmpeg -y
        # -probesize 5000000
        # -f image2
        # -r 48
        # -force_fps
        # -i ${DPX_HERO}
        # -c:v mjpeg
        # -qscale:v 1
        # -vendor ap10
        # -pix_fmt yuvj422p
        # -s 2048x1152
        # -r 48 output.mov
        conversion_options = {
            'i': input_path,
            'probesize': 5000000,
            'f': 'image2',
            'qscale:v': 1,
            'vcodec': 'mjpeg',
            'vendor': 'ap10',
            'pix_fmt': 'yuv422p',
            'o': output_path
        }
        conversion_options.update(options)

        self.ffmpeg(**conversion_options)

        return output_path

    @classmethod
    def convert_to_animated_gif(cls, input_path, output_path, options=None):
        """converts the given input to animated gif

        :param input_path: A string of path, can have wild card characters
        :param output_path: The output path
        :param options: Extra options to pass to the ffmpeg command
        :return:
        """
        if options is None:
            options = {}

        # change the extension to gif
        output_path = '%s%s' % (os.path.splitext(output_path)[0], '.gif')

        conversion_options = {
            'i': input_path,
            'o': output_path
        }
        conversion_options.update(options)

        cls.ffmpeg(**conversion_options)

        return output_path

    def upload_with_request_params(self, file_params):
        """upload objects with request params

        :param file_params: An object with two attributes, first a
          ``filename`` attribute and a ``file`` which is a file like object.
        """
        uploaded_file_info = []
        # get the file names
        for file_param in file_params:
            filename = file_param.filename
            file_object = file_param.file

            # upload to a temp path
            uploaded_file_full_path = self.upload_file(
                file_object,
                tempfile.mkdtemp(),
                filename
            )

            # return the file information
            file_info = {
                'full_path': uploaded_file_full_path,
                'original_filename': filename
            }

            uploaded_file_info.append(file_info)

        return uploaded_file_info

    def randomize_file_name(self, full_path):
        """randomizes the file name by adding a the first 4 characters of a
        UUID4 sequence to it.

        :param str full_path: The filename to be randomized
        :return: str
        """
        # get the filename
        path = os.path.dirname(full_path)
        filename = os.path.basename(full_path)

        # get the base name
        basename, extension = os.path.splitext(filename)

        # generate uuid4 sequence until there is no file with that name
        def generate():
            random_part = '_%s' % uuid.uuid4().hex[:4]
            return os.path.join(
                path, '%s%s%s' % (basename, random_part, extension)
            )

        random_file_full_path = generate()
        # generate until we have something unique
        # it will be the first one 99.9% of time
        while os.path.exists(random_file_full_path):
            random_file_full_path = generate()

        return random_file_full_path

    def format_filename(self, filename):
        """formats the filename to comply with file naming rules of Stalker
        Pyramid
        """
        if isinstance(filename, str):
            filename = filename.decode('utf-8')

        # replace Turkish characters
        bad_character_map = {
            '\xc3\xa7': 'c',
            '\xc4\x9f': 'g',
            '\xc4\xb1': 'i',
            '\xc3\xb6': 'o',
            '\xc5\x9f': 's',
            '\xc3\xbc': 'u',
            '\xc3\x87': 'C',
            '\xc4\x9e': 'G',
            '\xc4\xb0': 'I',
            '\xc5\x9e': 'S',
            '\xc3\x96': 'O',
            '\xc3\x9c': 'U',

            u'\xe7': 'c',
            u'\u011f': 'g',
            u'\u0131': 'i',
            u'\xf6': 'o',
            u'\u015f': 's',
            u'\xfc': 'u',
            u'\xc7': 'C',
            u'\u011e': 'G',
            u'\u0130': 'I',
            u'\u015e': 'S',
            u'\xd6': 'O',
            u'\xdc': 'U',
        }
        filename_buffer = []
        for char in filename:
            if char in bad_character_map:
                filename_buffer.append(bad_character_map[char])
            else:
                filename_buffer.append(char)
        filename = ''.join(filename_buffer)

        # replace ' ' with '_'
        basename, extension = os.path.splitext(filename)
        filename = '%s%s' % (
            re.sub(r'[\s\.\\/:\*\?"<>|=,+]+', '_', basename),
            extension
        )

        return filename

    def upload_file(self, file_object, file_path=None, filename=None):
        """Uploads files to the given path.

        The data of the files uploaded from a Web application is hold in a file
        like object. This method dumps the content of this file like object to
        the given path.

        :param file_object: File like object holding the data.
        :param str file_path: The path of the file to output the data to. If it
          is skipped the data will be written to a temp folder.
        :param str filename: The desired file name for the uploaded file. If it
          is skipped a unique temp filename will be generated.
        """
        if file_path is None:
            file_path = tempfile.gettempdir()

        if filename is None:
            filename = tempfile.mktemp(dir=file_path)
        else:
            filename = self.format_filename(filename)

        file_full_path = os.path.join(file_path, filename)
        if os.path.exists(file_full_path):
            file_full_path = self.randomize_file_name(file_full_path)

        # write down to a temp file first
        temp_file_full_path = '%s~' % file_full_path

        # create folders
        try:
            os.makedirs(file_path)
        except OSError:  # Path exist
            pass

        with open(temp_file_full_path, 'wb') as output_file:
            file_object.seek(0)
            while True:
                data = file_object.read(2 << 16)
                if not data:
                    break
                output_file.write(data)

        # data is written completely, rename temp file to original file
        os.rename(temp_file_full_path, file_full_path)

        return file_full_path

    def upload_reference(self, task, file_object, filename):
        """Uploads a reference for the given task to
        Task.path/References/Stalker_Pyramid/ folder and create a Link object
        to there. Again the Link object will have a Repository root relative
        path.

        It will also create a thumbnail under
        {{Task.absolute_path}}/References/Stalker_Pyramid/Thumbs folder and a
        web friendly version (PNG for images, WebM for video files) under
        {{Task.absolute_path}}/References/Stalker_Pyramid/ForWeb folder.

        :param task: The task that a reference is uploaded to. Should be an
          instance of :class:`.Task` class.
        :type task: :class:`.Task`
        :param file_object: The file like object holding the content of the
          uploaded file.
        :param str filename: The original filename.
        :returns: :class:`.Link` instance.
        """
        ############################################################
        # ORIGINAL
        ############################################################
        file_path = os.path.join(
            os.path.join(task.absolute_path),
            self.reference_path
        )

        # upload it
        reference_file_full_path = \
            self.upload_file(file_object, file_path, filename)

        reference_file_file_name = os.path.basename(reference_file_full_path)
        reference_file_base_name = \
            os.path.splitext(reference_file_file_name)[0]

        # create a Link instance and return it.
        # use a Repository relative path
        repo = task.project.repository

        from stalker import Repository, Link
        assert isinstance(repo, Repository)
        relative_full_path = repo.make_relative(reference_file_full_path)

        link = Link(full_path=relative_full_path, original_filename=filename)

        # create a thumbnail for the given reference
        # don't forget that the first thumbnail is the Web viewable version
        # and the second thumbnail is the thumbnail

        ############################################################
        # WEB VERSION
        ############################################################
        web_version_temp_full_path = \
            self.generate_media_for_web(reference_file_full_path)
        web_version_extension = \
            os.path.splitext(web_version_temp_full_path)[-1]

        web_version_file_name = '%s%s' % (reference_file_base_name,
                                          web_version_extension)
        web_version_full_path = \
            os.path.join(
                os.path.dirname(reference_file_full_path),
                'ForWeb',
                web_version_file_name
            )
        web_version_repo_relative_full_path = \
            repo.make_relative(web_version_full_path)
        web_version_link = Link(
            full_path=web_version_repo_relative_full_path,
            original_filename=web_version_file_name
        )

        # move it to repository
        try:
            os.makedirs(os.path.dirname(web_version_full_path))
        except OSError:  # path exists
            pass
        shutil.move(web_version_temp_full_path, web_version_full_path)

        ############################################################
        # THUMBNAIL
        ############################################################
        # finally generate a Thumbnail
        thumbnail_temp_full_path = \
            self.generate_thumbnail(reference_file_full_path)
        thumbnail_extension = os.path.splitext(thumbnail_temp_full_path)[-1]
        thumbnail_file_name = '%s%s' % (reference_file_base_name,
                                        thumbnail_extension)

        thumbnail_full_path = \
            os.path.join(
                os.path.dirname(reference_file_full_path),
                'Thumbnail',
                thumbnail_file_name
            )
        thumbnail_repo_relative_full_path = \
            repo.make_relative(thumbnail_full_path)
        thumbnail_link = Link(
            full_path=thumbnail_repo_relative_full_path,
            original_filename=thumbnail_file_name
        )

        # move it to repository
        try:
            os.makedirs(os.path.dirname(thumbnail_full_path))
        except OSError:  # path exists
            pass
        shutil.move(thumbnail_temp_full_path, thumbnail_full_path)

        ############################################################
        # LINK Objects
        ############################################################
        # link them
        # assign it as a reference to the given task
        task.references.append(link)
        link.thumbnail = web_version_link
        web_version_link.thumbnail = thumbnail_link

        return link

    def upload_version(self, task, file_object, take_name=None, extension=''):
        """Uploads versions to the Task.path/ folder and creates a Version
        object to there. Again the Version object will have a Repository root
        relative path.

        The filename of the version will be automatically generated by Stalker.

        :param task: The task that a version is uploaded to. Should be an
          instance of :class:`.Task` class.
        :param file_object: A file like object holding the content of the
          version.
        :param str take_name: A string showing the the take name of the
          Version. If skipped defaults.version_take_name will be used.
        :param str extension: The file extension of the version.
        :returns: :class:`.Version` instance.
        """
        from stalker import defaults, Version
        if take_name is None:
            take_name = defaults.version_take_name

        v = Version(task=task,
                    take_name=take_name,
                    created_with='Stalker Pyramid')
        v.update_paths()
        v.extension = extension

        # upload it
        self.upload_file(file_object, v.absolute_path, v.filename)

        return v

    def upload_version_output(self, version, file_object, filename):
        """Uploads a file as an output for the given :class:`.Version`
        instance. Will store the file in
        {{Version.absolute_path}}/Outputs/Stalker_Pyramid/ folder.

        It will also generate a thumbnail in
        {{Version.absolute_path}}/Outputs/Stalker_Pyramid/Thumbs folder and a
        web friendly version (PNG for images, WebM for video files) under
        {{Version.absolute_path}}/Outputs/Stalker_Pyramid/ForWeb folder.

        :param version: A :class:`.Version` instance that the output is
          uploaded for.
        :type version: :class:`.Version`
        :param file_object: The file like object holding the content of the
          uploaded file.
        :param str filename: The original filename.
        :returns: :class:`.Link` instance.
        """
        ############################################################
        # ORIGINAL
        ############################################################
        file_path = os.path.join(
            os.path.join(version.absolute_path),
            self.version_output_path
        )

        # upload it
        version_output_file_full_path = \
            self.upload_file(file_object, file_path, filename)

        version_output_file_name = \
            os.path.basename(version_output_file_full_path)
        version_output_base_name = \
            os.path.splitext(version_output_file_name)[0]

        # create a Link instance and return it.
        # use a Repository relative path
        repo = version.task.project.repository

        from stalker import Link
        full_path = str(version_output_file_full_path)

        link = Link(
            full_path=repo.to_os_independent_path(full_path),
            original_filename=str(filename)
        )

        # create a thumbnail for the given version output
        # don't forget that the first thumbnail is the Web viewable version
        # and the second thumbnail is the thumbnail

        ############################################################
        # WEB VERSION
        ############################################################
        web_version_link = None
        try:
            web_version_temp_full_path = \
                self.generate_media_for_web(version_output_file_full_path)
            web_version_extension = \
                os.path.splitext(web_version_temp_full_path)[-1]
            web_version_full_path = \
                os.path.join(
                    os.path.dirname(version_output_file_full_path),
                    'ForWeb',
                    version_output_base_name + web_version_extension
                )

            web_version_link = Link(
                full_path=repo.to_os_independent_path(web_version_full_path),
                original_filename=filename
            )

            # move it to repository
            try:
                os.makedirs(os.path.dirname(web_version_full_path))
            except OSError:  # path exists
                pass
            shutil.move(web_version_temp_full_path, web_version_full_path)
        except RuntimeError:
            # not an image or video so skip it
            pass

        ############################################################
        # THUMBNAIL
        ############################################################
        # finally generate a Thumbnail
        thumbnail_link = None
        try:
            thumbnail_temp_full_path = \
                self.generate_thumbnail(version_output_file_full_path)
            thumbnail_extension = os.path.splitext(thumbnail_temp_full_path)[-1]

            thumbnail_full_path = \
                os.path.join(
                    os.path.dirname(version_output_file_full_path),
                    'Thumbnail',
                    version_output_base_name + thumbnail_extension
                )

            thumbnail_link = Link(
                full_path=repo.to_os_independent_path(thumbnail_full_path),
                original_filename=filename
            )

            # move it to repository
            try:
                os.makedirs(os.path.dirname(thumbnail_full_path))
            except OSError:  # path exists
                pass
            shutil.move(thumbnail_temp_full_path, thumbnail_full_path)
        except RuntimeError:
            # not an image or video so skip it
            pass

        ############################################################
        # LINK Objects
        ############################################################
        # link them
        # assign it as an output to the given version
        version.outputs.append(link)
        if web_version_link:
            link.thumbnail = web_version_link
            if thumbnail_link:
                web_version_link.thumbnail = thumbnail_link

        return link


class Exposure(object):
    """A class for photo exposure calculation
    """

    def __init__(self, shutter=None, fstop=None, iso=None):
        self.shutter = shutter
        self.fstop = fstop
        self.iso = iso

    def to(self, other_exp):
        """calculate the exposure to equalize this exposure to the the given
        exposure

        :param other_exp: An exposure instance
        :return:
        """
        assert isinstance(other_exp, Exposure)

        import math

        shuter = math.log(other_exp.shutter / self.shutter, 2)
        fstop = math.log(
            (float(self.fstop) * float(self.fstop)) /
            (float(other_exp.fstop) * float(other_exp.fstop)), 2)
        iso = math.log(float(other_exp.iso) / float(self.iso), 2)
        return shuter + fstop + iso

    def from_(self, other_exp):
        """calculate the exposure to equalize the other exposure to this
        exposure

        :param other_exp:
        :return:
        """
        return -self.to(other_exp)
