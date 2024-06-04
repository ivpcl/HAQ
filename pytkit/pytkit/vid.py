import os
import cv2
import pytkit as pk
import tempfile
import skvideo.io as skvio


class Vid:

    vo = None
    """ Video object """

    props = {}
    """ Video properties """

    def __init__(self, pth, mode, fps=30, shape=(858, 480)):
        """
        Parameters
        ----------
        pth : Str
            Full path to video
        mode : Str
            Mode of operation. Can be `write` or `read`
        fps: Int, Optional
            Frames per second. Defaults to 30 fps
        shape: tuple
            (width, height) of the video

        Note
        ----
        For writing bitrate is set to
        """

        # check if the file exists
        if mode == "read":
            pk.fd.check_file_existance(pth)

        # Reading
        if mode == "read":
            self.vo = cv2.VideoCapture(pth)
            self.props = self._get_video_properties_reading(pth)

        elif mode == "write":
            self.vo = cv2.VideoWriter(
                pth,
                cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                fps,
                shape
            )
            self.props = self._get_video_properties_writing(pth)

        else:
            raise Exception(f"Unknown video mode \n\t{mode}")

    def _get_video_properties_reading(self, vpath):
        """ Returns a dictionary with following video properties,
        1. video_name
        2. video_ext
        3. video_path
        4. frame_rate

        Parameters
        ----------
        vpath: str
            Video file path
        """
        # Get video file name and directory location
        vdir_loc = os.path.dirname(vpath)
        vname, vext = os.path.splitext(os.path.basename(vpath))

        # Read video meta information
        vmeta = skvio.ffprobe(vpath)

        # If it is empty i.e. scikit video cannot read metadata
        # return empty stings and zeros
        if vmeta == {}:
            vprops = {
                'islocal': False,
                'full_path': vpath,
                'name': vname,
                'extension': vext,
                'dir_loc': vdir_loc,
                'frame_rate': 0,
                'duration': 0,
                'num_frames': 0,
                'width': 0,
                'height': 0,
                'frame_dim': None
            }

            return vprops

        # Calculate average frame rate
        fr_str = vmeta['video']['@avg_frame_rate']
        fr = round(int(fr_str.split("/")[0]) / int(fr_str.split("/")[1]))

        # get duration
        vdur = round(float(vmeta['video']['@duration']))

        # get number of frames
        vnbfrms = int(vmeta['video']['@nb_frames'])

        # video width
        width = int(vmeta['video']['@width'])

        # video height
        height = int(vmeta['video']['@height'])

        # Frame dimension assuming color video
        frame_dim = (height, width, 3)

        # Creating properties dictionary
        vprops = {
            'islocal': True,
            'full_path': vpath,
            'name': vname,
            'extension': vext,
            'dir_loc': vdir_loc,
            'frame_rate': fr,
            'duration': vdur,
            'num_frames': vnbfrms,
            'width': width,
            'height': height,
            'frame_dim': frame_dim
        }

        return vprops

    def _get_video_properties_writing(self, vpath):
        """ Returns a dictionary with following video properties,
        1. video_name
        2. video_ext
        3. video_path
        4. frame_rate

        Parameters
        ----------
        vpath: str
            Video file path
        """
        # Get video file name and directory location
        vdir_loc = os.path.dirname(vpath)
        vname, vext = os.path.splitext(os.path.basename(vpath))

        # Creating properties dictionary
        vprops = {
            'full_path': vpath,
            'name': vname,
            'extension': vext,
            'dir_loc': vdir_loc,
        }
        return vprops

    def get_frame(self, frm_num):
        """
        Returns a frame from video using its frame number

        Parameters
        ----------
        frm_num: int
            Frame number
        """

        # Read video and seek to frame
        self.vo.set(cv2.CAP_PROP_POS_FRAMES, frm_num)
        _, frame = self.vo.read()

        # Reset the video reader to starting frame
        self.vo.set(cv2.CAP_PROP_POS_FRAMES, 0)

        return frame

    def get_next_frame(self):
        """
        Returns a frame from video using its frame number

        Parameters
        ----------
        frm_num: int
            Frame number
        """
        _, frame = self.vo.read()
        return frame

    def write_frame(self, frm):
        """
        Write frame
        """

        # Write frame
        self.vo.write(frm)

        
    def save_spatiotemporal_trim(self, sfrm, efrm, bbox, opth):
        """
        Create a spatiotemporl trim. The output video name is
        <in_vid>_sfrm_efrm.mp4

        Parameters
        ----------
        sfrm: int
            Frame number of starting frame.
        efrm: int
            Frame number of ending frame.
        bbox: int[arr]
            Bounding box,
            [<width_location>, <height_location>, <width>, <height>]
        opth: str
            Output video path
        """
        
        # Time stamps from frame numbers
        sts = sfrm / self.props['frame_rate']
        nframes = efrm - sfrm

        # Creating ffmpeg command string
        crop_str = f"{bbox[2]}:{bbox[3]}:{bbox[0]}:{bbox[1]}"
        ffmpeg_cmd = (
            f'ffmpeg -hide_banner -loglevel warning '
            f'-y -ss {sts} -i {self.props["full_path"]} -vf "crop={crop_str}" '
            f'-c:v libx264 -crf 0 -frames:v {nframes} {opth}')
        os.system(ffmpeg_cmd)

        return opth

        
    def close(self, video_with_audio=""):
        """
        Parameters
        ----------
        video_with_audio: Str
            Path to video that has audio we need to add to the output video
            before closing
        """
        if isinstance(self.vo, cv2.VideoCapture):

            # Close cv2.VideoCapture
            self.vo.release()

        else:
            self.vo.release()
            tmp_dir = tempfile.gettempdir()
            tmp_vfile = f"{tmp_dir}/tmp.mp4"
            tmp_afile = f"{tmp_dir}/tmp.wav"

            # Do not add audio channel
            if not video_with_audio == "":

                av = video_with_audio
                extract_aud_cmd = f"ffmpeg -y -i {av} {tmp_afile}"
                cp_cmd = f"cp {self.props['full_path']} {tmp_vfile}"
                add_aud_cmd = (
                    f"ffmpeg -y -i {tmp_vfile} -i {tmp_afile} " +
                    f" -map 0:v -map 1:a -c:v libx264 "
                    f"{self.props['full_path']}"
                )

                os.system(extract_aud_cmd)
                os.system(cp_cmd)
                os.system(add_aud_cmd)
